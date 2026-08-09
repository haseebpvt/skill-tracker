"""The §4.4 validator."""

from __future__ import annotations

from core.repo import Repo
from core.validate import validate


def errors(repo: Repo) -> list[str]:
    return [issue["message"] for issue in validate(repo.load())["errors"]]


def warnings(repo: Repo) -> list[str]:
    return [issue["message"] for issue in validate(repo.load())["warnings"]]


def test_clean_repo_has_no_errors(repo: Repo):
    report = validate(repo.load())
    assert report["ok"]
    assert report["errors"] == []


def test_detects_duplicate_topic_ids(repo: Repo):
    folder = repo.root / "data" / "skills" / "beta"
    (folder / "more.md").write_text("## Dupe\n- id: third-topic\n- priority: 5\n", encoding="utf-8")
    assert any("duplicate topic id 'third-topic'" in m for m in errors(repo))


def test_detects_invalid_status(repo: Repo):
    path = repo.root / "data" / "skills" / "beta" / "topics.md"
    path.write_text(path.read_text().replace("status: not-started", "status: wizard"), encoding="utf-8")
    assert any("unknown status 'wizard'" in m for m in errors(repo))


def test_detects_non_integer_priority(repo: Repo):
    path = repo.root / "data" / "skills" / "beta" / "topics.md"
    path.write_text(path.read_text().replace("priority: 1", "priority: first"), encoding="utf-8")
    assert any("priority must be an integer" in m for m in errors(repo))


def test_detects_skill_id_not_matching_folder(repo: Repo):
    path = repo.root / "data" / "skills" / "beta" / "_skill.md"
    path.write_text(path.read_text().replace("id: beta", "id: mismatched"), encoding="utf-8")
    assert any("does not match folder name" in m for m in errors(repo))


def test_detects_missing_evidence_reference(repo: Repo):
    path = repo.root / "data" / "skills" / "alpha" / "topics.md"
    path.write_text(path.read_text().replace("raw/jd/example.md", "raw/jd/ghost.md"), encoding="utf-8")
    assert any("evidence 'raw/jd/ghost.md' not found" in m for m in warnings(repo))


def test_detects_duplicate_priorities_within_a_skill(repo: Repo):
    path = repo.root / "data" / "skills" / "alpha" / "topics.md"
    path.write_text(path.read_text().replace("- priority: 2", "- priority: 1"), encoding="utf-8")
    assert any("share priority 1" in m for m in warnings(repo))


def test_detects_skill_missing_from_role_order(repo: Repo):
    path = repo.root / "data" / "role.md"
    path.write_text(path.read_text().replace("  - beta\n", ""), encoding="utf-8")
    assert any("'beta' is not listed in role.md skill_order" in m for m in warnings(repo))


def test_detects_priority_out_of_sync_with_role_order(repo: Repo):
    path = repo.root / "data" / "skills" / "beta" / "_skill.md"
    path.write_text(path.read_text().replace("priority: 2", "priority: 7"), encoding="utf-8")
    assert any("does not match its position" in m for m in warnings(repo))


def test_warns_when_conclusions_are_stale(repo: Repo):
    repo.write_conclusions("## Skill priority ranking\nx\n")
    jd = repo.root / "evidence" / "raw" / "jd"
    (jd / "another.md").write_text("---\nsource: Another\n---\ncontent\n", encoding="utf-8")
    assert any("CONCLUSIONS.md is stale" in m for m in warnings(repo))


def test_warns_when_conclusions_missing_entirely(repo: Repo):
    assert any("has not been written yet" in m for m in warnings(repo))


def test_missing_role_file_is_an_error(repo: Repo):
    (repo.root / "data" / "role.md").unlink()
    assert any("missing data/role.md" in m for m in errors(repo))
