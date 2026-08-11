"""Parser, serialiser and progress derivation for ``data/roadmap.md``.

A milestone *references* topics and skills; it never stores their status. All
completion figures are derived from the live topics at read time, so a roadmap
can never drift out of sync with actual progress — the failure mode of every
hand-maintained plan.

    ---
    updated: 2026-08-10
    start_date: 2026-08-10
    target_date: 2026-09-08
    ---
    Optional intro prose.

    ## Week 1 — LLM & RAG foundations
    - id: w1-foundations
    - target: 2026-08-16
    - status: in-progress
    - skills: [llm-fundamentals, rag]
    - topics: [transformer-architecture, tokenization]

    Why this week matters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable

from .blocks import render_block, split_blocks
from .markdown import ParseError, join_frontmatter, split_frontmatter
from .models import MIN_BAR_STATUSES, STATUS_WEIGHTS, STATUSES, Issue, Topic, coverage, slugify

ROADMAP_FILE = "data/roadmap.md"

#: Explicit, agent-set milestone states.
MILESTONE_STATUSES = ("planned", "in-progress", "done", "blocked")

#: Canonical meta key order inside a milestone block.
MILESTONE_META_KEYS = ("id", "target", "status", "skills", "topics")

#: How close to its target a milestone may be, per remaining topic, before it
#: is called at-risk. Roughly "you need more than a day per outstanding topic".
_AT_RISK_DAYS_PER_TOPIC = 1.0


@dataclass
class Milestone:
    """One roadmap milestone."""

    id: str
    title: str
    target: str | None = None
    status: str = "planned"
    skills: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    description: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def sort_key(self) -> tuple[int, str, str]:
        # Undated milestones sink below dated ones but keep a stable order.
        return (0, self.target, self.id) if self.target else (1, "", self.id)


@dataclass
class Roadmap:
    """The parsed ``roadmap.md``."""

    exists: bool = False
    updated: str | None = None
    start_date: str | None = None
    target_date: str | None = None
    notes: str = ""
    milestones: list[Milestone] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def milestone(self, milestone_id: str) -> Milestone | None:
        return next((m for m in self.milestones if m.id == milestone_id), None)


# ----------------------------------------------------------------------
# Parsing / serialising
# ----------------------------------------------------------------------


def parse_roadmap(text: str) -> tuple[Roadmap, list[Issue]]:
    """Parse roadmap markdown. Never raises — problems come back as issues."""
    issues: list[Issue] = []
    try:
        meta, body = split_frontmatter(text)
    except ParseError as exc:
        return Roadmap(exists=True), [Issue("error", f"{ROADMAP_FILE}: {exc}", ROADMAP_FILE)]

    preamble, blocks = split_blocks(body)
    roadmap = Roadmap(
        exists=True,
        updated=_as_str(meta.pop("updated", None)),
        start_date=_as_str(meta.pop("start_date", None)),
        target_date=_as_str(meta.pop("target_date", None)),
        notes=preamble,
        extra=meta,
    )

    seen: set[str] = set()
    for block in blocks:
        fields = dict(block.meta)
        for key in block.duplicate_keys:
            issues.append(Issue("warning", f"milestone '{block.title}': duplicate meta key '{key}'", ROADMAP_FILE))

        if not block.saw_meta:
            issues.append(
                Issue("error", f"milestone '{block.title}': no meta block — expected '- key: value' lines", ROADMAP_FILE)
            )

        milestone_id = fields.pop("id", None)
        if not isinstance(milestone_id, str) or not milestone_id.strip():
            milestone_id = slugify(block.title)
            if block.saw_meta:
                issues.append(
                    Issue("warning", f"milestone '{block.title}': missing 'id', derived '{milestone_id}'", ROADMAP_FILE)
                )
        milestone_id = milestone_id.strip()
        if milestone_id in seen:
            issues.append(Issue("error", f"duplicate milestone id '{milestone_id}'", ROADMAP_FILE))
        seen.add(milestone_id)

        status = fields.pop("status", "planned")
        if status not in MILESTONE_STATUSES:
            issues.append(
                Issue(
                    "error",
                    f"milestone '{milestone_id}': unknown status {status!r} "
                    f"(expected {', '.join(MILESTONE_STATUSES)})",
                    ROADMAP_FILE,
                )
            )

        target = _as_str(fields.pop("target", None))
        if target and not _parse_date(target):
            issues.append(
                Issue("error", f"milestone '{milestone_id}': target '{target}' is not a YYYY-MM-DD date", ROADMAP_FILE)
            )
            target = None

        roadmap.milestones.append(
            Milestone(
                id=milestone_id,
                title=block.title,
                target=target,
                status=str(status),
                skills=_as_list(fields.pop("skills", [])),
                topics=_as_list(fields.pop("topics", [])),
                description=block.body,
                extra=fields,
            )
        )

    if roadmap.start_date and not _parse_date(roadmap.start_date):
        issues.append(Issue("error", f"{ROADMAP_FILE}: start_date is not a YYYY-MM-DD date", ROADMAP_FILE))
    if roadmap.target_date and not _parse_date(roadmap.target_date):
        issues.append(Issue("error", f"{ROADMAP_FILE}: target_date is not a YYYY-MM-DD date", ROADMAP_FILE))

    roadmap.milestones.sort(key=Milestone.sort_key)
    return roadmap, issues


def serialize_roadmap(roadmap: Roadmap) -> str:
    """Render a roadmap back to markdown, normalised and in target-date order."""
    front: dict[str, Any] = {"updated": roadmap.updated}
    if roadmap.start_date:
        front["start_date"] = roadmap.start_date
    if roadmap.target_date:
        front["target_date"] = roadmap.target_date
    front.update(roadmap.extra)

    chunks = [roadmap.notes.strip("\n")] if roadmap.notes.strip() else []
    for milestone in sorted(roadmap.milestones, key=Milestone.sort_key):
        chunks.append(
            render_block(
                milestone.title,
                {
                    "id": milestone.id,
                    "target": milestone.target,
                    "status": milestone.status,
                    "skills": milestone.skills,
                    "topics": milestone.topics,
                    **milestone.extra,
                },
                milestone.description,
                order=MILESTONE_META_KEYS,
            )
        )

    return join_frontmatter(front, "\n\n".join(chunks) + "\n" if chunks else "\n")


def load_roadmap(root: Path) -> tuple[Roadmap, list[Issue]]:
    path = root / ROADMAP_FILE
    if not path.is_file():
        return Roadmap(exists=False), []
    return parse_roadmap(path.read_text(encoding="utf-8"))


# ----------------------------------------------------------------------
# Derivation
# ----------------------------------------------------------------------


def resolve_topics(milestone: Milestone, all_topics: list[Topic]) -> tuple[list[Topic], list[str]]:
    """Expand a milestone's ``skills`` and ``topics`` into concrete topics.

    Returns the topics (de-duplicated, in skill/priority order) plus any
    referenced topic ids that no longer exist.
    """
    wanted_skills = set(milestone.skills)
    wanted_topics = set(milestone.topics)

    resolved: list[Topic] = []
    seen: set[str] = set()
    for topic in all_topics:
        if topic.id in seen:
            continue
        if topic.skill_id in wanted_skills or topic.id in wanted_topics:
            resolved.append(topic)
            seen.add(topic.id)

    missing = sorted(wanted_topics - {t.id for t in all_topics})
    return resolved, missing


def derive_milestone(
    milestone: Milestone,
    all_topics: list[Topic],
    *,
    today: date,
) -> dict[str, Any]:
    """Compute a milestone's live progress and schedule verdict."""
    topics, missing = resolve_topics(milestone, all_topics)

    counts = {status: 0 for status in STATUSES}
    for topic in topics:
        if topic.status in counts:
            counts[topic.status] += 1

    total = len(topics)
    complete = sum(1 for t in topics if t.status in MIN_BAR_STATUSES)
    earned = sum(STATUS_WEIGHTS.get(t.status, 0.0) for t in topics)
    percent = round(100 * earned / total, 1) if total else 0.0

    target = _parse_date(milestone.target) if milestone.target else None
    days_remaining = (target - today).days if target else None

    return {
        "id": milestone.id,
        "title": milestone.title,
        "target": milestone.target,
        "status": milestone.status,
        "derived_status": _derive_status(milestone, total, complete, days_remaining),
        "description_md": milestone.description.strip("\n"),
        "days_remaining": days_remaining,
        "skill_ids": list(milestone.skills),
        "topic_ids": list(milestone.topics),
        "missing_topic_ids": missing,
        "progress": {"percent": percent, "total": total, "complete": complete, "counts": counts},
        "coverage": coverage(topics),
        "topics": [
            {
                "id": t.id,
                "title": t.title,
                "skill_id": t.skill_id,
                "skill_name": t.skill_name,
                "status": t.status,
                "min_required": t.min_required,
                "focus": t.focus,
                "checklist": t.checklist.to_dict(),
                "needs_breakdown": t.needs_breakdown,
                "needs_evidence": t.needs_evidence,
            }
            for t in topics
        ],
    }


def _derive_status(milestone: Milestone, total: int, complete: int, days_remaining: int | None) -> str:
    """Schedule verdict, derived from real topic state rather than declared."""
    if milestone.status == "blocked":
        return "blocked"
    if total > 0 and complete >= total:
        return "done"
    if milestone.status == "done":
        # Declared done but the topics disagree — trust the topics.
        return "at-risk" if total else "done"
    if days_remaining is None:
        return "planned" if milestone.status == "planned" else "on-track"
    if days_remaining < 0:
        return "overdue"

    remaining = max(total - complete, 0)
    if remaining and days_remaining < remaining * _AT_RISK_DAYS_PER_TOPIC:
        return "at-risk"
    return "on-track"


def derive_roadmap(roadmap: Roadmap, all_topics: list[Topic], *, today: date) -> dict[str, Any]:
    """The full roadmap payload served to the UI and the agent."""
    milestones = [derive_milestone(m, all_topics, today=today) for m in roadmap.milestones]

    summary = {"total": len(milestones), "done": 0, "on_track": 0, "at_risk": 0, "overdue": 0, "blocked": 0, "planned": 0}
    for entry in milestones:
        key = entry["derived_status"].replace("-", "_")
        if key in summary:
            summary[key] += 1

    return {
        "exists": roadmap.exists,
        "updated": roadmap.updated,
        "start_date": roadmap.start_date,
        "target_date": roadmap.target_date,
        "notes_md": roadmap.notes.strip("\n"),
        "summary": summary,
        "milestones": milestones,
    }


def validate_roadmap(roadmap: Roadmap, all_topics: list[Topic], skill_ids: Iterable[str]) -> list[Issue]:
    """Cross-check milestone references against the rest of the repo."""
    issues: list[Issue] = []
    known_topics = {t.id for t in all_topics}
    known_skills = set(skill_ids)

    for milestone in roadmap.milestones:
        for topic_id in milestone.topics:
            if topic_id not in known_topics:
                issues.append(
                    Issue("warning", f"milestone '{milestone.id}' references unknown topic '{topic_id}'", ROADMAP_FILE)
                )
        for skill_id in milestone.skills:
            if skill_id not in known_skills:
                issues.append(
                    Issue("warning", f"milestone '{milestone.id}' references unknown skill '{skill_id}'", ROADMAP_FILE)
                )
        if not milestone.topics and not milestone.skills:
            issues.append(
                Issue("warning", f"milestone '{milestone.id}' references no topics or skills — it can never progress", ROADMAP_FILE)
            )

    if roadmap.exists:
        covered: set[str] = set()
        for milestone in roadmap.milestones:
            resolved, _ = resolve_topics(milestone, all_topics)
            covered |= {t.id for t in resolved}
        uncovered = known_topics - covered
        if uncovered:
            issues.append(
                Issue(
                    "warning",
                    f"{len(uncovered)} topic(s) are not covered by any milestone",
                    ROADMAP_FILE,
                )
            )

    return issues


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _as_str(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def _as_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def add_days(value: date, days: int) -> date:
    return value + timedelta(days=days)
