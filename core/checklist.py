"""Granular checklist items inside a topic body.

A topic says *what* to learn; a checklist says *what to actually do*, in order.
Items are ordinary GFM task-list lines living in the topic's own markdown:

    ### Checklist
    - [x] Explain self-attention (QKV) from memory
    - [ ] Derive why decode is memory-bandwidth bound
    - [ ] Implement a toy attention head in numpy

Storing them inline rather than in a side-car file means the checkbox state
*is* the file — there is no second copy to fall out of sync, checking a box is
a one-line diff, and the list renders correctly in any markdown viewer.

Items are picked up from anywhere in the body and grouped by the ``###``
heading they sit under, so an existing section (say "NeetCode problems in this
section") becomes a working checklist the moment its bullets get ``[ ]``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .models import slugify

#: A GFM task-list line: optional indent, bullet, [ ] or [x], then text.
_ITEM_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<bullet>[-*+])[ \t]+\[(?P<mark>[ xX])\][ \t]+(?P<text>.*?)[ \t]*$")

_HEADING_RE = re.compile(r"^###[ \t]+(.+?)[ \t]*$")

#: Heading used when items are added to a topic that has no checklist yet.
DEFAULT_SECTION = "Checklist"

#: Ids are slugs of the item text, capped so they stay readable in tool calls.
_MAX_ID_LEN = 60


@dataclass
class ChecklistItem:
    """One task-list line."""

    id: str
    text: str
    checked: bool
    section: str
    line: int  # 0-based index into the topic body's lines

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "text": self.text, "checked": self.checked, "section": self.section}


@dataclass
class Checklist:
    """All items in one topic body, in document (i.e. learning) order."""

    items: list[ChecklistItem] = field(default_factory=list)

    def item(self, item_id: str) -> ChecklistItem | None:
        return next((i for i in self.items if i.id == item_id), None)

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def done(self) -> int:
        return sum(1 for item in self.items if item.checked)

    @property
    def percent(self) -> float:
        return round(100 * self.done / self.total, 1) if self.total else 0.0

    def sections(self) -> list[dict[str, Any]]:
        """Items grouped by heading, preserving first-appearance order."""
        grouped: list[dict[str, Any]] = []
        index: dict[str, dict[str, Any]] = {}
        for item in self.items:
            bucket = index.get(item.section)
            if bucket is None:
                bucket = {"heading": item.section, "items": []}
                index[item.section] = bucket
                grouped.append(bucket)
            bucket["items"].append(item.to_dict())
        return grouped

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "done": self.done,
            "percent": self.percent,
            "sections": self.sections(),
        }


def parse_checklist(body: str) -> Checklist:
    """Extract every task-list item from a topic body."""
    checklist = Checklist()
    section = ""
    used: dict[str, int] = {}

    for line_number, line in enumerate(body.splitlines()):
        heading = _HEADING_RE.match(line)
        if heading:
            section = heading.group(1).strip()
            continue

        match = _ITEM_RE.match(line)
        if not match:
            continue

        text = match.group("text").strip()
        item_id = _unique_id(text, used)
        checklist.items.append(
            ChecklistItem(
                id=item_id,
                text=text,
                checked=match.group("mark").lower() == "x",
                section=section or DEFAULT_SECTION,
                line=line_number,
            )
        )
    return checklist


def _unique_id(text: str, used: dict[str, int]) -> str:
    """Stable, readable id from the item text, de-duplicated within a topic."""
    base = slugify(text)[:_MAX_ID_LEN].strip("-") or "item"
    seen = used.get(base, 0)
    used[base] = seen + 1
    return base if seen == 0 else f"{base}-{seen + 1}"


def set_item(body: str, item_id: str, checked: bool) -> tuple[str, ChecklistItem] | None:
    """Return the body with one item toggled, plus the updated item.

    ``None`` when the id is not present. Only the checkbox mark is rewritten,
    so any trailing content on the line is preserved.
    """
    checklist = parse_checklist(body)
    item = checklist.item(item_id)
    if item is None:
        return None

    lines = body.splitlines()
    match = _ITEM_RE.match(lines[item.line])
    if match is None:  # pragma: no cover - parse and rewrite are in lockstep
        return None

    mark = "x" if checked else " "
    lines[item.line] = f"{match.group('indent')}{match.group('bullet')} [{mark}] {match.group('text')}"

    item.checked = checked
    return "\n".join(lines), item


def add_items(body: str, texts: list[str], *, section: str = DEFAULT_SECTION) -> tuple[str, list[str]]:
    """Append unchecked items under ``section``, creating it if absent.

    Returns the new body and the ids of the items actually added; texts that
    already exist in the topic are skipped so re-running is harmless.
    """
    existing = {item.text.strip().lower() for item in parse_checklist(body).items}
    fresh = []
    for text in texts:
        cleaned = " ".join(str(text).split()).strip()
        if cleaned and cleaned.lower() not in existing:
            fresh.append(cleaned)
            existing.add(cleaned.lower())
    if not fresh:
        return body, []

    lines = body.splitlines()
    headings = [(i, _HEADING_RE.match(line)) for i, line in enumerate(lines)]
    target_start = next(
        (i for i, match in headings if match and match.group(1).strip().lower() == section.strip().lower()),
        None,
    )

    new_lines = [f"- [ ] {text}" for text in fresh]

    if target_start is None:
        block = ([""] if lines and lines[-1].strip() else []) + [f"### {section}", *new_lines]
        lines.extend(block)
    else:
        # Insert at the end of that section, before the next ### heading.
        end = next((i for i, match in headings if match and i > target_start), len(lines))
        while end > target_start + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = new_lines

    body = "\n".join(lines)
    added = parse_checklist(body)
    ids = [item.id for item in added.items if item.text in fresh]
    return body, ids
