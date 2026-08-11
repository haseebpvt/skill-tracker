"""The repo as an object: load everything into a model, and write it back.

This is the single place that knows the on-disk layout. Both the MCP server
and the viewer backend go through it, so parsing exists exactly once.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from datetime import date as _date
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import checklist as checklist_mod
from . import evidence as evidence_mod
from . import history as history_mod
from . import roadmap as roadmap_mod
from . import velocity as velocity_mod
from .git import git_status
from .history import Event, utc_now
from .markdown import ParseError, join_frontmatter, split_frontmatter, today
from .models import (
    STATUS_WEIGHTS,
    STATUSES,
    coverage,
    Conclusions,
    EvidenceFile,
    Issue,
    Role,
    Skill,
    Topic,
    slugify,
)
from .paths import find_repo_root, relative_to_root, safe_path
from .render import render_roadmap_doc
from .roadmap import Milestone, Roadmap
from .topics import TopicFile, append_log_entry, parse_topics, serialize_topics

#: The generated status report at the repo root (see core/render.py).
ROADMAP_DOC = "ROADMAP.md"

DATA_DIR = "data"
SKILLS_DIR = "data/skills"
ROLE_FILE = "data/role.md"
SKILL_META_FILE = "_skill.md"
DEFAULT_TOPICS_FILE = "topics.md"


class RepoError(Exception):
    """A write was rejected: bad id, duplicate, unknown skill, etc."""


@dataclass
class State:
    """Everything the viewer and the agent need, parsed once."""

    root: Path
    role: Role | None = None
    skills: list[Skill] = field(default_factory=list)
    evidence: list[EvidenceFile] = field(default_factory=list)
    conclusions: Conclusions = field(default_factory=Conclusions)
    roadmap: Roadmap = field(default_factory=Roadmap)
    events: list[Event] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)

    # ---- derived views -------------------------------------------------

    def skill(self, skill_id: str) -> Skill | None:
        return next((s for s in self.skills if s.id == skill_id), None)

    @property
    def all_topics(self) -> list[Topic]:
        return [topic for skill in self.skills for topic in skill.topics]

    def summary(self) -> dict[str, Any]:
        topics = self.all_topics
        counts = {status: 0 for status in STATUSES}
        for topic in topics:
            if topic.status in counts:
                counts[topic.status] += 1
        earned = sum(STATUS_WEIGHTS.get(t.status, 0.0) for t in topics)
        min_required = [t for t in topics if t.min_required]
        return {
            "overall_percent": round(100 * earned / len(topics), 1) if topics else 0.0,
            "total_topics": len(topics),
            "counts": counts,
            "min_bar": {
                "total": len(min_required),
                "met": sum(1 for t in min_required if t.meets_min_bar),
            },
            "coverage": coverage(topics),
        }

    def evidence_status(self) -> dict[str, list[str]]:
        return evidence_mod.evidence_status(self.evidence, self.conclusions)

    def roadmap_view(self, *, today: _date | None = None) -> dict[str, Any]:
        return roadmap_mod.derive_roadmap(self.roadmap, self.all_topics, today=today or _date.today())

    def velocity_view(self, *, today: _date | None = None) -> dict[str, Any]:
        return velocity_mod.compute(
            self.events,
            self.all_topics,
            today=today or _date.today(),
            target_date=self.roadmap.target_date,
            start_date=self.roadmap.start_date,
        )

    def history_view(self, limit: int = 40) -> dict[str, Any]:
        """Recent events, enriched with the titles the UI wants to display."""
        topics = {t.id: t for t in self.all_topics}
        skills = {s.id: s for s in self.skills}

        recent = []
        for event in reversed(self.events[-limit:]):
            payload = event.to_dict()
            topic = topics.get(event.topic_id)
            skill = skills.get(event.skill_id)
            payload["topic_title"] = topic.title if topic else event.topic_id
            payload["skill_name"] = skill.name if skill else event.skill_id
            recent.append(payload)

        return {"total_events": len(self.events), "recent": recent}

    def to_dict(self) -> dict[str, Any]:
        """The full JSON payload served at ``/api/state`` and pushed over SSE."""
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "role": self.role.to_dict() if self.role else None,
            "skills": [skill.to_dict() for skill in self.skills],
            "focus": [topic.to_dict() for topic in self.all_topics if topic.focus],
            "summary": self.summary(),
            "conclusions": self.conclusions.to_dict(),
            "evidence_status": self.evidence_status(),
            "evidence_files": [item.to_dict() for item in self.evidence],
            "roadmap": self.roadmap_view(),
            "velocity": self.velocity_view(),
            "history": self.history_view(),
            "git": git_status(self.root),
            "issues": [issue.to_dict() for issue in self.issues],
        }


class Repo:
    """Read/write access to one skill-tracker repo."""

    def __init__(self, root: Path | str | None = None) -> None:
        self.root = find_repo_root(root)

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self) -> State:
        """Parse the whole repo. Never raises for bad content — see ``issues``."""
        state = State(root=self.root)

        role, role_issues = self._load_role()
        state.role = role
        state.issues.extend(role_issues)

        skills, skill_issues = self._load_skills()
        state.issues.extend(skill_issues)
        state.skills = self._order_skills(skills, role)

        files, evidence_issues = evidence_mod.scan_evidence(self.root)
        state.evidence = files
        state.issues.extend(evidence_issues)

        conclusions, conclusion_issues = evidence_mod.load_conclusions(self.root)
        state.conclusions = conclusions
        state.issues.extend(conclusion_issues)

        plan, roadmap_issues = roadmap_mod.load_roadmap(self.root)
        state.roadmap = plan
        state.issues.extend(roadmap_issues)
        state.issues.extend(
            roadmap_mod.validate_roadmap(plan, state.all_topics, [s.id for s in state.skills])
        )

        events, history_issues = history_mod.read_events(self.root)
        state.events = events
        state.issues.extend(history_issues)

        # Cross-file checks live in validate.py to keep loading dumb.
        from .validate import cross_check

        state.issues.extend(cross_check(state))
        return state

    def _load_role(self) -> tuple[Role | None, list[Issue]]:
        path = self.root / ROLE_FILE
        if not path.is_file():
            return None, [Issue("error", f"missing {ROLE_FILE}", ROLE_FILE)]

        try:
            meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
        except ParseError as exc:
            return None, [Issue("error", f"{ROLE_FILE}: {exc}", ROLE_FILE)]

        issues: list[Issue] = []
        order = meta.pop("skill_order", []) or []
        if not isinstance(order, list):
            issues.append(Issue("error", f"{ROLE_FILE}: skill_order must be a list", ROLE_FILE))
            order = []

        role = Role(
            role=str(meta.pop("role", "") or ""),
            level=str(meta.pop("level", "") or ""),
            updated=meta.pop("updated", None),
            skill_order=[str(item) for item in order],
            notes=body.strip("\n"),
            extra=meta,
        )
        if not role.role:
            issues.append(Issue("warning", f"{ROLE_FILE}: no 'role' set", ROLE_FILE))
        return role, issues

    def _load_skills(self) -> tuple[list[Skill], list[Issue]]:
        issues: list[Issue] = []
        skills: list[Skill] = []
        skills_root = self.root / SKILLS_DIR
        if not skills_root.is_dir():
            return skills, [Issue("error", f"missing {SKILLS_DIR}/ directory", SKILLS_DIR)]

        for folder in sorted(p for p in skills_root.iterdir() if p.is_dir() and not p.name.startswith(".")):
            skill, skill_issues = self._load_skill(folder)
            issues.extend(skill_issues)
            if skill is not None:
                skills.append(skill)
        return skills, issues

    def _load_skill(self, folder: Path) -> tuple[Skill | None, list[Issue]]:
        issues: list[Issue] = []
        meta_path = folder / SKILL_META_FILE
        rel_meta = relative_to_root(self.root, meta_path)

        meta: dict[str, Any] = {}
        body = ""
        if meta_path.is_file():
            try:
                meta, body = split_frontmatter(meta_path.read_text(encoding="utf-8"))
            except ParseError as exc:
                issues.append(Issue("error", f"{rel_meta}: {exc}", rel_meta))
        else:
            issues.append(Issue("warning", f"skill '{folder.name}': missing {SKILL_META_FILE}", rel_meta))

        skill_id = str(meta.pop("id", "") or folder.name)
        if skill_id != folder.name:
            issues.append(
                Issue("error", f"{rel_meta}: id '{skill_id}' does not match folder name '{folder.name}'", rel_meta)
            )
            skill_id = folder.name

        priority = meta.pop("priority", 999)
        if isinstance(priority, bool) or not isinstance(priority, int):
            issues.append(Issue("error", f"{rel_meta}: priority must be an integer", rel_meta))
            priority = 999

        skill = Skill(
            id=skill_id,
            name=str(meta.pop("name", "") or skill_id.replace("-", " ").title()),
            priority=priority,
            updated=meta.pop("updated", None),
            description=body.strip("\n"),
            extra=meta,
        )

        for topic_file in self._topic_files(folder):
            rel = relative_to_root(self.root, topic_file)
            parsed, file_issues = parse_topics(
                topic_file.read_text(encoding="utf-8"), path=rel, skill_id=skill.id
            )
            issues.extend(file_issues)
            for topic in parsed.topics:
                topic.skill_name = skill.name
                skill.topics.append(topic)

        if not skill.topics:
            issues.append(Issue("warning", f"skill '{skill.id}': no topics found", relative_to_root(self.root, folder)))

        skill.topics.sort(key=lambda t: (t.priority if isinstance(t.priority, int) else 999, t.title.lower()))
        return skill, issues

    @staticmethod
    def _topic_files(folder: Path) -> list[Path]:
        """Any number of ``*.md`` files per skill, except the ``_``-prefixed meta."""
        return sorted(p for p in folder.glob("*.md") if not p.name.startswith("_"))

    @staticmethod
    def _order_skills(skills: list[Skill], role: Role | None) -> list[Skill]:
        """Display order: role.skill_order first, then leftovers by priority."""
        by_id = {skill.id: skill for skill in skills}
        ordered: list[Skill] = []
        seen: set[str] = set()

        for skill_id in (role.skill_order if role else []):
            skill = by_id.get(skill_id)
            if skill is not None and skill.id not in seen:
                ordered.append(skill)
                seen.add(skill.id)

        leftovers = [s for s in skills if s.id not in seen]
        leftovers.sort(key=lambda s: (s.priority, s.name.lower()))
        return ordered + leftovers

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def _write(self, path: Path, text: str) -> None:
        """Atomic write, so the file watcher never sees a half-written file."""
        path = safe_path(self.root, path)
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        )
        try:
            with handle:
                handle.write(text)
            os.replace(handle.name, path)
        except BaseException:
            Path(handle.name).unlink(missing_ok=True)
            raise

    def _commit(self, *events: Event) -> None:
        """Record events, then regenerate ROADMAP.md.

        Every write path ends here, which is what guarantees the generated
        roadmap can never be stale relative to the data.
        """
        history_mod.append_events(self.root, events)
        self.refresh_roadmap_doc()

    def refresh_roadmap_doc(self) -> str:
        """Rewrite the generated ``ROADMAP.md`` from current state."""
        state = self.load()
        text = render_roadmap_doc(state.to_dict(), state.events, today=_date.today())
        self._write(self.root / ROADMAP_DOC, text)
        return ROADMAP_DOC

    def _skill_folder(self, skill_id: str) -> Path:
        folder = safe_path(self.root, SKILLS_DIR, skill_id)
        if not folder.is_dir():
            raise RepoError(f"unknown skill '{skill_id}'")
        return folder

    def _load_topic_files(self, folder: Path, skill_id: str) -> list[TopicFile]:
        parsed_files: list[TopicFile] = []
        for path in self._topic_files(folder):
            parsed, _ = parse_topics(
                path.read_text(encoding="utf-8"), path=relative_to_root(self.root, path), skill_id=skill_id
            )
            parsed_files.append(parsed)
        return parsed_files

    def _touch_skill(self, folder: Path) -> None:
        """Bump ``updated:`` on a skill's ``_skill.md``."""
        meta_path = folder / SKILL_META_FILE
        if not meta_path.is_file():
            return
        try:
            meta, body = split_frontmatter(meta_path.read_text(encoding="utf-8"))
        except ParseError:
            return
        meta["updated"] = today()
        self._write(meta_path, join_frontmatter(meta, body))

    # -- topics ---------------------------------------------------------

    def update_topic_status(
        self, skill_id: str, topic_id: str, status: str, note: str | None = None
    ) -> dict[str, Any]:
        """Set a topic's status and append a dated log line."""
        if status not in STATUSES:
            raise RepoError(f"invalid status '{status}'; expected one of {', '.join(STATUSES)}")

        folder = self._skill_folder(skill_id)
        for parsed in self._load_topic_files(folder, skill_id):
            topic = next((t for t in parsed.topics if t.id == topic_id), None)
            if topic is None:
                continue

            previous = topic.status
            topic.status = status
            topic.updated = today()
            log_note = note.strip() if note else f"status {previous} → {status}"
            append_log_entry(topic, log_note, date=today())

            self._write(self.root / parsed.path, serialize_topics(parsed))
            self._touch_skill(folder)
            self._commit(
                Event(
                    ts=utc_now(),
                    type=history_mod.STATUS_CHANGE,
                    skill_id=skill_id,
                    topic_id=topic_id,
                    from_status=previous,
                    to_status=status,
                    note=note.strip() if note else "",
                )
            )
            return {
                "skill_id": skill_id,
                "topic_id": topic_id,
                "previous_status": previous,
                "status": status,
                "file": parsed.path,
                "logged": log_note,
            }

        raise RepoError(f"unknown topic '{topic_id}' in skill '{skill_id}'")

    def add_topic(
        self,
        skill_id: str,
        title: str,
        *,
        topic_id: str | None = None,
        status: str = "not-started",
        priority: int | None = None,
        min_required: bool = False,
        focus: bool = False,
        evidence: Iterable[str] = (),
        enough: Iterable[str] = (),
        notes: str = "",
        file: str | None = None,
    ) -> dict[str, Any]:
        """Add a new topic section to a skill's topic file."""
        if status not in STATUSES:
            raise RepoError(f"invalid status '{status}'; expected one of {', '.join(STATUSES)}")
        title = title.strip()
        if not title:
            raise RepoError("topic title is required")

        folder = self._skill_folder(skill_id)
        new_id = (topic_id or slugify(title)).strip()

        state = self.load()
        if any(t.id == new_id for t in state.all_topics):
            raise RepoError(f"topic id '{new_id}' already exists in this repo")

        parsed_files = self._load_topic_files(folder, skill_id)
        if file:
            target = next((p for p in parsed_files if Path(p.path).name == file), None)
            if target is None:
                target = TopicFile(path=relative_to_root(self.root, folder / file))
                parsed_files.append(target)
        elif parsed_files:
            target = parsed_files[0]
        else:
            target = TopicFile(path=relative_to_root(self.root, folder / DEFAULT_TOPICS_FILE))
            parsed_files.append(target)

        if priority is None:
            existing = [t.priority for t in target.topics if isinstance(t.priority, int)]
            priority = (max(existing) + 1) if existing else 1

        body_parts = []
        enough_lines = [line.strip() for line in enough if line and line.strip()]
        if enough_lines:
            body_parts.append('### What "enough" looks like\n' + "\n".join(f"- {line}" for line in enough_lines))
        log_lines = [f"- {today()}: topic added"]
        if notes.strip():
            log_lines.append(f"- {today()}: {notes.strip()}")
        body_parts.append("### Notes / log\n" + "\n".join(log_lines))

        topic = Topic(
            id=new_id,
            title=title,
            status=status,
            priority=priority,
            min_required=min_required,
            focus=focus,
            updated=today(),
            evidence=[str(item) for item in evidence],
            body="\n\n".join(body_parts),
            skill_id=skill_id,
        )
        target.topics.append(topic)
        target.topics.sort(key=lambda t: (t.priority if isinstance(t.priority, int) else 999, t.title.lower()))

        self._write(self.root / target.path, serialize_topics(target))
        self._touch_skill(folder)
        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.TOPIC_ADDED,
                skill_id=skill_id,
                topic_id=new_id,
                to_status=status,
                note=notes.strip(),
                data={"title": title, "min_required": min_required},
            )
        )
        return {"skill_id": skill_id, "topic_id": new_id, "file": target.path, "priority": priority}

    def set_focus(self, targets: Iterable[tuple[str, str]], *, clear_existing: bool = True) -> dict[str, Any]:
        """Mark topics as ``focus: true``, optionally clearing all previous flags."""
        wanted = {(skill_id, topic_id) for skill_id, topic_id in targets}

        state = self.load()
        known = {(t.skill_id, t.id) for t in state.all_topics}
        missing = sorted(f"{s}/{t}" for s, t in wanted - known)
        if missing:
            raise RepoError(f"unknown topic(s): {', '.join(missing)}")

        touched_skills = {skill_id for skill_id, _ in wanted}
        if clear_existing:
            touched_skills |= {t.skill_id for t in state.all_topics if t.focus}

        now_focused: list[str] = []
        cleared: list[str] = []
        for skill_id in sorted(touched_skills):
            folder = self._skill_folder(skill_id)
            for parsed in self._load_topic_files(folder, skill_id):
                changed = False
                for topic in parsed.topics:
                    should_focus = (skill_id, topic.id) in wanted
                    if should_focus and not topic.focus:
                        topic.focus = True
                        topic.updated = today()
                        changed = True
                    elif clear_existing and topic.focus and not should_focus:
                        topic.focus = False
                        topic.updated = today()
                        changed = True
                        cleared.append(f"{skill_id}/{topic.id}")
                    if topic.focus:
                        now_focused.append(f"{skill_id}/{topic.id}")
                if changed:
                    self._write(self.root / parsed.path, serialize_topics(parsed))

        focused = sorted(set(now_focused))
        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.FOCUS_SET,
                data={"focused": focused, "cleared": sorted(set(cleared))},
            )
        )
        return {"focused": focused, "cleared": sorted(set(cleared))}

    # -- skills / role ---------------------------------------------------

    def add_skill(
        self,
        skill_id: str,
        name: str,
        *,
        priority: int | None = None,
        description: str = "",
    ) -> dict[str, Any]:
        """Create a skill folder, its ``_skill.md`` and an empty ``topics.md``."""
        skill_id = slugify(skill_id or name)
        folder = safe_path(self.root, SKILLS_DIR, skill_id)
        if folder.exists():
            raise RepoError(f"skill '{skill_id}' already exists")

        state = self.load()
        order = list(state.role.skill_order) if state.role else []
        # Keep the stored order honest before inserting into it.
        order = [item for item in order if any(s.id == item for s in state.skills)]

        if priority is None or priority < 1 or priority > len(order) + 1:
            priority = len(order) + 1
        order.insert(priority - 1, skill_id)

        self._write(
            folder / SKILL_META_FILE,
            join_frontmatter(
                {"id": skill_id, "name": name.strip() or skill_id, "priority": priority, "updated": today()},
                (description.strip() or f"Topics covering {name}.") + "\n",
            ),
        )
        self._write(folder / DEFAULT_TOPICS_FILE, f"<!-- Topics for {name}. See MASTER.md for the format. -->\n")

        self.update_role_order(order)
        self._renumber_skill_priorities(order)
        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.SKILL_ADDED,
                skill_id=skill_id,
                data={"name": name, "priority": priority},
            )
        )
        return {"skill_id": skill_id, "priority": priority, "skill_order": order}

    def update_role_order(self, skill_order: list[str]) -> dict[str, Any]:
        """Rewrite ``skill_order`` in role.md and re-sync each skill's priority."""
        path = self.root / ROLE_FILE
        if not path.is_file():
            raise RepoError(f"missing {ROLE_FILE}")

        known = {folder.name for folder in (self.root / SKILLS_DIR).iterdir() if folder.is_dir()}
        unknown = [item for item in skill_order if item not in known]
        if unknown:
            raise RepoError(f"unknown skill id(s) in skill_order: {', '.join(unknown)}")
        if len(set(skill_order)) != len(skill_order):
            raise RepoError("skill_order contains duplicates")

        missing = sorted(known - set(skill_order))
        order = list(skill_order) + missing

        meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
        meta["skill_order"] = order
        meta["updated"] = today()
        self._write(path, join_frontmatter(meta, body))
        self._renumber_skill_priorities(order)
        # Reordering changes how the generated roadmap reads, so refresh it.
        self.refresh_roadmap_doc()
        return {"skill_order": order, "appended_missing": missing}

    def _renumber_skill_priorities(self, order: list[str]) -> None:
        """Keep each ``_skill.md`` priority equal to its 1-based position."""
        for index, skill_id in enumerate(order, start=1):
            meta_path = safe_path(self.root, SKILLS_DIR, skill_id, SKILL_META_FILE)
            if not meta_path.is_file():
                continue
            try:
                meta, body = split_frontmatter(meta_path.read_text(encoding="utf-8"))
            except ParseError:
                continue
            if meta.get("priority") == index:
                continue
            meta["priority"] = index
            meta["updated"] = today()
            self._write(meta_path, join_frontmatter(meta, body))

    # -- checklists ------------------------------------------------------

    def _edit_topic(self, skill_id: str, topic_id: str, mutate):
        """Load the topic's file, apply ``mutate(topic)``, write it back.

        ``mutate`` returns a result to hand back to the caller, or ``None`` to
        abandon the write.
        """
        folder = self._skill_folder(skill_id)
        for parsed in self._load_topic_files(folder, skill_id):
            topic = next((t for t in parsed.topics if t.id == topic_id), None)
            if topic is None:
                continue
            result = mutate(topic)
            if result is None:
                return None
            topic.updated = today()
            self._write(self.root / parsed.path, serialize_topics(parsed))
            self._touch_skill(folder)
            return result
        raise RepoError(f"unknown topic '{topic_id}' in skill '{skill_id}'")

    def set_checklist_item(self, skill_id: str, topic_id: str, item_id: str, checked: bool) -> dict[str, Any]:
        """Tick or untick one checklist item inside a topic."""
        captured: dict[str, Any] = {}

        def mutate(topic: Topic):
            outcome = checklist_mod.set_item(topic.body, item_id, checked)
            if outcome is None:
                known = ", ".join(i.id for i in topic.checklist.items) or "none"
                raise RepoError(f"unknown checklist item '{item_id}' in topic '{topic_id}'. Known items: {known}")
            body, item = outcome
            if body == topic.body:
                # Already in the requested state — do not churn the file.
                captured["item"] = item.to_dict()
                captured["changed"] = False
                return None
            topic.body = body
            captured["item"] = item.to_dict()
            captured["changed"] = True
            return captured

        result = self._edit_topic(skill_id, topic_id, mutate)
        if result is None:
            # Unchanged: report current state without touching disk or history.
            state = self.load()
            topic = next((t for t in state.all_topics if t.id == topic_id), None)
            return {
                "skill_id": skill_id,
                "topic_id": topic_id,
                "changed": False,
                "item": captured.get("item"),
                "checklist": topic.checklist.to_dict() if topic else None,
            }

        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.CHECKLIST_ITEM,
                skill_id=skill_id,
                topic_id=topic_id,
                note=("checked" if checked else "unchecked") + f": {captured['item']['text']}",
                data={"item_id": item_id, "checked": checked},
            )
        )

        state = self.load()
        topic = next((t for t in state.all_topics if t.id == topic_id), None)
        return {
            "skill_id": skill_id,
            "topic_id": topic_id,
            "changed": True,
            "item": captured["item"],
            "checklist": topic.checklist.to_dict() if topic else None,
        }

    def add_checklist_items(
        self,
        skill_id: str,
        topic_id: str,
        items: Iterable[str],
        *,
        section: str = checklist_mod.DEFAULT_SECTION,
    ) -> dict[str, Any]:
        """Append concrete, ordered items to a topic's checklist."""
        texts = [str(text) for text in items if str(text).strip()]
        if not texts:
            raise RepoError("no checklist items supplied")

        captured: dict[str, Any] = {}

        def mutate(topic: Topic):
            body, added = checklist_mod.add_items(topic.body, texts, section=section)
            captured["added"] = added
            captured["skipped"] = len(texts) - len(added)
            if not added:
                return None
            topic.body = body
            return captured

        result = self._edit_topic(skill_id, topic_id, mutate)
        if result is None:
            return {"skill_id": skill_id, "topic_id": topic_id, "added": [], "skipped": captured.get("skipped", 0)}

        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.CHECKLIST_ADDED,
                skill_id=skill_id,
                topic_id=topic_id,
                note=f"added {len(captured['added'])} checklist item(s)",
                data={"item_ids": captured["added"], "section": section},
            )
        )

        state = self.load()
        topic = next((t for t in state.all_topics if t.id == topic_id), None)
        return {
            "skill_id": skill_id,
            "topic_id": topic_id,
            "added": captured["added"],
            "skipped": captured["skipped"],
            "checklist": topic.checklist.to_dict() if topic else None,
        }

    # -- roadmap ---------------------------------------------------------

    def _write_roadmap(self, plan: Roadmap) -> None:
        plan.updated = today()
        self._write(self.root / roadmap_mod.ROADMAP_FILE, roadmap_mod.serialize_roadmap(plan))

    def set_roadmap_meta(
        self,
        *,
        start_date: str | None = None,
        target_date: str | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        """Set the roadmap's overall window and intro prose."""
        plan, _ = roadmap_mod.load_roadmap(self.root)
        plan.exists = True

        for label, value in (("start_date", start_date), ("target_date", target_date)):
            if value is not None:
                if value and not roadmap_mod._parse_date(value):
                    raise RepoError(f"{label} '{value}' is not a YYYY-MM-DD date")
                setattr(plan, label, value or None)

        if notes is not None:
            plan.notes = notes.strip("\n")

        self._write_roadmap(plan)
        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.MILESTONE_SET,
                note="roadmap window updated",
                data={"start_date": plan.start_date, "target_date": plan.target_date},
            )
        )
        return {"start_date": plan.start_date, "target_date": plan.target_date, "milestones": len(plan.milestones)}

    def set_milestone(
        self,
        milestone_id: str,
        *,
        title: str | None = None,
        target: str | None = None,
        status: str | None = None,
        skills: Iterable[str] | None = None,
        topics: Iterable[str] | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create or update one milestone. Only supplied fields are changed."""
        milestone_id = slugify(milestone_id or title or "")
        if not milestone_id:
            raise RepoError("milestone id or title is required")

        plan, _ = roadmap_mod.load_roadmap(self.root)
        plan.exists = True
        existing = plan.milestone(milestone_id)
        created = existing is None

        if created and not title:
            raise RepoError(f"milestone '{milestone_id}' does not exist yet — supply a title to create it")

        if status is not None and status not in roadmap_mod.MILESTONE_STATUSES:
            raise RepoError(
                f"invalid milestone status '{status}'; expected one of {', '.join(roadmap_mod.MILESTONE_STATUSES)}"
            )
        if target and not roadmap_mod._parse_date(target):
            raise RepoError(f"target '{target}' is not a YYYY-MM-DD date")

        # Referencing something that does not exist is a mistake worth catching
        # at write time rather than leaving as a dangling id in the file.
        state = self.load()
        known_topics = {t.id for t in state.all_topics}
        known_skills = {s.id for s in state.skills}
        if topics is not None:
            unknown = sorted(set(topics) - known_topics)
            if unknown:
                raise RepoError(f"unknown topic id(s): {', '.join(unknown)}")
        if skills is not None:
            unknown = sorted(set(skills) - known_skills)
            if unknown:
                raise RepoError(f"unknown skill id(s): {', '.join(unknown)}")

        milestone = existing or Milestone(id=milestone_id, title=title or milestone_id)
        if title is not None:
            milestone.title = title
        if target is not None:
            milestone.target = target or None
        if status is not None:
            milestone.status = status
        if skills is not None:
            milestone.skills = [str(s) for s in skills]
        if topics is not None:
            milestone.topics = [str(t) for t in topics]
        if description is not None:
            milestone.description = description.strip("\n")

        if created:
            plan.milestones.append(milestone)

        self._write_roadmap(plan)
        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.MILESTONE_SET,
                note=("created" if created else "updated") + f" milestone '{milestone.title}'",
                data={"milestone_id": milestone_id, "created": created, "target": milestone.target},
            )
        )

        derived = roadmap_mod.derive_milestone(milestone, state.all_topics, today=_date.today())
        return {"milestone_id": milestone_id, "created": created, "milestone": derived}

    def remove_milestone(self, milestone_id: str) -> dict[str, Any]:
        plan, _ = roadmap_mod.load_roadmap(self.root)
        milestone = plan.milestone(milestone_id)
        if milestone is None:
            known = ", ".join(m.id for m in plan.milestones) or "none"
            raise RepoError(f"unknown milestone '{milestone_id}'. Known milestones: {known}")

        plan.milestones = [m for m in plan.milestones if m.id != milestone_id]
        self._write_roadmap(plan)
        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.MILESTONE_REMOVED,
                note=f"removed milestone '{milestone.title}'",
                data={"milestone_id": milestone_id},
            )
        )
        return {"milestone_id": milestone_id, "remaining": len(plan.milestones)}

    def log_activity(
        self,
        note: str,
        *,
        skill_id: str = "",
        topic_id: str = "",
    ) -> dict[str, Any]:
        """Record a free-text event without changing any status.

        For study sessions and observations that belong in the timeline but do
        not, on their own, justify moving a topic's status.
        """
        note = note.strip()
        if not note:
            raise RepoError("note is required")

        if topic_id:
            state = self.load()
            if not any(t.id == topic_id for t in state.all_topics):
                raise RepoError(f"unknown topic '{topic_id}'")

        event = Event(ts=utc_now(), type=history_mod.NOTE, skill_id=skill_id, topic_id=topic_id, note=note)
        self._commit(event)
        return {"logged": event.to_dict()}

    # -- evidence --------------------------------------------------------

    def read_evidence(self, path: str) -> dict[str, Any]:
        """Read one raw evidence file, by path relative to ``evidence/``."""
        rel = path.strip().lstrip("/")
        if rel.startswith("evidence/"):
            rel = rel[len("evidence/") :]
        target = safe_path(self.root, evidence_mod.EVIDENCE_DIR, rel)
        if not target.is_file():
            raise RepoError(f"no evidence file at 'evidence/{rel}'")

        text = target.read_text(encoding="utf-8")
        meta, body = split_frontmatter(text)
        return {
            "path": rel,
            "source": meta.get("source", ""),
            "url": meta.get("url", ""),
            "added": meta.get("added"),
            "hash": evidence_mod.hash_text(text),
            "content": body.strip("\n"),
        }

    def write_conclusions(self, content: str) -> dict[str, Any]:
        """Overwrite CONCLUSIONS.md and refresh its evidence hash manifest."""
        if not content.strip():
            raise RepoError("conclusions content is empty")

        missing = evidence_mod.check_conclusions_structure(content)
        files, _ = evidence_mod.scan_evidence(self.root)
        existing, _ = evidence_mod.load_conclusions(self.root)
        extra = {k: v for k, v in existing.extra.items() if k != "updated"}

        path = self.root / evidence_mod.EVIDENCE_DIR / evidence_mod.CONCLUSIONS_FILE
        self._write(path, evidence_mod.render_conclusions(content, files, updated=today(), extra=extra))
        self._commit(
            Event(
                ts=utc_now(),
                type=history_mod.CONCLUSIONS_UPDATED,
                data={"evidence_files": len(files), "missing_sections": missing},
            )
        )
        return {
            "path": f"{evidence_mod.EVIDENCE_DIR}/{evidence_mod.CONCLUSIONS_FILE}",
            "evidence_files_recorded": len(files),
            "missing_sections": missing,
        }
