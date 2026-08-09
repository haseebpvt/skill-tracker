"""Loading and the write operations behind the MCP tools."""

from __future__ import annotations

import pytest

from core.markdown import today
from core.paths import PathEscapeError
from core.repo import Repo, RepoError


# ----------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------


def test_loads_role_skills_and_topics(repo: Repo):
    state = repo.load()
    assert state.role.role == "Agentic AI Engineer"
    assert [s.id for s in state.skills] == ["alpha", "beta"]
    assert len(state.all_topics) == 3


def test_skills_follow_role_order_not_alphabetical(repo: Repo):
    path = repo.root / "data" / "role.md"
    path.write_text(path.read_text().replace("  - alpha\n  - beta\n", "  - beta\n  - alpha\n"), encoding="utf-8")
    assert [s.id for s in repo.load().skills] == ["beta", "alpha"]


def test_progress_and_min_bar(repo: Repo):
    summary = repo.load().summary()
    # learning (1/3) + strong (1) + not-started (0), over 3 topics
    assert summary["overall_percent"] == pytest.approx(44.4, abs=0.1)
    assert summary["min_bar"] == {"total": 2, "met": 1}


def test_topics_sorted_by_priority(repo: Repo):
    alpha = repo.load().skill("alpha")
    assert [t.id for t in alpha.topics] == ["first-topic", "second-topic"]


def test_extra_topic_files_are_parsed(repo: Repo):
    folder = repo.root / "data" / "skills" / "alpha"
    (folder / "advanced.md").write_text("## Extra\n- id: extra\n- priority: 9\n", encoding="utf-8")
    assert "extra" in {t.id for t in repo.load().skill("alpha").topics}


def test_underscore_files_are_not_treated_as_topics(repo: Repo):
    assert "alpha" not in {t.id for t in repo.load().all_topics}


def test_load_never_raises_on_broken_files(repo: Repo):
    (repo.root / "data" / "skills" / "alpha" / "topics.md").write_text("## Broken\n\nno meta\n", encoding="utf-8")
    state = repo.load()
    assert any(i.level == "error" for i in state.issues)


# ----------------------------------------------------------------------
# update_topic_status
# ----------------------------------------------------------------------


def test_update_status_writes_and_logs(repo: Repo):
    result = repo.update_topic_status("alpha", "first-topic", "comfortable", note="built a thing")
    assert result["previous_status"] == "learning"

    topic = repo.load().skill("alpha").topic("first-topic")
    assert topic.status == "comfortable"
    assert topic.updated == today()
    assert f"- {today()}: built a thing" in topic.log_md


def test_update_status_defaults_the_log_note(repo: Repo):
    repo.update_topic_status("alpha", "first-topic", "strong")
    assert "learning → strong" in repo.load().skill("alpha").topic("first-topic").log_md


def test_update_status_leaves_other_topics_untouched(repo: Repo, topics_path):
    before = topics_path.read_text()
    repo.update_topic_status("alpha", "first-topic", "strong")
    after = topics_path.read_text()
    # The sibling topic and its custom field are unchanged.
    assert "- custom_field: kept" in after
    assert before.count("## Second topic") == after.count("## Second topic")


def test_update_status_rejects_bad_values(repo: Repo):
    with pytest.raises(RepoError, match="invalid status"):
        repo.update_topic_status("alpha", "first-topic", "wizard")
    with pytest.raises(RepoError, match="unknown topic"):
        repo.update_topic_status("alpha", "nope", "strong")
    with pytest.raises(RepoError, match="unknown skill"):
        repo.update_topic_status("nope", "first-topic", "strong")


# ----------------------------------------------------------------------
# add_topic / add_skill
# ----------------------------------------------------------------------


def test_add_topic(repo: Repo):
    result = repo.add_topic("beta", "A brand new topic", enough=["Can do X", "Knows why"], min_required=True)
    assert result["topic_id"] == "a-brand-new-topic"

    topic = repo.load().skill("beta").topic("a-brand-new-topic")
    assert topic.min_required is True
    assert topic.status == "not-started"
    assert "Can do X" in topic.enough_md
    assert "topic added" in topic.log_md


def test_add_topic_appends_priority_when_omitted(repo: Repo):
    repo.add_topic("alpha", "Later topic", enough=["x"])
    assert repo.load().skill("alpha").topic("later-topic").priority == 3


def test_add_topic_rejects_duplicate_ids_across_the_repo(repo: Repo):
    with pytest.raises(RepoError, match="already exists"):
        repo.add_topic("beta", "First topic", enough=["x"])  # id collides with alpha's


def test_add_skill_creates_files_and_updates_order(repo: Repo):
    result = repo.add_skill("gamma", "Gamma Skill", priority=2, description="Third one.")
    assert result["skill_order"] == ["alpha", "gamma", "beta"]

    state = repo.load()
    assert [s.id for s in state.skills] == ["alpha", "gamma", "beta"]
    # Priorities are renumbered to match position, so the UI order is consistent.
    assert [s.priority for s in state.skills] == [1, 2, 3]
    assert (repo.root / "data" / "skills" / "gamma" / "topics.md").is_file()


def test_add_skill_rejects_duplicates(repo: Repo):
    with pytest.raises(RepoError, match="already exists"):
        repo.add_skill("alpha", "Alpha again")


# ----------------------------------------------------------------------
# set_focus
# ----------------------------------------------------------------------


def test_set_focus_clears_previous_by_default(repo: Repo):
    repo.set_focus([("alpha", "first-topic")])
    focused = {t.id for t in repo.load().all_topics if t.focus}
    assert focused == {"first-topic"}  # second-topic started focused and was cleared


def test_set_focus_can_add_without_clearing(repo: Repo):
    repo.set_focus([("alpha", "first-topic")], clear_existing=False)
    focused = {t.id for t in repo.load().all_topics if t.focus}
    assert focused == {"first-topic", "second-topic"}


def test_set_focus_clears_across_skills(repo: Repo):
    repo.set_focus([("beta", "third-topic")])
    focused = {t.id for t in repo.load().all_topics if t.focus}
    assert focused == {"third-topic"}


def test_set_focus_rejects_unknown_topics(repo: Repo):
    with pytest.raises(RepoError, match="unknown topic"):
        repo.set_focus([("alpha", "ghost")])


# ----------------------------------------------------------------------
# role order
# ----------------------------------------------------------------------


def test_update_role_order_renumbers_priorities(repo: Repo):
    repo.update_role_order(["beta", "alpha"])
    state = repo.load()
    assert state.role.skill_order == ["beta", "alpha"]
    assert state.skill("beta").priority == 1
    assert state.skill("alpha").priority == 2


def test_update_role_order_appends_omitted_skills(repo: Repo):
    result = repo.update_role_order(["beta"])
    assert result["appended_missing"] == ["alpha"]
    assert repo.load().role.skill_order == ["beta", "alpha"]


def test_update_role_order_rejects_unknown_and_duplicates(repo: Repo):
    with pytest.raises(RepoError, match="unknown skill id"):
        repo.update_role_order(["alpha", "ghost"])
    with pytest.raises(RepoError, match="duplicates"):
        repo.update_role_order(["alpha", "alpha"])


# ----------------------------------------------------------------------
# evidence + sandboxing
# ----------------------------------------------------------------------


def test_read_evidence(repo: Repo):
    result = repo.read_evidence("raw/jd/example.md")
    assert result["source"] == "Example JD"
    assert "do the thing" in result["content"]


def test_read_evidence_tolerates_an_evidence_prefix(repo: Repo):
    assert repo.read_evidence("evidence/raw/jd/example.md")["source"] == "Example JD"


def test_read_evidence_rejects_missing_files(repo: Repo):
    with pytest.raises(RepoError, match="no evidence file"):
        repo.read_evidence("raw/jd/ghost.md")


@pytest.mark.parametrize("path", ["../../../../etc/passwd", "/etc/passwd", "raw/../../../secrets.md"])
def test_path_traversal_is_blocked(repo: Repo, path):
    with pytest.raises((PathEscapeError, RepoError)):
        repo.read_evidence(path)


def test_write_conclusions_records_hashes(repo: Repo):
    content = (
        "## Skill priority ranking\nAlpha first.\n\n"
        "## Minimum bar\nTwo topics.\n\n"
        "## Per-skill topic requirements\nStuff.\n\n"
        "## Open contradictions / questions for the human\nNone.\n"
    )
    result = repo.write_conclusions(content)
    assert result["evidence_files_recorded"] == 1
    assert result["missing_sections"] == []

    state = repo.load()
    assert state.conclusions.exists
    assert state.conclusions.considered[0]["path"] == "raw/jd/example.md"
    assert len(state.conclusions.considered[0]["hash"]) == 64
    # Freshly compiled, so nothing is stale.
    assert state.evidence_status()["unchanged"] == ["raw/jd/example.md"]


def test_write_conclusions_reports_missing_sections(repo: Repo):
    assert "Minimum bar" in repo.write_conclusions("## Skill priority ranking\nx\n")["missing_sections"]


def test_write_conclusions_rejects_empty(repo: Repo):
    with pytest.raises(RepoError, match="empty"):
        repo.write_conclusions("   \n")


def test_evidence_status_detects_new_and_modified(repo: Repo):
    repo.write_conclusions("## Skill priority ranking\nx\n")

    jd = repo.root / "evidence" / "raw" / "jd"
    (jd / "example.md").write_text("---\nsource: Example JD\n---\nchanged content\n", encoding="utf-8")
    (jd / "fresh.md").write_text("---\nsource: New JD\n---\nnew content\n", encoding="utf-8")

    status = repo.load().evidence_status()
    assert status["modified"] == ["raw/jd/example.md"]
    assert status["new"] == ["raw/jd/fresh.md"]


def test_evidence_status_detects_deleted(repo: Repo):
    repo.write_conclusions("## Skill priority ranking\nx\n")
    (repo.root / "evidence" / "raw" / "jd" / "example.md").unlink()
    assert repo.load().evidence_status()["deleted"] == ["raw/jd/example.md"]


def test_hashes_ignore_line_ending_differences(repo: Repo):
    repo.write_conclusions("## Skill priority ranking\nx\n")
    path = repo.root / "evidence" / "raw" / "jd" / "example.md"
    path.write_bytes(path.read_text().replace("\n", "\r\n").encode("utf-8"))
    assert repo.load().evidence_status()["modified"] == []


def test_state_is_json_serialisable(repo: Repo):
    import json

    json.dumps(repo.load().to_dict())
