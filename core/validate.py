"""Repo validator (§4.4).

Checks unique ids, valid statuses, integer priorities and that referenced
evidence files exist. Returns issues rather than raising — the viewer renders
them, the MCP tool reports them, the CLI exits non-zero on errors.
"""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from .models import STATUSES, Issue

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .repo import State


def cross_check(state: "State") -> list[Issue]:
    """Checks that need the whole repo in hand (run automatically on load)."""
    issues: list[Issue] = []

    # --- unique ids ----------------------------------------------------
    skill_counts = Counter(skill.id for skill in state.skills)
    for skill_id, count in skill_counts.items():
        if count > 1:
            issues.append(Issue("error", f"duplicate skill id '{skill_id}' ({count} folders)", "data/skills"))

    topic_counts = Counter(topic.id for topic in state.all_topics)
    for topic_id, count in topic_counts.items():
        if count > 1:
            owners = sorted({t.source_file for t in state.all_topics if t.id == topic_id})
            issues.append(Issue("error", f"duplicate topic id '{topic_id}' in {', '.join(owners)}", owners[0] if owners else ""))

    # --- statuses and priorities ---------------------------------------
    for skill in state.skills:
        seen_priorities: dict[int, str] = {}
        for topic in skill.topics:
            if topic.status not in STATUSES:
                issues.append(
                    Issue(
                        "error",
                        f"topic '{topic.id}': unknown status '{topic.status}' (expected {', '.join(STATUSES)})",
                        topic.source_file,
                    )
                )
            if isinstance(topic.priority, int) and topic.priority in seen_priorities:
                issues.append(
                    Issue(
                        "warning",
                        f"skill '{skill.id}': topics '{seen_priorities[topic.priority]}' and '{topic.id}' "
                        f"share priority {topic.priority}",
                        topic.source_file,
                    )
                )
            elif isinstance(topic.priority, int):
                seen_priorities[topic.priority] = topic.id

    # --- evidence references exist -------------------------------------
    known_evidence = {item.path for item in state.evidence}
    for topic in state.all_topics:
        for reference in topic.evidence:
            normalised = reference.strip().lstrip("/")
            if normalised.startswith("evidence/"):
                normalised = normalised[len("evidence/") :]
            if not normalised.startswith("raw/"):
                normalised = f"raw/{normalised}"
            if normalised not in known_evidence:
                issues.append(
                    Issue(
                        "warning",
                        f"topic '{topic.id}': evidence '{reference}' not found under evidence/raw/",
                        topic.source_file,
                    )
                )

    # --- role ordering matches skill priorities -------------------------
    if state.role is not None:
        order = state.role.skill_order
        unknown = [skill_id for skill_id in order if not any(s.id == skill_id for s in state.skills)]
        for skill_id in unknown:
            issues.append(Issue("warning", f"role.md skill_order lists unknown skill '{skill_id}'", "data/role.md"))

        missing = [skill.id for skill in state.skills if skill.id not in order]
        for skill_id in missing:
            issues.append(
                Issue("warning", f"skill '{skill_id}' is not listed in role.md skill_order", "data/role.md")
            )

        for position, skill_id in enumerate([s for s in order if s not in unknown], start=1):
            skill = state.skill(skill_id)
            if skill is not None and skill.priority != position:
                issues.append(
                    Issue(
                        "warning",
                        f"skill '{skill_id}': priority {skill.priority} does not match its position "
                        f"({position}) in role.md skill_order",
                        f"data/skills/{skill_id}/_skill.md",
                    )
                )

    # --- conclusions freshness -----------------------------------------
    if state.conclusions.exists:
        status = state.evidence_status()
        stale = status["new"] + status["modified"] + status["deleted"]
        if stale:
            issues.append(
                Issue(
                    "warning",
                    f"CONCLUSIONS.md is stale: {len(status['new'])} new, {len(status['modified'])} modified, "
                    f"{len(status['deleted'])} deleted evidence file(s)",
                    "evidence/CONCLUSIONS.md",
                )
            )
    elif state.evidence:
        issues.append(
            Issue("warning", "evidence exists but evidence/CONCLUSIONS.md has not been written yet", "evidence")
        )

    return issues


def validate(state: "State") -> dict[str, object]:
    """Full validation result, split into errors and warnings."""
    issues = state.issues
    errors = [issue.to_dict() for issue in issues if issue.level == "error"]
    warnings = [issue.to_dict() for issue in issues if issue.level == "warning"]
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {"errors": len(errors), "warnings": len(warnings)},
    }
