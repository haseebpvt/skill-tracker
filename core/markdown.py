"""YAML frontmatter and scalar (de)serialisation helpers.

Kept deliberately small: the goal is round-trippable, git-diffable markdown,
not a general-purpose YAML layer.
"""

from __future__ import annotations

import datetime as _dt
import re
from typing import Any

import yaml

_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.DOTALL)


class ParseError(ValueError):
    """Raised when a file cannot be parsed at all."""


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split ``text`` into (frontmatter dict, body).

    A file with no frontmatter yields an empty dict and the whole text as body.
    """
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    raw = match.group(1)
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ParseError(f"invalid YAML frontmatter: {exc}") from exc

    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ParseError("frontmatter must be a YAML mapping")

    return normalize(loaded), text[match.end() :]


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _dateify(value: Any) -> Any:
    """Turn ``YYYY-MM-DD`` strings back into dates before dumping.

    PyYAML quotes a date-shaped *string* to preserve its type. Handing it a real
    ``date`` instead makes it emit ``updated: 2026-08-09`` bare, so files written
    by the agent look identical to hand-written ones. Reading is unaffected —
    :func:`normalize` turns it straight back into a string.
    """
    if isinstance(value, dict):
        return {k: _dateify(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_dateify(v) for v in value]
    if isinstance(value, str) and _DATE_RE.match(value):
        try:
            return _dt.date.fromisoformat(value)
        except ValueError:
            return value
    return value


def join_frontmatter(data: dict[str, Any], body: str) -> str:
    """Inverse of :func:`split_frontmatter`."""
    dumped = yaml.safe_dump(
        _dateify(normalize(data)),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).rstrip("\n")
    body = body.lstrip("\n")
    return f"---\n{dumped}\n---\n\n{body}".rstrip("\n") + "\n"


def normalize(value: Any) -> Any:
    """Convert YAML-native types into JSON-safe ones.

    Mainly this turns ``date``/``datetime`` (which PyYAML produces for bare
    ``2026-08-09``) into ISO strings so the whole model stays JSON-encodable.
    """
    if isinstance(value, dict):
        return {str(k): normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(v) for v in value]
    if isinstance(value, _dt.datetime):
        return value.date().isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    return value


def parse_scalar(raw: str) -> Any:
    """Parse one ``key: value`` value from a topic meta line.

    Uses YAML so that ``true``, ``3``, ``[a, b]`` and ``2026-08-09`` all behave
    the way a reader would expect. Anything YAML chokes on is kept as a string.
    """
    raw = raw.strip()
    if raw == "":
        return ""
    try:
        return normalize(yaml.safe_load(raw))
    except yaml.YAMLError:
        return raw


def format_scalar(value: Any) -> str:
    """Render a value for a topic meta line (inverse of :func:`parse_scalar`)."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(format_scalar(v) for v in value) + "]"
    if isinstance(value, (int, float)):
        return str(value)

    text = str(value)
    # Round-trip guard: if re-reading the bare text would not give back the
    # same string, quote it.
    if text != "" and parse_scalar(text) != text:
        return yaml.safe_dump(text, default_flow_style=True).strip().rstrip("\n...").strip()
    return text


def today() -> str:
    """Today's date as ``YYYY-MM-DD``. Single place to stub in tests."""
    return _dt.date.today().isoformat()
