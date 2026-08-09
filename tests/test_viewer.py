"""The read-only viewer backend."""

from __future__ import annotations

import asyncio
import json

import pytest
from fastapi.testclient import TestClient

from core.repo import Repo
from skilltracker_viewer.app import ViewerState, _sse, create_app, event_stream


@pytest.fixture
def client(repo: Repo):
    with TestClient(create_app(repo.root)) as test_client:
        yield test_client


def test_health(client, repo: Repo):
    body = client.get("/api/health").json()
    assert body["ok"] is True
    assert body["repo"] == str(repo.root)


def test_state_matches_the_contract(client):
    body = client.get("/api/state").json()
    assert body["role"]["role"] == "Agentic AI Engineer"
    assert [s["id"] for s in body["skills"]] == ["alpha", "beta"]
    assert body["summary"]["min_bar"] == {"total": 2, "met": 1}
    assert [t["id"] for t in body["focus"]] == ["second-topic"]

    topic = body["skills"][0]["topics"][0]
    for key in ("id", "title", "status", "priority", "min_required", "focus", "enough_md", "log_md", "body_md"):
        assert key in topic, f"missing '{key}' in the topic payload"


def test_state_reflects_writes_without_a_restart(client, repo: Repo):
    assert client.get("/api/state").json()["skills"][0]["topics"][0]["status"] == "learning"
    repo.update_topic_status("alpha", "first-topic", "strong")
    assert client.get("/api/state").json()["skills"][0]["topics"][0]["status"] == "strong"


def test_broken_repo_surfaces_issues_instead_of_500(client, repo: Repo):
    (repo.root / "data" / "skills" / "alpha" / "topics.md").write_text("## Broken\n\nno meta\n", encoding="utf-8")
    response = client.get("/api/state")
    assert response.status_code == 200
    assert any(issue["level"] == "error" for issue in response.json()["issues"])


def test_events_stream_opens_with_a_state_event(repo: Repo):
    async def scenario():
        viewer = ViewerState(repo)
        stream = event_stream(viewer)
        try:
            first = await anext(stream)
            assert first.startswith(b"event: state\ndata: ")

            # A change published while the client is connected is pushed to it.
            await asyncio.to_thread(repo.update_topic_status, "alpha", "first-topic", "strong")
            await viewer.refresh_and_publish()
            second = await anext(stream)
        finally:
            await stream.aclose()
        return first, second

    first, second = asyncio.run(scenario())

    initial = json.loads(first.split(b"data: ", 1)[1])
    assert initial["role"]["role"] == "Agentic AI Engineer"
    assert initial["skills"][0]["topics"][0]["status"] == "learning"

    assert second.startswith(b"event: state\n")
    pushed = json.loads(second.split(b"data: ", 1)[1])
    assert pushed["skills"][0]["topics"][0]["status"] == "strong"


def test_stream_unsubscribes_when_the_client_disconnects(repo: Repo):
    async def scenario():
        viewer = ViewerState(repo)
        stream = event_stream(viewer)
        await anext(stream)
        assert viewer.broadcaster.client_count == 1
        await stream.aclose()
        return viewer.broadcaster.client_count

    assert asyncio.run(scenario()) == 0


def test_events_endpoint_sets_streaming_headers(repo: Repo):
    """Built without consuming the stream — it never ends, so a client would hang."""
    app = create_app(repo.root)
    route = next(r for r in app.routes if getattr(r, "path", "") == "/api/events")

    async def build():
        response = await route.endpoint()
        await response.body_iterator.aclose()  # generator was never started
        return response

    response = asyncio.run(build())
    assert response.media_type == "text/event-stream"
    assert response.headers["cache-control"].startswith("no-cache")
    assert response.headers["x-accel-buffering"] == "no"


def test_there_are_no_write_endpoints(client):
    """The viewer is read-only by design (§10). Guard against regressions."""
    routes = client.app.routes
    for route in routes:
        for method in getattr(route, "methods", set()):
            assert method in {"GET", "HEAD", "OPTIONS"}, f"{route.path} exposes {method}"


def test_sse_frame_encoding():
    assert _sse("state", '{"a":1}') == b'event: state\ndata: {"a":1}\n\n'


def test_sse_frame_escapes_multiline_payloads():
    """A raw newline mid-payload would truncate the event, so each line is prefixed."""
    assert _sse("state", "line1\nline2") == b"event: state\ndata: line1\ndata: line2\n\n"


def test_missing_ui_build_returns_a_helpful_message(client):
    response = client.get("/")
    assert response.status_code == 503
    assert "npm run build" in response.json()["fix"]
