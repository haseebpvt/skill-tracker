#!/usr/bin/env python3
"""One-command launcher for the Skill Tracker viewer.

    python scripts/launch.py            # sync deps, build UI if stale, serve, open browser
    python scripts/launch.py --dev      # also run the Vite dev server for UI work
    python scripts/launch.py --no-open  # do not open a browser

Deliberately dependency-free: this runs on a bare system Python, before
anything is installed.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UI_DIR = REPO_ROOT / "viewer" / "ui"
DIST_DIR = UI_DIR / "dist"
DEFAULT_PORT = 8749
VITE_DEV_PORT = 5174


def info(message: str) -> None:
    print(f"  {message}")


def step(message: str) -> None:
    print(f"\n\033[1m{message}\033[0m")


def fail(message: str) -> "NoReturn":  # type: ignore[valid-type]
    print(f"\n\033[31merror:\033[0m {message}", file=sys.stderr)
    raise SystemExit(1)


def require(tool: str, hint: str) -> str:
    path = shutil.which(tool)
    if path is None:
        fail(f"'{tool}' not found on PATH. {hint}")
    return path


def run(cmd: list[str], *, cwd: Path, what: str) -> None:
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        fail(f"{what} failed (exit {result.returncode}): {' '.join(cmd)}")


# ----------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------


def sync_python(skip: bool) -> None:
    step("Python dependencies")
    if skip:
        info("skipped (--skip-deps)")
        return
    uv = require("uv", "Install it from https://docs.astral.sh/uv/ then re-run.")
    run([uv, "sync", "--quiet"], cwd=REPO_ROOT, what="uv sync")
    info("up to date")


def ui_is_stale() -> bool:
    """True if dist/ is missing or older than any UI source file."""
    index = DIST_DIR / "index.html"
    if not index.is_file():
        return True

    built_at = index.stat().st_mtime
    watched: list[Path] = [UI_DIR / "package.json", UI_DIR / "vite.config.js", UI_DIR / "index.html"]
    src = UI_DIR / "src"
    if src.is_dir():
        watched.extend(p for p in src.rglob("*") if p.is_file())

    return any(path.is_file() and path.stat().st_mtime > built_at for path in watched)


def build_ui(force: bool, skip: bool) -> None:
    step("UI build")
    if skip:
        info("skipped (--skip-build)")
        return
    if not force and not ui_is_stale():
        info("dist/ is current — nothing to build")
        return

    npm = require("npm", "Install Node.js (which ships npm) then re-run.")
    if not (UI_DIR / "node_modules").is_dir():
        info("installing npm packages (first run, this takes a minute)...")
        lockfile = UI_DIR / "package-lock.json"
        run([npm, "ci" if lockfile.is_file() else "install"], cwd=UI_DIR, what="npm install")

    info("building...")
    run([npm, "run", "build"], cwd=UI_DIR, what="npm run build")
    info("built")


# ----------------------------------------------------------------------
# Serving
# ----------------------------------------------------------------------


def check_port_free(port: int) -> None:
    """Fail early with a readable message instead of a uvicorn bind traceback."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        if probe.connect_ex(("127.0.0.1", port)) != 0:
            return

    try:
        with urllib.request.urlopen(f"http://localhost:{port}/api/health", timeout=1) as response:
            if b'"ok"' in response.read():
                fail(
                    f"Skill Tracker is already running on port {port}.\n"
                    f"       Open http://localhost:{port}/ , or stop it and re-run."
                )
    except (urllib.error.URLError, OSError):
        pass

    fail(f"Port {port} is already in use by something else. Re-run with --port <other>.")


def wait_until_up(url: str, timeout: float = 25.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1):
                return True
        except (urllib.error.URLError, OSError):
            time.sleep(0.25)
    return False


def open_browser_when_ready(url: str, health_url: str) -> None:
    def worker() -> None:
        if wait_until_up(health_url):
            webbrowser.open(url)

    threading.Thread(target=worker, daemon=True).start()


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch the Skill Tracker viewer")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"backend port (default {DEFAULT_PORT})")
    parser.add_argument("--dev", action="store_true", help="also run the Vite dev server with hot reload")
    parser.add_argument("--no-open", action="store_true", help="do not open a browser")
    parser.add_argument("--rebuild", action="store_true", help="force a UI rebuild even if dist/ looks current")
    parser.add_argument("--skip-deps", action="store_true", help="skip 'uv sync'")
    parser.add_argument("--skip-build", action="store_true", help="skip the UI build")
    args = parser.parse_args()

    print("\033[1mSkill Tracker\033[0m")
    info(f"repo: {REPO_ROOT}")

    check_port_free(args.port)
    sync_python(args.skip_deps)
    # In dev mode Vite serves the UI itself, so a production build is pointless.
    build_ui(force=args.rebuild, skip=args.skip_build or args.dev)

    uv = require("uv", "Install it from https://docs.astral.sh/uv/ then re-run.")
    backend = [uv, "run", "skilltracker-viewer", "--port", str(args.port), "--repo", str(REPO_ROOT)]

    vite = None
    if args.dev:
        step("Vite dev server")
        npm = require("npm", "Install Node.js then re-run.")
        if not (UI_DIR / "node_modules").is_dir():
            run([npm, "install"], cwd=UI_DIR, what="npm install")
        vite = subprocess.Popen([npm, "run", "dev", "--", "--port", str(VITE_DEV_PORT)], cwd=UI_DIR)
        info(f"http://localhost:{VITE_DEV_PORT} (proxies /api to the backend)")

    url = f"http://localhost:{VITE_DEV_PORT if args.dev else args.port}/"
    step("Serving")
    if not args.no_open:
        open_browser_when_ready(url, f"http://localhost:{args.port}/api/health")
    print(f"  {url}")
    print("  Ctrl-C to stop\n")

    try:
        subprocess.run(backend, cwd=REPO_ROOT)
    except KeyboardInterrupt:
        pass
    finally:
        if vite is not None:
            vite.terminate()
            try:
                vite.wait(timeout=5)
            except subprocess.TimeoutExpired:
                vite.kill()
    return 0


if __name__ == "__main__":
    os.environ.setdefault("SKILL_TRACKER_REPO", str(REPO_ROOT))
    raise SystemExit(main())
