"""Read-only git status for the viewer header.

Per §10 of the plan the app never runs git *write* commands — the human pushes
and pulls manually. This module only ever reads.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

_TIMEOUT_SECONDS = 3


def _run(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def git_status(root: Path) -> dict[str, Any]:
    """Branch, dirty flag and last commit, or ``{"available": False}``."""
    inside = _run(root, "rev-parse", "--is-inside-work-tree")
    if inside != "true":
        return {"available": False}

    branch = _run(root, "rev-parse", "--abbrev-ref", "HEAD") or ""
    porcelain = _run(root, "status", "--porcelain")
    last_commit = _run(root, "log", "-1", "--pretty=%h %s")

    return {
        "available": True,
        "branch": branch,
        "dirty": bool(porcelain),
        "changed_files": len([line for line in (porcelain or "").splitlines() if line.strip()]),
        "last_commit": last_commit or "",
    }
