"""Parser and serialiser for ``topics.md``.

Format (settled — see MASTER.md §"File formats"): each topic is an ``##``
heading followed immediately by a **dash-list meta block**, then free markdown
with ``###`` subsections.

    ## LangGraph state machines
    - id: langgraph-state-machines
    - status: learning
    - priority: 1
    - min_required: true
    - focus: false
    - updated: 2026-08-07
    - evidence: [jd/acme-2026-07.md]

    ### What "enough" looks like
    - ...

The parser is strict about the *shape* (meta lines must be the first non-blank
lines under the heading) but tolerant about *content*: missing optional fields
get defaults and anything suspicious is reported as an :class:`Issue` rather
than raised, so the viewer shows errors instead of crashing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .blocks import Block, render_block, split_blocks
from .models import TOPIC_META_KEYS, Issue, Topic, slugify

_BOOL_KEYS = ("min_required", "focus")


@dataclass
class TopicFile:
    """One parsed ``*.md`` topics file inside a skill folder."""

    path: str
    preamble: str = ""
    topics: list[Topic] = field(default_factory=list)


def parse_topics(text: str, *, path: str = "topics.md", skill_id: str = "") -> tuple[TopicFile, list[Issue]]:
    """Parse a topics file into topics plus any issues found."""
    issues: list[Issue] = []
    preamble, blocks = split_blocks(text)
    parsed = TopicFile(path=path, preamble=preamble)

    for block in blocks:
        topic, topic_issues = _parse_one(block, path=path, skill_id=skill_id)
        parsed.topics.append(topic)
        issues.extend(topic_issues)

    return parsed, issues


def _parse_one(block: Block, *, path: str, skill_id: str) -> tuple[Topic, list[Issue]]:
    title, meta, body, saw_meta = block.title, dict(block.meta), block.body, block.saw_meta
    issues: list[Issue] = [
        Issue("warning", f"topic '{title}': duplicate meta key '{key}'", path) for key in block.duplicate_keys
    ]

    if not saw_meta:
        issues.append(
            Issue("error", f"topic '{title}': no meta block — expected '- key: value' lines under the heading", path)
        )

    topic_id = meta.pop("id", None)
    if not isinstance(topic_id, str) or not topic_id.strip():
        topic_id = slugify(title)
        if saw_meta:
            issues.append(Issue("warning", f"topic '{title}': missing 'id', derived '{topic_id}'", path))
    topic_id = topic_id.strip()

    status = meta.pop("status", "not-started")
    if not isinstance(status, str) or not status:
        status = "not-started"

    priority = meta.pop("priority", 999)
    if isinstance(priority, bool) or not isinstance(priority, int):
        issues.append(Issue("error", f"topic '{topic_id}': priority must be an integer, got {priority!r}", path))
        priority = 999

    flags: dict[str, bool] = {}
    for key in _BOOL_KEYS:
        value = meta.pop(key, False)
        if not isinstance(value, bool):
            issues.append(Issue("error", f"topic '{topic_id}': {key} must be true or false, got {value!r}", path))
            value = bool(value)
        flags[key] = value

    updated = meta.pop("updated", None)
    if updated is not None and not isinstance(updated, str):
        updated = str(updated)

    evidence = meta.pop("evidence", [])
    if isinstance(evidence, str):
        evidence = [part.strip() for part in evidence.split(",") if part.strip()]
    elif not isinstance(evidence, list):
        issues.append(Issue("error", f"topic '{topic_id}': evidence must be a list, got {evidence!r}", path))
        evidence = []
    evidence = [str(item) for item in evidence]

    topic = Topic(
        id=topic_id,
        title=title,
        status=status,
        priority=priority,
        min_required=flags["min_required"],
        focus=flags["focus"],
        updated=updated,
        evidence=evidence,
        body=body,
        extra=dict(meta),
        skill_id=skill_id,
        source_file=path,
    )
    return topic, issues


def serialize_topics(parsed: TopicFile) -> str:
    """Render a :class:`TopicFile` back to markdown.

    This is a normalising formatter: every topic is written with the full
    canonical meta block in :data:`TOPIC_META_KEYS` order, so a file written
    twice is byte-identical.
    """
    chunks: list[str] = []
    if parsed.preamble.strip():
        chunks.append(parsed.preamble.strip("\n"))

    for topic in parsed.topics:
        chunks.append(serialize_topic(topic))

    return "\n\n".join(chunks).strip("\n") + "\n"


def serialize_topic(topic: Topic) -> str:
    """Render a single topic section (heading + meta block + body)."""
    meta = {
        "id": topic.id,
        "status": topic.status,
        "priority": topic.priority,
        "min_required": topic.min_required,
        "focus": topic.focus,
        # render_block drops None and empty lists, so these vanish when unset.
        "updated": topic.updated or None,
        "evidence": topic.evidence,
        **topic.extra,
    }
    return render_block(topic.title, meta, topic.body, order=TOPIC_META_KEYS)


def append_log_entry(topic: Topic, note: str, *, date: str) -> None:
    """Append ``- <date>: <note>`` to the topic's "Notes / log" section.

    Creates the section if it does not exist yet, so the log is always in the
    same place regardless of how the topic was originally written.
    """
    note = note.strip()
    if not note:
        return

    entry = f"- {date}: {note}"
    body = topic.body.strip("\n")

    # Locate an existing log heading and append to the end of that section.
    headings = list(re.finditer(r"^###[ \t]+(.+?)[ \t]*$", body, re.MULTILINE))
    for index, heading in enumerate(headings):
        if heading.group(1).strip().lower() in ("notes / log", "notes/log", "notes", "log"):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
            section = body[heading.end() : end].rstrip("\n")
            rebuilt = body[: heading.end()] + section + "\n" + entry + "\n" + ("\n" + body[end:].lstrip("\n") if body[end:].strip() else "")
            topic.body = rebuilt.rstrip("\n")
            return

    topic.body = (body + "\n\n" if body else "") + "### Notes / log\n" + entry
