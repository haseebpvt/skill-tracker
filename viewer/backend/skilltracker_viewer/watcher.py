"""Debounced filesystem watching for ``data/`` and ``evidence/``."""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger("skilltracker.viewer.watcher")

#: Editors and atomic writes produce a lot of noise; only markdown matters.
WATCHED_SUFFIXES = (".md",)


class _Handler(FileSystemEventHandler):
    def __init__(self, notify: Callable[[], None]) -> None:
        self._notify = notify

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        paths = [str(getattr(event, "src_path", "")), str(getattr(event, "dest_path", "") or "")]
        for path in paths:
            name = Path(path).name
            # Skip our own atomic-write temp files (".topics.md.xxxx.tmp").
            if name.startswith(".") or name.endswith(".tmp"):
                continue
            if path.endswith(WATCHED_SUFFIXES):
                self._notify()
                return


class RepoWatcher:
    """Watches sub-directories of the repo and fires ``on_change`` once per burst."""

    def __init__(
        self,
        *,
        root: Path,
        paths: list[str],
        on_change: Callable[[], object],
        debounce: float = 0.3,
    ) -> None:
        self._root = root
        self._paths = paths
        self._on_change = on_change
        self._debounce = debounce
        self._observer: Observer | None = None
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def _schedule_fire(self) -> None:
        """Restart the debounce timer; a burst of saves fires exactly once."""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self._debounce, self._fire)
            self._timer.daemon = True
            self._timer.start()

    def _fire(self) -> None:
        try:
            self._on_change()
        except Exception:  # pragma: no cover - never kill the watcher thread
            logger.exception("change handler failed")

    def start(self) -> None:
        observer = Observer()
        handler = _Handler(self._schedule_fire)
        watched = 0
        for relative in self._paths:
            target = self._root / relative
            if target.is_dir():
                observer.schedule(handler, str(target), recursive=True)
                watched += 1
            else:
                logger.warning("not watching missing directory %s", target)
        if watched:
            observer.start()
            self._observer = observer

    def stop(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
        if self._observer is not None:
            self._observer.stop()
            self._observer.join(timeout=2)
            self._observer = None
