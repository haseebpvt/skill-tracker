"""MCP server for the skill tracker (stdio).

The app has no brain: these tools only read and write markdown. Every decision —
what "comfortable" means, what to focus on next, how to weigh new evidence — is
made by the agent on the other end of this connection. See MASTER.md.

Built on the official Python MCP SDK. In SDK 2.x the server class formerly known
as ``FastMCP`` is ``MCPServer``; the decorator-based API is otherwise the same.
"""

from __future__ import annotations

import os
from typing import Annotated, Any, Literal

from mcp.server.mcpserver import MCPServer
from pydantic import BaseModel, Field

from core.models import STATUSES
from core.paths import PathEscapeError
from core.repo import Repo, RepoError
from core.validate import validate as run_validate

INSTRUCTIONS = """\
Skill tracker: markdown-backed progress tracking for interview prep and upskilling.

Read MASTER.md at the repo root before your first write in a session. It defines
the status rubric, the stability rules for priorities and conclusions, and the
step-by-step workflows these tools are meant to be used in.

Two rules that are easy to get wrong:
  - Do not upgrade a topic to `comfortable` or `strong` on the human's say-so.
    Probe first against the topic's "what enough looks like" criteria.
  - Do not reorder skill or topic priorities on your own. Propose; let the human
    approve; only then call update_role_order.
"""

server = MCPServer(
    name="skill-tracker",
    version="0.1.0",
    instructions=INSTRUCTIONS,
)

Status = Literal["not-started", "learning", "comfortable", "strong"]


def _repo() -> Repo:
    """Fresh handle each call, so writes made outside are always picked up."""
    return Repo(os.environ.get("SKILL_TRACKER_REPO"))


def _guard(action, *args, **kwargs) -> Any:
    """Translate repo errors into tool errors the agent can read."""
    try:
        return action(*args, **kwargs)
    except (RepoError, PathEscapeError) as exc:
        raise ValueError(str(exc)) from exc


class FocusTarget(BaseModel):
    """One topic to flag as the current focus."""

    skill_id: str = Field(description="Skill folder id, e.g. 'agentic-frameworks'")
    topic_id: str = Field(description="Topic id within that skill, e.g. 'langgraph-state-machines'")


# ----------------------------------------------------------------------
# Read tools
# ----------------------------------------------------------------------


@server.tool(
    description=(
        "Cheap orientation call. Returns the target role, the ordered skill list with per-skill "
        "progress percentage and status counts, overall progress, minimum-bar coverage, and whether "
        "conclusions are stale. Start here. See MASTER.md for workflow rules."
    )
)
def get_overview() -> dict[str, Any]:
    state = _repo().load()
    return {
        "role": state.role.to_dict() if state.role else None,
        "summary": state.summary(),
        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "priority": skill.priority,
                "updated": skill.updated,
                "progress": skill.progress(),
            }
            for skill in state.skills
        ],
        "focus": [
            {"skill_id": t.skill_id, "topic_id": t.id, "title": t.title, "status": t.status}
            for t in state.all_topics
            if t.focus
        ],
        "evidence_status": state.evidence_status(),
        "conclusions_updated": state.conclusions.updated,
        "issue_counts": {
            "errors": sum(1 for i in state.issues if i.level == "error"),
            "warnings": sum(1 for i in state.issues if i.level == "warning"),
        },
    }


@server.tool(
    description=(
        "Full parsed content of one skill: every topic with its status, priority, min_required flag, "
        "focus flag, evidence references, the 'what enough looks like' criteria and the notes log. "
        "Read this before judging whether a status should change. See MASTER.md for workflow rules."
    )
)
def get_skill(skill_id: Annotated[str, Field(description="Skill folder id, e.g. 'dsa'")]) -> dict[str, Any]:
    state = _repo().load()
    skill = state.skill(skill_id)
    if skill is None:
        known = ", ".join(s.id for s in state.skills)
        raise ValueError(f"unknown skill '{skill_id}'. Known skills: {known}")
    return skill.to_dict()


@server.tool(
    description=(
        "Returns the raw material for choosing what to learn next: every topic across every skill with "
        "status, skill priority, topic priority, min_required and current focus flags, plus the "
        "min-bar gap list. This tool does NOT choose — you do. Reason using min_required gaps first, "
        "then priority order, then prerequisites. See MASTER.md → 'What should I focus on next?'."
    )
)
def get_focus_candidates() -> dict[str, Any]:
    state = _repo().load()
    candidates = []
    for skill in state.skills:
        for topic in skill.topics:
            candidates.append(
                {
                    "skill_id": skill.id,
                    "skill_name": skill.name,
                    "skill_priority": skill.priority,
                    "topic_id": topic.id,
                    "title": topic.title,
                    "status": topic.status,
                    "topic_priority": topic.priority,
                    "min_required": topic.min_required,
                    "focus": topic.focus,
                    "updated": topic.updated,
                    "enough": topic.enough_md,
                }
            )
    gaps = [c for c in candidates if c["min_required"] and c["status"] in ("not-started", "learning")]
    return {
        "summary": state.summary(),
        "current_focus": [c for c in candidates if c["focus"]],
        "min_bar_gaps": sorted(gaps, key=lambda c: (c["skill_priority"], c["topic_priority"])),
        "candidates": candidates,
    }


@server.tool(
    description=(
        "Diffs the sha256 of every file under evidence/raw/ against the manifest recorded in "
        "CONCLUSIONS.md, and reports which are new, modified, deleted or unchanged. Call this before "
        "recompiling conclusions and read ONLY the new/modified files — that is what keeps updates "
        "incremental. See MASTER.md → 'New evidence added'."
    )
)
def get_evidence_status() -> dict[str, Any]:
    state = _repo().load()
    status = state.evidence_status()
    return {
        "conclusions_exist": state.conclusions.exists,
        "conclusions_updated": state.conclusions.updated,
        "needs_recompile": bool(status["new"] or status["modified"] or status["deleted"]),
        **status,
        "files": [item.to_dict() for item in state.evidence],
    }


@server.tool(
    description=(
        "Read one raw evidence file, by path relative to evidence/ (e.g. 'raw/jd/acme-2026-07.md'). "
        "Paths are sandboxed to the repo. See MASTER.md for workflow rules."
    )
)
def read_evidence(
    path: Annotated[str, Field(description="Path relative to evidence/, e.g. 'raw/jd/acme-2026-07.md'")],
) -> dict[str, Any]:
    return _guard(_repo().read_evidence, path)


@server.tool(
    description=(
        "Run the repo validator: unique ids, valid statuses, integer priorities, evidence references "
        "resolve, role.md ordering matches skill priorities, conclusions freshness. Returns errors and "
        "warnings. Run after any batch of writes. See MASTER.md for workflow rules."
    )
)
def validate_repo() -> dict[str, Any]:
    return run_validate(_repo().load())


# ----------------------------------------------------------------------
# Write tools
# ----------------------------------------------------------------------


@server.tool(
    description=(
        "Set a topic's status and append a dated line to its Notes / log section.\n\n"
        "Do NOT call this with `comfortable` or `strong` just because the human said they learned "
        "something. First get_skill, read that topic's 'what enough looks like' criteria, and ask "
        "probing questions until you can judge it yourself. See MASTER.md → status rubric."
    )
)
def update_topic_status(
    skill_id: Annotated[str, Field(description="Skill folder id")],
    topic_id: Annotated[str, Field(description="Topic id within that skill")],
    status: Annotated[Status, Field(description=f"One of: {', '.join(STATUSES)}")],
    note: Annotated[
        str | None,
        Field(description="What changed and what evidence justified it. Becomes the dated log line."),
    ] = None,
) -> dict[str, Any]:
    return _guard(_repo().update_topic_status, skill_id, topic_id, status, note)


@server.tool(
    description=(
        "Add a new topic to a skill. The id must be unique across the whole repo; it is derived from "
        "the title if omitted. Always supply `enough` — concrete, checkable criteria for what "
        "proficiency in this topic actually means, since that is what future status judgements are "
        "made against. See MASTER.md for the file format."
    )
)
def add_topic(
    skill_id: Annotated[str, Field(description="Skill folder id the topic belongs to")],
    title: Annotated[str, Field(description="Human-readable topic title, e.g. 'LangGraph state machines'")],
    enough: Annotated[
        list[str],
        Field(description="Bullet points defining what 'enough' looks like for this topic"),
    ],
    topic_id: Annotated[str | None, Field(description="Explicit id; derived from the title if omitted")] = None,
    status: Annotated[Status, Field(description="Starting status")] = "not-started",
    priority: Annotated[
        int | None, Field(description="Order within the skill, 1 = most important. Appended last if omitted.")
    ] = None,
    min_required: Annotated[
        bool, Field(description="Is this part of the minimum bar for the role, per the evidence?")
    ] = False,
    evidence: Annotated[
        list[str], Field(description="Evidence paths relative to evidence/, e.g. ['raw/jd/acme.md']")
    ] = [],
    notes: Annotated[str, Field(description="Optional first log line")] = "",
) -> dict[str, Any]:
    return _guard(
        _repo().add_topic,
        skill_id,
        title,
        topic_id=topic_id,
        status=status,
        priority=priority,
        min_required=min_required,
        evidence=evidence,
        enough=enough,
        notes=notes,
    )


@server.tool(
    description=(
        "Create a new skill: its folder, _skill.md and an empty topics.md, then insert it into "
        "role.md's skill_order at the given position. Inserting changes the display order of every "
        "skill below it, so confirm the position with the human first. See MASTER.md → stability rules."
    )
)
def add_skill(
    skill_id: Annotated[str, Field(description="Folder id, kebab-case, e.g. 'agentic-frameworks'")],
    name: Annotated[str, Field(description="Display name, e.g. 'Agentic Frameworks'")],
    priority: Annotated[
        int | None, Field(description="1-based position in role.md skill_order. Appended last if omitted.")
    ] = None,
    description: Annotated[str, Field(description="What this skill covers and why it matters")] = "",
) -> dict[str, Any]:
    return _guard(_repo().add_skill, skill_id, name, priority=priority, description=description)


@server.tool(
    description=(
        "Flag 1-3 topics as the current focus; they pulse in the viewer. By default this clears all "
        "previous focus flags first, which is what keeps focus meaningful — do not pass "
        "clear_existing=false unless the human asked to add to the existing set. After calling, tell "
        "the human WHY you picked these. See MASTER.md → 'What should I focus on next?'."
    )
)
def set_focus(
    topics: Annotated[list[FocusTarget], Field(description="The topics to focus on. Keep it to 1-3.")],
    clear_existing: Annotated[bool, Field(description="Clear all existing focus flags first")] = True,
) -> dict[str, Any]:
    targets = [(t.skill_id, t.topic_id) for t in topics]
    return _guard(_repo().set_focus, targets, clear_existing=clear_existing)


@server.tool(
    description=(
        "Overwrite evidence/CONCLUSIONS.md and refresh its evidence hash manifest automatically.\n\n"
        "This is a full overwrite, so `content` must be the complete document, not a patch: read the "
        "existing conclusions first and carry forward everything still true. Integrate only the delta "
        "from new evidence. Where new evidence contradicts an existing conclusion, do not silently "
        "overwrite — record it under 'Open contradictions / questions for the human'. Expected "
        "sections: Skill priority ranking, Minimum bar, Per-skill topic requirements, Open "
        "contradictions. See MASTER.md → stability rules."
    )
)
def write_conclusions(
    content: Annotated[str, Field(description="The complete markdown body, without frontmatter")],
) -> dict[str, Any]:
    return _guard(_repo().write_conclusions, content)


@server.tool(
    description=(
        "Rewrite the skill display order in role.md and re-sync each skill's priority field.\n\n"
        "REQUIRES EXPLICIT HUMAN CONFIRMATION. Priority order is deliberately sticky so the viewer "
        "does not reshuffle every time conclusions are recompiled. Propose the new order and your "
        "reasoning in chat, wait for a yes, then call this. Any skill you omit is appended in its "
        "current relative order rather than dropped. See MASTER.md → stability rules."
    )
)
def update_role_order(
    skill_order: Annotated[list[str], Field(description="Skill ids, most important first")],
) -> dict[str, Any]:
    return _guard(_repo().update_role_order, skill_order)


def main() -> None:
    """Entry point: serve over stdio."""
    server.run("stdio")


if __name__ == "__main__":  # pragma: no cover
    main()
