"""Shared fixtures: a throwaway repo built from scratch for each test."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from core.repo import Repo

ROLE_MD = """\
---
role: Agentic AI Engineer
level: Senior
updated: 2026-08-01
skill_order:
  - alpha
  - beta
---
Notes about the role.
"""

ALPHA_SKILL = """\
---
id: alpha
name: Alpha Skill
priority: 1
updated: 2026-08-01
---
The first skill.
"""

ALPHA_TOPICS = """\
<!-- preamble comment that must survive a round trip -->

## First topic
- id: first-topic
- status: learning
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-01
- evidence: [raw/jd/example.md]

### What "enough" looks like
- Can do the thing
- Knows why the thing works

### Notes / log
- 2026-08-01: started

## Second topic
- id: second-topic
- status: strong
- priority: 2
- min_required: true
- focus: true
- updated: 2026-08-02
- custom_field: kept

### What "enough" looks like
- Can teach it
"""

BETA_SKILL = """\
---
id: beta
name: Beta Skill
priority: 2
updated: 2026-08-01
---
The second skill.
"""

BETA_TOPICS = """\
## Third topic
- id: third-topic
- status: not-started
- priority: 1
- min_required: false
- focus: false

### What "enough" looks like
- Something concrete
"""

EVIDENCE = """\
---
source: "Example JD"
added: 2026-08-01
---
We need someone who can do the thing.
"""


@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    """A minimal but complete repo: 2 skills, 3 topics, 1 evidence file."""
    (tmp_path / "MASTER.md").write_text("# MASTER\n", encoding="utf-8")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "role.md").write_text(ROLE_MD, encoding="utf-8")

    skills = tmp_path / "data" / "skills"
    for name, meta, topics in (
        ("alpha", ALPHA_SKILL, ALPHA_TOPICS),
        ("beta", BETA_SKILL, BETA_TOPICS),
    ):
        folder = skills / name
        folder.mkdir(parents=True)
        (folder / "_skill.md").write_text(meta, encoding="utf-8")
        (folder / "topics.md").write_text(topics, encoding="utf-8")

    jd = tmp_path / "evidence" / "raw" / "jd"
    jd.mkdir(parents=True)
    (jd / "example.md").write_text(EVIDENCE, encoding="utf-8")

    return Repo(tmp_path)


@pytest.fixture
def topics_path(repo: Repo) -> Path:
    return repo.root / "data" / "skills" / "alpha" / "topics.md"
