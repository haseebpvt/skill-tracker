"""Append-only event log: ``data/history.jsonl``.

Every progress-affecting write records one line here. This is what makes
velocity and forecasting possible — the ``updated:`` field on a topic only
tells you *when it last changed*, not the shape of the curve that got it there.

JSONL rather than markdown on purpose: appending never rewrites earlier lines,
so the git diff for a study session is the handful of lines you actually added,
and two machines editing on different days merge without conflict.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .models import Issue

HISTORY_FILE = "data/history.jsonl"

#: Event types. Anything else is kept but will not be specially rendered.
STATUS_CHANGE = "status_change"
TOPIC_ADDED = "topic_added"
SKILL_ADDED = "skill_added"
FOCUS_SET = "focus_set"
MILESTONE_SET = "milestone_set"
MILESTONE_REMOVED = "milestone_removed"
CONCLUSIONS_UPDATED = "conclusions_updated"
NOTE = "note"

KNOWN_TYPES = (
    STATUS_CHANGE,
    TOPIC_ADDED,
    SKILL_ADDED,
    FOCUS_SET,
    MILESTONE_SET,
    MILESTONE_REMOVED,
    CONCLUSIONS_UPDATED,
    NOTE,
)


def utc_now() -> str:
    """Current time as an ISO-8601 UTC string. Single place to stub in tests."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class Event:
    """One recorded change. Only ``ts`` and ``type`` are guaranteed."""

    ts: str
    type: str
    skill_id: str = ""
    topic_id: str = ""
    from_status: str = ""
    to_status: str = ""
    note: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def to_line(self) -> str:
        payload: dict[str, Any] = {"ts": self.ts, "type": self.type}
        for key, value in (
            ("skill_id", self.skill_id),
            ("topic_id", self.topic_id),
            ("from", self.from_status),
            ("to", self.to_status),
            ("note", self.note),
        ):
            if value:
                payload[key] = value
        if self.data:
            payload["data"] = self.data
        return json.dumps(payload, ensure_ascii=False, sort_keys=False)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ts": self.ts,
            "type": self.type,
            "skill_id": self.skill_id,
            "topic_id": self.topic_id,
            "from": self.from_status,
            "to": self.to_status,
            "note": self.note,
            "data": dict(self.data),
        }

    @property
    def date(self) -> str:
        """The ``YYYY-MM-DD`` part, for day-level grouping."""
        return self.ts[:10]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Event":
        data = raw.get("data")
        return cls(
            ts=str(raw.get("ts", "")),
            type=str(raw.get("type", NOTE)),
            skill_id=str(raw.get("skill_id", "") or ""),
            topic_id=str(raw.get("topic_id", "") or ""),
            from_status=str(raw.get("from", "") or ""),
            to_status=str(raw.get("to", "") or ""),
            note=str(raw.get("note", "") or ""),
            data=data if isinstance(data, dict) else {},
        )


def append_events(root: Path, events: Iterable[Event]) -> int:
    """Append events to the log, creating it if needed. Returns how many."""
    events = [e for e in events if e is not None]
    if not events:
        return 0

    path = root / HISTORY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    # Plain append: never rewrites existing lines, so a partial write can only
    # ever damage the tail, which read_events skips as malformed.
    with path.open("a", encoding="utf-8") as handle:
        for event in events:
            handle.write(event.to_line() + "\n")
    return len(events)


def read_events(root: Path) -> tuple[list[Event], list[Issue]]:
    """Read the whole log in file order, skipping unparseable lines."""
    path = root / HISTORY_FILE
    if not path.is_file():
        return [], []

    events: list[Event] = []
    issues: list[Issue] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            issues.append(Issue("warning", f"history line {number} is not valid JSON — skipped", HISTORY_FILE))
            continue
        if not isinstance(raw, dict) or not raw.get("ts"):
            issues.append(Issue("warning", f"history line {number} is missing 'ts' — skipped", HISTORY_FILE))
            continue
        events.append(Event.from_dict(raw))

    events.sort(key=lambda e: e.ts)
    return events, issues


def describe(event: Event) -> str:
    """A one-line human sentence for an event, used in ROADMAP.md."""
    label = event.topic_id or event.skill_id or ""
    if event.type == STATUS_CHANGE:
        return f"{label}: {event.from_status or '?'} → {event.to_status or '?'}"
    if event.type == TOPIC_ADDED:
        return f"added topic {label}"
    if event.type == SKILL_ADDED:
        return f"added skill {label}"
    if event.type == FOCUS_SET:
        focused = event.data.get("focused") or []
        return "focus set to " + (", ".join(focused) if focused else "nothing")
    if event.type == MILESTONE_SET:
        return f"milestone '{event.data.get('milestone_id', label)}' updated"
    if event.type == MILESTONE_REMOVED:
        return f"milestone '{event.data.get('milestone_id', label)}' removed"
    if event.type == CONCLUSIONS_UPDATED:
        return "conclusions recompiled"
    return event.note or event.type
