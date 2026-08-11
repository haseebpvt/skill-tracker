"""Data model for the repo. Plain dataclasses, all JSON-encodable via ``to_dict``."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

#: The only legal topic statuses, in ascending order of proficiency.
STATUSES: tuple[str, ...] = ("not-started", "learning", "comfortable", "strong")

#: Fractional credit each status contributes to a progress percentage.
STATUS_WEIGHTS: dict[str, float] = {
    "not-started": 0.0,
    "learning": 1 / 3,
    "comfortable": 2 / 3,
    "strong": 1.0,
}

#: Statuses that count as "meets the minimum bar".
MIN_BAR_STATUSES: frozenset[str] = frozenset({"comfortable", "strong"})

#: Canonical order of the keys in a topic's meta block. Unknown keys are kept
#: and written after these, so hand-added fields survive a round trip.
TOPIC_META_KEYS: tuple[str, ...] = (
    "id",
    "status",
    "priority",
    "min_required",
    "focus",
    "updated",
    "evidence",
)

_ENOUGH_HEADINGS = ("what \"enough\" looks like", "what enough looks like", "what 'enough' looks like")
_LOG_HEADINGS = ("notes / log", "notes/log", "notes", "log")

_SECTION_RE = re.compile(r"^###[ \t]+(.+?)[ \t]*$", re.MULTILINE)


def slugify(text: str) -> str:
    """Turn a human title into a stable kebab-case id."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "topic"


def split_sections(body: str) -> dict[str, str]:
    """Split a topic body into its ``###`` subsections, keyed by heading."""
    sections: dict[str, str] = {}
    matches = list(_SECTION_RE.finditer(body))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[match.group(1).strip()] = body[match.end() : end].strip("\n")
    return sections


def _find_section(sections: dict[str, str], candidates: tuple[str, ...]) -> str:
    for heading, content in sections.items():
        if heading.strip().lower() in candidates:
            return content
    return ""


@dataclass
class Topic:
    """One topic inside a skill."""

    id: str
    title: str
    status: str = "not-started"
    priority: int = 999
    min_required: bool = False
    focus: bool = False
    updated: str | None = None
    evidence: list[str] = field(default_factory=list)
    body: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    # Set by the loader; not stored in the file.
    skill_id: str = ""
    skill_name: str = ""
    source_file: str = ""

    @property
    def sections(self) -> dict[str, str]:
        return split_sections(self.body)

    @property
    def checklist(self):
        """The granular items to work through, parsed from the body."""
        from .checklist import parse_checklist

        return parse_checklist(self.body)

    @property
    def needs_breakdown(self) -> bool:
        """No concrete items yet — "learn X" with nothing actionable under it."""
        return self.checklist.total == 0

    @property
    def needs_evidence(self) -> bool:
        """Nothing in evidence/ backs this topic, so its criteria are unsourced."""
        return not self.evidence

    @property
    def enough_md(self) -> str:
        return _find_section(self.sections, _ENOUGH_HEADINGS)

    @property
    def log_md(self) -> str:
        return _find_section(self.sections, _LOG_HEADINGS)

    @property
    def weight(self) -> float:
        return STATUS_WEIGHTS.get(self.status, 0.0)

    @property
    def meets_min_bar(self) -> bool:
        return self.status in MIN_BAR_STATUSES

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "min_required": self.min_required,
            "focus": self.focus,
            "updated": self.updated,
            "evidence": list(self.evidence),
            "enough_md": self.enough_md,
            "log_md": self.log_md,
            "body_md": self.body.strip("\n"),
            "checklist": self.checklist.to_dict(),
            "needs_breakdown": self.needs_breakdown,
            "needs_evidence": self.needs_evidence,
            "extra": dict(self.extra),
        }


def coverage(topics: list["Topic"]) -> dict[str, Any]:
    """Checklist coverage across a set of topics.

    Deliberately separate from the status-weighted percentage: coverage says
    how much of the work you have *ticked off*, status says how well you were
    judged to know it. Ticking every box does not make you `comfortable`.
    """
    total = done = needs_breakdown = needs_evidence = 0
    for topic in topics:
        items = topic.checklist
        total += items.total
        done += items.done
        if items.total == 0:
            needs_breakdown += 1
        if not topic.evidence:
            needs_evidence += 1

    return {
        "total": total,
        "done": done,
        "percent": round(100 * done / total, 1) if total else 0.0,
        "topics_needing_breakdown": needs_breakdown,
        "topics_needing_evidence": needs_evidence,
    }


@dataclass
class Skill:
    """One skill folder: ``_skill.md`` plus any number of topic files."""

    id: str
    name: str
    priority: int = 999
    updated: str | None = None
    description: str = ""
    topics: list[Topic] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def topic(self, topic_id: str) -> Topic | None:
        return next((t for t in self.topics if t.id == topic_id), None)

    def progress(self, topics: list[Topic] | None = None) -> dict[str, Any]:
        items = self.topics if topics is None else topics
        counts = {status: 0 for status in STATUSES}
        for topic in items:
            if topic.status in counts:
                counts[topic.status] += 1
        total = len(items)
        earned = sum(topic.weight for topic in items)
        min_required = [t for t in items if t.min_required]
        return {
            "percent": round(100 * earned / total, 1) if total else 0.0,
            "total": total,
            "counts": counts,
            "min_required_total": len(min_required),
            "min_required_met": sum(1 for t in min_required if t.meets_min_bar),
            "coverage": coverage(items),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "updated": self.updated,
            "description_md": self.description.strip("\n"),
            "progress": self.progress(),
            "topics": [topic.to_dict() for topic in self.topics],
            "extra": dict(self.extra),
        }


@dataclass
class Role:
    """``data/role.md``."""

    role: str = ""
    level: str = ""
    updated: str | None = None
    skill_order: list[str] = field(default_factory=list)
    notes: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "level": self.level,
            "updated": self.updated,
            "skill_order": list(self.skill_order),
            "notes_md": self.notes.strip("\n"),
            "extra": dict(self.extra),
        }


@dataclass
class EvidenceFile:
    """One file under ``evidence/raw/``."""

    path: str  # relative to evidence/, e.g. "raw/jd/acme.md"
    source: str = ""
    url: str = ""
    added: str | None = None
    sha256: str = ""
    body: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "source": self.source,
            "url": self.url,
            "added": self.added,
            "hash": self.sha256,
        }


@dataclass
class Conclusions:
    """``evidence/CONCLUSIONS.md``."""

    exists: bool = False
    updated: str | None = None
    considered: list[dict[str, str]] = field(default_factory=list)
    content: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "exists": self.exists,
            "updated": self.updated,
            "content_md": self.content.strip("\n"),
            "sections": [m.group(1).strip() for m in re.finditer(r"^##[ \t]+(.+?)$", self.content, re.MULTILINE)],
            "evidence_files_considered": list(self.considered),
        }


@dataclass
class Issue:
    """A validation error or warning, surfaced in the UI rather than raised."""

    level: str  # "error" | "warning"
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"level": self.level, "message": self.message, "path": self.path}
