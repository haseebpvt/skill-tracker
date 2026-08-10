"""Renders the generated ``ROADMAP.md`` status report at the repo root.

Regenerated after every write, so it is never stale. Because it is committed
alongside the data, ``git log -p ROADMAP.md`` becomes a readable record of how
progress actually unfolded — which is the point of writing it to disk at all
rather than only rendering it in the viewer.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from .history import Event, describe
from .models import STATUSES

BANNER = "<!-- GENERATED FILE — do not edit by hand. Rewritten on every progress change. -->"

#: How many recent events to include.
ACTIVITY_LIMIT = 15

_BAR_WIDTH = 24

_STATUS_LABEL = {
    "done": "done",
    "on-track": "on track",
    "at-risk": "at risk",
    "overdue": "OVERDUE",
    "blocked": "blocked",
    "planned": "planned",
}


def bar(percent: float, width: int = _BAR_WIDTH) -> str:
    """A text progress bar that stays readable in a diff."""
    filled = int(round(max(0.0, min(100.0, percent)) / 100 * width))
    return "█" * filled + "░" * (width - filled)


def render_roadmap_doc(state_dict: dict[str, Any], events: list[Event], *, today: date) -> str:
    """Build the whole document from an already-derived state payload."""
    role = state_dict.get("role") or {}
    summary = state_dict.get("summary") or {}
    roadmap = state_dict.get("roadmap") or {}
    velocity = state_dict.get("velocity") or {}

    lines: list[str] = [BANNER, ""]
    title = role.get("role") or "Skill Tracker"
    level = role.get("level")
    lines.append(f"# Roadmap — {title}" + (f" ({level})" if level else ""))
    lines.append("")
    lines.append(f"_Generated {today.isoformat()}._")
    lines.append("")

    lines += _headline(summary, roadmap, velocity)
    lines += _milestones(roadmap, today=today)
    lines += _forecast(velocity, roadmap)
    lines += _skills(state_dict)
    lines += _activity(events)

    return "\n".join(lines).rstrip("\n") + "\n"


def _headline(summary: dict, roadmap: dict, velocity: dict) -> list[str]:
    percent = summary.get("overall_percent", 0.0)
    total = summary.get("total_topics", 0)
    min_bar = summary.get("min_bar") or {}

    lines = ["## Where things stand", ""]
    lines.append(f"`{bar(percent)}` **{percent}%** across {total} topics")
    lines.append("")
    lines.append(f"- Minimum bar: **{min_bar.get('met', 0)}/{min_bar.get('total', 0)}** topics at comfortable or better")

    if roadmap.get("target_date"):
        lines.append(f"- Target date: **{roadmap['target_date']}**")

    counts = roadmap.get("summary") or {}
    if counts.get("total"):
        parts = [
            f"{counts.get(key, 0)} {label}"
            for key, label in (
                ("done", "done"),
                ("on_track", "on track"),
                ("at_risk", "at risk"),
                ("overdue", "overdue"),
                ("blocked", "blocked"),
                ("planned", "planned"),
            )
            if counts.get(key)
        ]
        lines.append(f"- Milestones: {' · '.join(parts)}")

    forecast = velocity.get("forecast") or {}
    if forecast.get("available") and forecast.get("projected_date"):
        verdict = forecast.get("verdict", "unknown")
        delta = forecast.get("days_vs_target")
        suffix = ""
        if delta is not None:
            suffix = " (on target)" if delta == 0 else f" ({abs(delta)} days {'late' if delta > 0 else 'early'})"
        lines.append(f"- Projected completion: **{forecast['projected_date']}** — {verdict}{suffix}")
    else:
        lines.append(f"- Projected completion: _not enough history yet_ — {forecast.get('reason', 'no data')}")

    lines.append("")
    return lines


def _milestones(roadmap: dict, *, today: date) -> list[str]:
    milestones = roadmap.get("milestones") or []
    if not milestones:
        if not roadmap.get("exists"):
            return [
                "## Milestones",
                "",
                "_No roadmap yet._ Ask your agent to create one — it can call `set_milestone`.",
                "",
            ]
        return ["## Milestones", "", "_The roadmap has no milestones yet._", ""]

    lines = ["## Milestones", "", "| Milestone | Target | Progress | Done | Status |", "|---|---|---|---|---|"]
    for entry in milestones:
        progress = entry.get("progress") or {}
        percent = progress.get("percent", 0.0)
        state = _STATUS_LABEL.get(entry.get("derived_status", ""), entry.get("derived_status", ""))
        days = entry.get("days_remaining")
        target = entry.get("target") or "—"
        if days is not None and entry.get("derived_status") not in ("done",):
            target += f" ({_humanise_days(days)})"
        lines.append(
            f"| {entry.get('title', entry.get('id'))} | {target} | `{bar(percent, 14)}` {percent}% | "
            f"{progress.get('complete', 0)}/{progress.get('total', 0)} | {state} |"
        )
    lines.append("")

    # Call out anything actively going wrong, so it is not buried in the table.
    trouble = [e for e in milestones if e.get("derived_status") in ("overdue", "at-risk", "blocked")]
    if trouble:
        lines.append("### Needs attention")
        lines.append("")
        for entry in trouble:
            progress = entry.get("progress") or {}
            outstanding = max(progress.get("total", 0) - progress.get("complete", 0), 0)
            lines.append(
                f"- **{entry.get('title')}** — {_STATUS_LABEL.get(entry.get('derived_status'), '')}, "
                f"{outstanding} topic(s) outstanding, target {entry.get('target') or 'unset'}"
            )
        lines.append("")

    missing = [(e.get("title"), e.get("missing_topic_ids") or []) for e in milestones]
    missing = [(title, ids) for title, ids in missing if ids]
    if missing:
        lines.append("### Broken references")
        lines.append("")
        for title, ids in missing:
            lines.append(f"- **{title}** references unknown topic(s): {', '.join(ids)}")
        lines.append("")

    return lines


def _forecast(velocity: dict, roadmap: dict) -> list[str]:
    lines = ["## Pace", ""]
    if not velocity.get("has_data"):
        lines += ["_No progress events recorded yet._ Velocity appears once statuses start changing.", ""]
        return lines

    lines.append(
        f"- Recent rate: **{velocity.get('topics_per_week', 0)} topics/week** "
        f"({velocity.get('points_per_day', 0)} points/day over the last {velocity.get('window_days')} days)"
    )
    lines.append(
        f"- Recorded: {velocity.get('events_in_window', 0)} status change(s) in that window "
        f"across {velocity.get('observed_days', 0)} observed day(s)"
    )
    lines.append(f"- Remaining: **{velocity.get('remaining_points', 0)}** of {velocity.get('total_points', 0)} points")

    forecast = velocity.get("forecast") or {}
    required = forecast.get("required_points_per_day")
    if required is not None:
        lines.append(f"- Rate needed to hit {forecast.get('target_date')}: **{required} points/day**")
    if forecast.get("available"):
        lines.append(f"- Confidence: {forecast.get('confidence')} — {forecast.get('reason')}")
    else:
        lines.append(f"- No projection: {forecast.get('reason')}")

    lines.append("")
    return lines


def _skills(state_dict: dict) -> list[str]:
    skills = state_dict.get("skills") or []
    if not skills:
        return []

    lines = ["## Skills", "", "| # | Skill | Progress | Topics | Min bar |", "|---|---|---|---|---|"]
    for index, skill in enumerate(skills, start=1):
        progress = skill.get("progress") or {}
        percent = progress.get("percent", 0.0)
        lines.append(
            f"| {index} | {skill.get('name')} | `{bar(percent, 14)}` {percent}% | "
            f"{progress.get('total', 0)} | {progress.get('min_required_met', 0)}/{progress.get('min_required_total', 0)} |"
        )
    lines.append("")
    return lines


def _activity(events: list[Event]) -> list[str]:
    if not events:
        return ["## Recent activity", "", "_Nothing recorded yet._", ""]

    lines = ["## Recent activity", ""]
    for event in list(reversed(events))[:ACTIVITY_LIMIT]:
        note = f" — {event.note}" if event.note else ""
        lines.append(f"- `{event.ts}` {describe(event)}{note}")
    if len(events) > ACTIVITY_LIMIT:
        lines.append("")
        lines.append(f"_{len(events) - ACTIVITY_LIMIT} earlier event(s) in `data/history.jsonl`._")
    lines.append("")
    return lines


def _humanise_days(days: int) -> str:
    if days == 0:
        return "today"
    if days == 1:
        return "1 day left"
    if days > 1:
        return f"{days} days left"
    return f"{abs(days)} day{'s' if days < -1 else ''} overdue"


__all__ = ["render_roadmap_doc", "bar", "BANNER", "STATUSES"]
