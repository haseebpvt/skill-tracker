"""Parsing and serialising ``topics.md``."""

from __future__ import annotations

import pytest

from core.models import Topic
from core.topics import append_log_entry, parse_topics, serialize_topics

SAMPLE = """\
## A topic
- id: a-topic
- status: comfortable
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-01
- evidence: [raw/jd/x.md, raw/research/y.md]

### What "enough" looks like
- Criterion one

### Notes / log
- 2026-08-01: did a thing
"""


def test_parses_meta_block():
    parsed, issues = parse_topics(SAMPLE, skill_id="s")
    assert not issues
    topic = parsed.topics[0]
    assert topic.id == "a-topic"
    assert topic.title == "A topic"
    assert topic.status == "comfortable"
    assert topic.priority == 3
    assert topic.min_required is True
    assert topic.focus is False
    assert topic.updated == "2026-08-01"
    assert topic.evidence == ["raw/jd/x.md", "raw/research/y.md"]


def test_extracts_named_sections():
    parsed, _ = parse_topics(SAMPLE, skill_id="s")
    topic = parsed.topics[0]
    assert "Criterion one" in topic.enough_md
    assert "did a thing" in topic.log_md


def test_round_trip_is_byte_stable():
    parsed, _ = parse_topics(SAMPLE, skill_id="s")
    once = serialize_topics(parsed)
    twice = serialize_topics(parse_topics(once, skill_id="s")[0])
    assert once == twice
    assert once == SAMPLE


def test_unknown_meta_keys_survive_round_trip():
    text = SAMPLE.replace("- updated: 2026-08-01", "- updated: 2026-08-01\n- reviewer: someone")
    parsed, _ = parse_topics(text, skill_id="s")
    assert parsed.topics[0].extra["reviewer"] == "someone"
    assert "- reviewer: someone" in serialize_topics(parsed)


def test_preamble_survives_round_trip():
    text = "<!-- keep me -->\n\n" + SAMPLE
    parsed, _ = parse_topics(text, skill_id="s")
    assert "<!-- keep me -->" in serialize_topics(parsed)


def test_missing_optional_fields_get_defaults():
    parsed, issues = parse_topics("## Bare\n- id: bare\n", skill_id="s")
    topic = parsed.topics[0]
    assert topic.status == "not-started"
    assert topic.focus is False
    assert topic.min_required is False
    assert topic.evidence == []
    assert not [i for i in issues if i.level == "error"]


def test_missing_meta_block_is_an_error_not_a_crash():
    parsed, issues = parse_topics("## No meta\n\nJust prose.\n", skill_id="s")
    assert parsed.topics[0].id == "no-meta"  # derived from the title
    assert any(i.level == "error" and "no meta block" in i.message for i in issues)


@pytest.mark.parametrize(
    "line,fragment",
    [
        ("- priority: high", "priority must be an integer"),
        ("- min_required: yes-please", "min_required must be true or false"),
    ],
)
def test_bad_field_types_are_reported(line, fragment):
    text = f"## T\n- id: t\n{line}\n"
    _, issues = parse_topics(text, skill_id="s")
    assert any(fragment in i.message for i in issues)


def test_log_entry_appends_to_existing_section():
    parsed, _ = parse_topics(SAMPLE, skill_id="s")
    topic = parsed.topics[0]
    append_log_entry(topic, "second thing", date="2026-08-09")
    assert topic.log_md.splitlines() == [
        "- 2026-08-01: did a thing",
        "- 2026-08-09: second thing",
    ]


def test_log_entry_creates_section_when_absent():
    topic = Topic(id="t", title="T", body='### What "enough" looks like\n- x')
    append_log_entry(topic, "first note", date="2026-08-09")
    assert "### Notes / log" in topic.body
    assert topic.log_md == "- 2026-08-09: first note"
    assert 'What "enough" looks like' in topic.body  # existing content untouched
