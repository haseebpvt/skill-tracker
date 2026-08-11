"""Checklist parsing, toggling and coverage."""

from __future__ import annotations

import pytest

from core.checklist import add_items, parse_checklist, set_item
from core.models import coverage
from core.repo import Repo, RepoError

BODY = '''### What "enough" looks like
- Can explain it

### Checklist
- [x] Read the paper
- [ ] Implement a toy version
- [ ] Explain it to someone

### Notes / log
- 2026-08-01: started
'''


def test_parses_items_in_document_order():
    checklist = parse_checklist(BODY)
    assert [i.text for i in checklist.items] == [
        "Read the paper",
        "Implement a toy version",
        "Explain it to someone",
    ]


def test_counts_and_percent():
    checklist = parse_checklist(BODY)
    assert (checklist.total, checklist.done) == (3, 1)
    assert checklist.percent == 33.3


def test_plain_bullets_are_not_items():
    """Only task-list syntax counts, so 'what enough looks like' is not a checklist."""
    assert parse_checklist('### What "enough" looks like\n- Can explain it\n').total == 0


def test_items_are_grouped_by_their_heading():
    body = "### Alpha\n- [ ] one\n\n### Beta\n- [ ] two\n- [ ] three\n"
    sections = parse_checklist(body).sections()
    assert [s["heading"] for s in sections] == ["Alpha", "Beta"]
    assert len(sections[1]["items"]) == 2


def test_ids_are_stable_slugs_of_the_text():
    assert parse_checklist("- [ ] Implement a toy version\n").items[0].id == "implement-a-toy-version"


def test_duplicate_texts_get_distinct_ids():
    ids = [i.id for i in parse_checklist("- [ ] Same\n- [ ] Same\n").items]
    assert ids == ["same", "same-2"]


@pytest.mark.parametrize("bullet", ["-", "*", "+"])
def test_accepts_any_bullet_marker(bullet):
    assert parse_checklist(f"{bullet} [ ] item\n").total == 1


def test_accepts_capital_x():
    assert parse_checklist("- [X] done\n").items[0].checked is True


def test_indented_items_are_kept():
    assert parse_checklist("  - [ ] nested\n").total == 1


# ----------------------------------------------------------------------
# Toggling
# ----------------------------------------------------------------------


def test_set_item_rewrites_only_the_mark():
    body, item = set_item(BODY, "implement-a-toy-version", True)
    assert item.checked is True
    assert "- [x] Implement a toy version" in body
    # Neighbours untouched.
    assert "- [x] Read the paper" in body
    assert "- [ ] Explain it to someone" in body


def test_set_item_can_untick():
    body, _ = set_item(BODY, "read-the-paper", False)
    assert "- [ ] Read the paper" in body


def test_set_item_preserves_indentation_and_bullet():
    body, _ = set_item("  * [ ] nested item\n", "nested-item", True)
    assert body == "  * [x] nested item"


def test_set_item_returns_none_for_unknown_id():
    assert set_item(BODY, "ghost", True) is None


def test_toggling_is_idempotent_at_the_text_level():
    once, _ = set_item(BODY, "implement-a-toy-version", True)
    twice, _ = set_item(once, "implement-a-toy-version", True)
    assert once == twice


# ----------------------------------------------------------------------
# Adding
# ----------------------------------------------------------------------


def test_add_items_appends_to_existing_section():
    body, added = add_items(BODY, ["Benchmark it"])
    assert added == ["benchmark-it"]
    lines = body.splitlines()
    # Lands at the end of the Checklist section, before Notes / log.
    assert lines.index("- [ ] Benchmark it") < lines.index("### Notes / log")


def test_add_items_creates_the_section_when_absent():
    body, added = add_items("Just prose.\n", ["First thing"])
    assert "### Checklist" in body
    assert "- [ ] First thing" in body
    assert added == ["first-thing"]


def test_add_items_skips_duplicates():
    body, added = add_items(BODY, ["Read the paper", "Something new"])
    assert added == ["something-new"]
    assert body.count("Read the paper") == 1


def test_add_items_into_a_named_section():
    body, _ = add_items(BODY, ["#1 Two Sum"], section="Problems")
    assert "### Problems" in body
    assert parse_checklist(body).items[-1].section == "Problems"


def test_add_items_normalises_whitespace():
    body, _ = add_items("", ["  spaced   out  "])
    assert "- [ ] spaced out" in body


# ----------------------------------------------------------------------
# Repo integration
# ----------------------------------------------------------------------


def test_repo_add_and_toggle(repo: Repo):
    repo.add_checklist_items("alpha", "first-topic", ["Read it", "Build it"])
    topic = repo.load().skill("alpha").topic("first-topic")
    assert topic.checklist.total == 2
    assert topic.needs_breakdown is False

    result = repo.set_checklist_item("alpha", "first-topic", "read-it", True)
    assert result["changed"] is True
    assert result["checklist"]["done"] == 1


def test_toggling_records_an_event(repo: Repo):
    repo.add_checklist_items("alpha", "first-topic", ["Read it"])
    repo.set_checklist_item("alpha", "first-topic", "read-it", True)
    types = [e.type for e in repo.load().events]
    assert "checklist_added" in types
    assert "checklist_item" in types


def test_toggling_to_the_same_state_is_a_no_op(repo: Repo):
    repo.add_checklist_items("alpha", "first-topic", ["Read it"])
    repo.set_checklist_item("alpha", "first-topic", "read-it", True)
    before = len(repo.load().events)

    result = repo.set_checklist_item("alpha", "first-topic", "read-it", True)
    assert result["changed"] is False
    assert len(repo.load().events) == before, "a no-op must not pollute the history"


def test_repo_rejects_unknown_item_and_topic(repo: Repo):
    with pytest.raises(RepoError, match="unknown checklist item"):
        repo.set_checklist_item("alpha", "first-topic", "ghost", True)
    with pytest.raises(RepoError, match="unknown topic"):
        repo.set_checklist_item("alpha", "ghost", "x", True)


def test_checklist_survives_a_status_write(repo: Repo):
    """Round-tripping the topic file must not eat the task-list syntax."""
    repo.add_checklist_items("alpha", "first-topic", ["Read it", "Build it"])
    repo.set_checklist_item("alpha", "first-topic", "read-it", True)
    repo.update_topic_status("alpha", "first-topic", "comfortable", note="did the work")

    topic = repo.load().skill("alpha").topic("first-topic")
    assert topic.checklist.total == 2
    assert topic.checklist.done == 1
    assert topic.status == "comfortable"


def test_ticking_boxes_does_not_change_status(repo: Repo):
    """Coverage and proficiency are separate claims — see MASTER.md."""
    repo.add_checklist_items("alpha", "first-topic", ["A", "B"])
    repo.set_checklist_item("alpha", "first-topic", "a", True)
    repo.set_checklist_item("alpha", "first-topic", "b", True)

    topic = repo.load().skill("alpha").topic("first-topic")
    assert topic.checklist.percent == 100.0
    assert topic.status == "learning", "status must still require a judged update"


# ----------------------------------------------------------------------
# Coverage + gap flags
# ----------------------------------------------------------------------


def test_coverage_aggregates_across_topics(repo: Repo):
    repo.add_checklist_items("alpha", "first-topic", ["A", "B"])
    repo.set_checklist_item("alpha", "first-topic", "a", True)

    result = coverage(repo.load().all_topics)
    assert result["total"] == 2
    assert result["done"] == 1
    assert result["percent"] == 50.0


def test_gap_flags(repo: Repo):
    state = repo.load()
    first = state.skill("alpha").topic("first-topic")
    third = state.skill("beta").topic("third-topic")

    assert first.needs_breakdown is True
    assert first.needs_evidence is False   # it cites raw/jd/example.md
    assert third.needs_evidence is True    # it cites nothing


def test_validator_reports_gaps(repo: Repo):
    messages = [i.message for i in repo.load().issues if i.level == "warning"]
    assert any("have no checklist breakdown yet" in m for m in messages)
    assert any("cite no evidence" in m for m in messages)


def test_milestone_reports_coverage(repo: Repo):
    repo.set_milestone("w1", title="Week 1", skills=["alpha"])
    repo.add_checklist_items("alpha", "first-topic", ["A", "B", "C"])
    repo.set_checklist_item("alpha", "first-topic", "a", True)

    milestone = repo.load().roadmap_view()["milestones"][0]
    assert milestone["coverage"]["total"] == 3
    assert milestone["coverage"]["done"] == 1
    assert milestone["coverage"]["topics_needing_breakdown"] == 1  # second-topic
