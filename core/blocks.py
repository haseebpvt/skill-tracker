"""The generic ``## heading`` + dash-list meta block format.

Both ``topics.md`` and ``roadmap.md`` use the same shape:

    ## Human readable title
    - key: value
    - other: value

    free markdown body with ### subsections

This module knows only about that shape. Field names, defaults and coercion
are the caller's business (see :mod:`core.topics` and :mod:`core.roadmap`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .markdown import format_scalar, parse_scalar

_HEADING_RE = re.compile(r"^##[ \t]+(?!#)(.+?)[ \t]*$")
_META_RE = re.compile(r"^-[ \t]+([A-Za-z_][A-Za-z0-9_-]*)[ \t]*:[ \t]?(.*)$")


@dataclass
class Block:
    """One ``##`` section: its title, parsed meta block and remaining body."""

    title: str
    meta: dict[str, Any] = field(default_factory=dict)
    body: str = ""
    saw_meta: bool = False
    duplicate_keys: list[str] = field(default_factory=list)


def split_blocks(text: str) -> tuple[str, list[Block]]:
    """Split a document into (preamble, blocks).

    Meta lines must be the first non-blank lines under the heading; the first
    line that is not ``- key: value`` ends the meta block and starts the body.
    """
    lines = text.splitlines()
    heading_indexes = [i for i, line in enumerate(lines) if _HEADING_RE.match(line)]
    preamble_end = heading_indexes[0] if heading_indexes else len(lines)
    preamble = "\n".join(lines[:preamble_end]).strip("\n")

    blocks: list[Block] = []
    for position, start in enumerate(heading_indexes):
        end = heading_indexes[position + 1] if position + 1 < len(heading_indexes) else len(lines)
        title = _HEADING_RE.match(lines[start]).group(1).strip()
        blocks.append(_parse_block(title, lines[start + 1 : end]))

    return preamble, blocks


def _parse_block(title: str, lines: list[str]) -> Block:
    cursor = 0
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1

    meta: dict[str, Any] = {}
    duplicates: list[str] = []
    saw_meta = False
    while cursor < len(lines):
        match = _META_RE.match(lines[cursor])
        if not match:
            break
        saw_meta = True
        key, raw = match.group(1), match.group(2)
        if key in meta:
            duplicates.append(key)
        meta[key] = parse_scalar(raw)
        cursor += 1

    return Block(
        title=title,
        meta=meta,
        body="\n".join(lines[cursor:]).strip("\n"),
        saw_meta=saw_meta,
        duplicate_keys=duplicates,
    )


def render_block(title: str, meta: dict[str, Any], body: str, *, order: tuple[str, ...] = ()) -> str:
    """Render one block. Keys in ``order`` come first; the rest follow as given.

    A key whose value is ``None`` or an empty list is omitted, so optional
    fields do not litter the file.
    """
    keys = [k for k in order if k in meta] + [k for k in meta if k not in order]

    meta_lines = []
    for key in keys:
        value = meta[key]
        if value is None or (isinstance(value, (list, tuple)) and not value):
            continue
        meta_lines.append(f"- {key}: {format_scalar(value)}")

    section = f"## {title}\n" + "\n".join(meta_lines)
    body = body.strip("\n")
    if body:
        section += "\n\n" + body
    return section
