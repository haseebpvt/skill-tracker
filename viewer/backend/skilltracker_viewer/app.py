"""Read-only viewer backend.

Parses the repo into JSON, serves the built React UI, and pushes a fresh state
over SSE whenever a file under ``data/`` or ``evidence/`` changes.

There are no write endpoints, by design (§10 of the plan): the MCP server and
the human are the only writers. The backend never talks to the MCP server — it
just watches the filesystem, which is what makes MCP-made edits show up here.
"""

from __future__ import annotations

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from core.repo import Repo

from .watcher import RepoWatcher

logger = logging.getLogger("skilltracker.viewer")

#: Uncommon port, so it does not collide with the usual dev servers.
DEFAULT_PORT = 8749

#: Coalesce bursts of file events (an editor save is often several).
DEBOUNCE_SECONDS = 0.3

#: Keepalive cadence for idle SSE connections.
PING_SECONDS = 20.0


class Broadcaster:
    """Fan out state snapshots to every connected SSE client."""

    def __init__(self) -> None:
        self._clients: set[asyncio.Queue[str]] = set()
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue[str]:
        queue: asyncio.Queue[str] = asyncio.Queue(maxsize=8)
        async with self._lock:
            self._clients.add(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue[str]) -> None:
        async with self._lock:
            self._clients.discard(queue)

    async def publish(self, payload: str) -> None:
        async with self._lock:
            clients = list(self._clients)
        for queue in clients:
            try:
                queue.put_nowait(payload)
            except asyncio.QueueFull:
                # A client that cannot keep up will refetch on reconnect.
                logger.debug("dropping event for a slow SSE client")

    @property
    def client_count(self) -> int:
        return len(self._clients)


class ViewerState:
    """Holds the parsed repo and re-parses it on demand."""

    def __init__(self, repo: Repo) -> None:
        self.repo = repo
        self.broadcaster = Broadcaster()
        self._cache: dict[str, Any] | None = None
        self._lock = asyncio.Lock()

    async def snapshot(self, *, refresh: bool = False) -> dict[str, Any]:
        async with self._lock:
            if self._cache is None or refresh:
                # Parsing touches the filesystem; keep the event loop free.
                self._cache = await asyncio.to_thread(self._parse)
            return self._cache

    def _parse(self) -> dict[str, Any]:
        try:
            return self.repo.load().to_dict()
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("failed to parse repo")
            return {
                "role": None,
                "skills": [],
                "focus": [],
                "summary": {
                    "overall_percent": 0.0,
                    "total_topics": 0,
                    "counts": {},
                    "min_bar": {"total": 0, "met": 0},
                },
                "conclusions": {"exists": False},
                "evidence_status": {"new": [], "modified": [], "deleted": [], "unchanged": []},
                "git": {"available": False},
                "issues": [{"level": "error", "path": "", "message": f"failed to parse repo: {exc}"}],
            }

    async def refresh_and_publish(self) -> None:
        state = await self.snapshot(refresh=True)
        await self.broadcaster.publish(json.dumps(state))


def create_app(repo_root: Path | str | None = None) -> FastAPI:
    repo = Repo(repo_root)
    viewer = ViewerState(repo)
    ui_dist = repo.root / "viewer" / "ui" / "dist"

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        loop = asyncio.get_running_loop()
        watcher = RepoWatcher(
            root=repo.root,
            paths=["data", "evidence"],
            debounce=DEBOUNCE_SECONDS,
            on_change=lambda: asyncio.run_coroutine_threadsafe(viewer.refresh_and_publish(), loop),
        )
        watcher.start()
        logger.info("watching %s for changes", repo.root)
        try:
            yield
        finally:
            watcher.stop()

    app = FastAPI(title="Skill Tracker viewer", version="0.1.0", lifespan=lifespan)
    app.state.viewer = viewer

    @app.get("/api/state")
    async def get_state() -> JSONResponse:
        """The full parsed model. Always re-read so a manual edit is never stale."""
        return JSONResponse(await viewer.snapshot(refresh=True))

    @app.get("/api/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": True,
            "repo": str(repo.root),
            "ui_built": ui_dist.is_dir(),
            "sse_clients": viewer.broadcaster.client_count,
        }

    @app.get("/api/events")
    async def events() -> StreamingResponse:
        """SSE stream: the current state on connect, then one event per change."""
        return StreamingResponse(
            event_stream(viewer),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache, no-transform",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    _mount_ui(app, ui_dist)
    return app


async def event_stream(viewer: ViewerState) -> AsyncIterator[bytes]:
    """Yield the current state, then one frame per change, pinging when idle.

    Module-level rather than nested in the route so it can be driven directly
    in tests — an endless generator is awkward to tear down through a test client.
    """
    queue = await viewer.broadcaster.subscribe()
    try:
        yield _sse("state", json.dumps(await viewer.snapshot(refresh=True)))
        while True:
            try:
                payload = await asyncio.wait_for(queue.get(), timeout=PING_SECONDS)
            except asyncio.TimeoutError:
                yield _sse("ping", "{}")
                continue
            yield _sse("state", payload)
    finally:
        await viewer.broadcaster.unsubscribe(queue)


def _sse(event: str, data: str) -> bytes:
    """Encode one SSE frame. Data must not contain raw newlines mid-field."""
    lines = "".join(f"data: {line}\n" for line in data.split("\n"))
    return f"event: {event}\n{lines}\n".encode("utf-8")


def _mount_ui(app: FastAPI, dist: Path) -> None:
    """Serve the built UI at ``/``, with a helpful page if it is not built yet."""
    if dist.is_dir() and (dist / "index.html").is_file():
        app.mount("/", StaticFiles(directory=dist, html=True), name="ui")
        return

    @app.get("/")
    async def missing_ui() -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={
                "error": "The UI has not been built yet.",
                "fix": "Run scripts/launch.py, or: cd viewer/ui && npm install && npm run build",
                "expected_at": str(dist),
            },
        )
