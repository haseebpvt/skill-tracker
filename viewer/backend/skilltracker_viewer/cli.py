"""Command line entry point for the viewer backend."""

from __future__ import annotations

import argparse
import logging

import uvicorn

from core.paths import find_repo_root

from .app import DEFAULT_PORT, create_app


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skilltracker-viewer", description="Serve the skill tracker viewer")
    parser.add_argument("--repo", default=None, help="path to the skill-tracker repo (default: auto-detect)")
    parser.add_argument("--host", default="127.0.0.1", help="bind host (default: localhost only)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"port (default: {DEFAULT_PORT})")
    parser.add_argument("--log-level", default="warning", help="uvicorn log level")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    root = find_repo_root(args.repo)
    app = create_app(root)

    print(f"Skill Tracker  →  http://localhost:{args.port}")
    print(f"repo: {root}")
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
