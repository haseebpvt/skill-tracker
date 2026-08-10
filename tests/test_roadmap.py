"""Roadmap parsing, milestone derivation and the schedule verdict."""

from __future__ import annotations

from datetime import date

import pytest

from core.repo import Repo, RepoError
from core.roadmap import (
    Milestone,
    derive_milestone,
    parse_roadmap,
    resolve_topics,
    serialize_roadmap,
    validate_roadmap,
)

SAMPLE = """\
---
updated: 2026-08-10
start_date: 2026-08-01
target_date: 2026-09-01
---

Intro prose.

## Week 1 — Foundations
- id: w1
- target: 2026-08-15
- status: in-progress
- skills: [alpha]
- topics: [third-topic]

Why this matters.
"""


def test_parses_frontmatter_and_milestones():
    roadmap, issues = parse_roadmap(SAMPLE)
    assert not [i for i in issues if i.level == "error"]
    assert roadmap.start_date == "2026-08-01"
    assert roadmap.target_date == "2026-09-01"
    assert "Intro prose." in roadmap.notes

    milestone = roadmap.milestones[0]
    assert milestone.id == "w1"
    assert milestone.target == "2026-08-15"
    assert milestone.skills == ["alpha"]
    assert milestone.topics == ["third-topic"]
    assert "Why this matters." in milestone.description


def test_round_trip_is_stable():
    roadmap, _ = parse_roadmap(SAMPLE)
    once = serialize_roadmap(roadmap)
    twice = serialize_roadmap(parse_roadmap(once)[0])
    assert once == twice


def test_milestones_sort_by_target_date():
    text = SAMPLE + "\n## Earlier\n- id: w0\n- target: 2026-08-02\n- skills: [beta]\n"
    roadmap, _ = parse_roadmap(text)
    assert [m.id for m in roadmap.milestones] == ["w0", "w1"]


def test_undated_milestones_sort_last():
    text = SAMPLE + "\n## Someday\n- id: later\n- skills: [beta]\n"
    roadmap, _ = parse_roadmap(text)
    assert [m.id for m in roadmap.milestones] == ["w1", "later"]


def test_invalid_status_and_target_are_reported():
    text = "---\n---\n\n## Bad\n- id: bad\n- target: soon\n- status: nearly\n"
    _, issues = parse_roadmap(text)
    messages = [i.message for i in issues if i.level == "error"]
    assert any("unknown status" in m for m in messages)
    assert any("not a YYYY-MM-DD date" in m for m in messages)


# ----------------------------------------------------------------------
# Derivation — the part that keeps the roadmap honest
# ----------------------------------------------------------------------


def test_skills_expand_to_all_their_topics(repo: Repo):
    state = repo.load()
    milestone = Milestone(id="m", title="M", skills=["alpha"])
    topics, missing = resolve_topics(milestone, state.all_topics)
    assert {t.id for t in topics} == {"first-topic", "second-topic"}
    assert missing == []


def test_topics_and_skills_combine_without_duplicates(repo: Repo):
    state = repo.load()
    milestone = Milestone(id="m", title="M", skills=["alpha"], topics=["first-topic", "third-topic"])
    topics, _ = resolve_topics(milestone, state.all_topics)
    assert [t.id for t in topics].count("first-topic") == 1
    assert {t.id for t in topics} == {"first-topic", "second-topic", "third-topic"}


def test_missing_topic_references_are_reported(repo: Repo):
    state = repo.load()
    milestone = Milestone(id="m", title="M", topics=["ghost"])
    _, missing = resolve_topics(milestone, state.all_topics)
    assert missing == ["ghost"]


def test_progress_is_derived_from_live_topic_status(repo: Repo):
    milestone = Milestone(id="m", title="M", skills=["alpha"])
    before = derive_milestone(milestone, repo.load().all_topics, today=date(2026, 8, 10))
    assert before["progress"]["complete"] == 1  # second-topic is strong

    repo.update_topic_status("alpha", "first-topic", "comfortable")
    after = derive_milestone(milestone, repo.load().all_topics, today=date(2026, 8, 10))
    assert after["progress"]["complete"] == 2
    assert after["derived_status"] == "done"


@pytest.mark.parametrize(
    "target,expected",
    [
        ("2026-08-01", "overdue"),   # target already passed
        ("2026-08-10", "at-risk"),   # due today with 1 topic still outstanding
        ("2026-08-11", "on-track"),  # exactly 1 day per outstanding topic — tight but doable
        ("2026-09-30", "on-track"),  # plenty of time
    ],
)
def test_schedule_verdicts(repo: Repo, target, expected):
    """Alpha has 2 topics, 1 of them already strong, so 1 is outstanding."""
    milestone = Milestone(id="m", title="M", skills=["alpha"], target=target, status="in-progress")
    derived = derive_milestone(milestone, repo.load().all_topics, today=date(2026, 8, 10))
    assert derived["derived_status"] == expected


def test_blocked_wins_over_schedule(repo: Repo):
    milestone = Milestone(id="m", title="M", skills=["alpha"], target="2026-01-01", status="blocked")
    derived = derive_milestone(milestone, repo.load().all_topics, today=date(2026, 8, 10))
    assert derived["derived_status"] == "blocked"


def test_declared_done_is_overruled_by_incomplete_topics(repo: Repo):
    """A milestone cannot claim to be finished while its topics say otherwise."""
    milestone = Milestone(id="m", title="M", skills=["alpha"], status="done", target="2026-09-30")
    derived = derive_milestone(milestone, repo.load().all_topics, today=date(2026, 8, 10))
    assert derived["derived_status"] == "at-risk"


def test_validate_flags_unknown_references(repo: Repo):
    state = repo.load()
    roadmap, _ = parse_roadmap("---\n---\n\n## M\n- id: m\n- topics: [ghost]\n- skills: [nope]\n")
    messages = [i.message for i in validate_roadmap(roadmap, state.all_topics, {"alpha", "beta"})]
    assert any("unknown topic 'ghost'" in m for m in messages)
    assert any("unknown skill 'nope'" in m for m in messages)


def test_validate_flags_empty_milestone(repo: Repo):
    roadmap, _ = parse_roadmap("---\n---\n\n## Empty\n- id: empty\n")
    messages = [i.message for i in validate_roadmap(roadmap, repo.load().all_topics, set())]
    assert any("references no topics or skills" in m for m in messages)


# ----------------------------------------------------------------------
# Write operations
# ----------------------------------------------------------------------


def test_set_milestone_creates_then_updates(repo: Repo):
    created = repo.set_milestone("w1", title="Week 1", target="2026-08-20", skills=["alpha"])
    assert created["created"] is True

    updated = repo.set_milestone("w1", target="2026-08-25")
    assert updated["created"] is False

    roadmap = repo.load().roadmap
    assert len(roadmap.milestones) == 1
    milestone = roadmap.milestone("w1")
    assert milestone.target == "2026-08-25"
    assert milestone.title == "Week 1"      # untouched by the partial update
    assert milestone.skills == ["alpha"]


def test_set_milestone_requires_title_on_create(repo: Repo):
    with pytest.raises(RepoError, match="supply a title"):
        repo.set_milestone("ghost", target="2026-08-20")


def test_set_milestone_rejects_unknown_references(repo: Repo):
    with pytest.raises(RepoError, match="unknown topic id"):
        repo.set_milestone("w1", title="W1", topics=["ghost"])
    with pytest.raises(RepoError, match="unknown skill id"):
        repo.set_milestone("w1", title="W1", skills=["ghost"])


def test_set_milestone_rejects_bad_dates_and_statuses(repo: Repo):
    with pytest.raises(RepoError, match="not a YYYY-MM-DD date"):
        repo.set_milestone("w1", title="W1", target="next tuesday")
    with pytest.raises(RepoError, match="invalid milestone status"):
        repo.set_milestone("w1", title="W1", status="nearly")


def test_remove_milestone(repo: Repo):
    repo.set_milestone("w1", title="Week 1", skills=["alpha"])
    assert repo.remove_milestone("w1")["remaining"] == 0
    with pytest.raises(RepoError, match="unknown milestone"):
        repo.remove_milestone("w1")


def test_set_roadmap_window(repo: Repo):
    repo.set_roadmap_meta(start_date="2026-08-01", target_date="2026-09-01", notes="Go.")
    roadmap = repo.load().roadmap
    assert roadmap.start_date == "2026-08-01"
    assert roadmap.target_date == "2026-09-01"
    assert "Go." in roadmap.notes


def test_set_roadmap_window_rejects_bad_dates(repo: Repo):
    with pytest.raises(RepoError, match="not a YYYY-MM-DD date"):
        repo.set_roadmap_meta(target_date="whenever")
