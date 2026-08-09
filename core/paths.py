"""Repo root discovery and path sandboxing.

Every read/write in this project goes through :func:`safe_path`, so a bad
argument from an agent can never touch a file outside the repo.
"""

from __future__ import annotations

import os
from pathlib import Path

#: Marker files that identify the skill-tracker repo root.
_ROOT_MARKERS = ("MASTER.md", "data")

#: Environment variable used to point the MCP server / viewer at a repo
#: explicitly, for when the process is not started from inside it.
REPO_ENV_VAR = "SKILL_TRACKER_REPO"


class PathEscapeError(ValueError):
    """Raised when a caller-supplied path resolves outside the repo root."""


def find_repo_root(start: Path | str | None = None) -> Path:
    """Locate the repo root.

    Order of precedence: explicit ``start`` argument, the ``SKILL_TRACKER_REPO``
    environment variable, then an upward walk from the current directory
    looking for the marker files.
    """
    if start is not None:
        return Path(start).expanduser().resolve()

    env = os.environ.get(REPO_ENV_VAR)
    if env:
        return Path(env).expanduser().resolve()

    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if all((candidate / marker).exists() for marker in _ROOT_MARKERS):
            return candidate

    # Fall back to the package's own repo (…/core/paths.py → repo root).
    packaged = Path(__file__).resolve().parent.parent
    if all((packaged / marker).exists() for marker in _ROOT_MARKERS):
        return packaged

    return here


def safe_path(root: Path, *parts: str | Path) -> Path:
    """Join ``parts`` onto ``root`` and refuse anything that escapes it.

    Absolute inputs are allowed only if they already live under ``root``.
    """
    root = root.resolve()
    joined = Path(*[str(p) for p in parts]) if parts else Path()
    target = joined if joined.is_absolute() else root / joined

    # resolve() follows symlinks, which is what we want: a symlink pointing
    # out of the repo is an escape too.
    resolved = Path(os.path.normpath(target)).resolve()
    if resolved != root and root not in resolved.parents:
        raise PathEscapeError(f"path {joined!s} resolves outside the repo root")
    return resolved


def relative_to_root(root: Path, path: Path) -> str:
    """Return ``path`` as a POSIX-style string relative to ``root``."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
