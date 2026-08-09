"""Evidence scanning, content hashing and the CONCLUSIONS.md staleness diff."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .markdown import ParseError, join_frontmatter, split_frontmatter
from .models import Conclusions, EvidenceFile, Issue

#: Sub-directory of the repo holding all evidence.
EVIDENCE_DIR = "evidence"
CONCLUSIONS_FILE = "CONCLUSIONS.md"
RAW_DIR = "raw"


def hash_text(text: str) -> str:
    """sha256 of the file's content, newline-normalised.

    Normalising line endings means a checkout on a different platform does not
    make every evidence file look "modified".
    """
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def scan_evidence(root: Path) -> tuple[list[EvidenceFile], list[Issue]]:
    """Read every markdown file under ``evidence/raw/``."""
    issues: list[Issue] = []
    files: list[EvidenceFile] = []
    raw_root = root / EVIDENCE_DIR / RAW_DIR
    if not raw_root.is_dir():
        return files, issues

    for path in sorted(raw_root.rglob("*.md")):
        if path.name.startswith("."):
            continue
        rel = path.relative_to(root / EVIDENCE_DIR).as_posix()
        text = path.read_text(encoding="utf-8")
        try:
            meta, body = split_frontmatter(text)
        except ParseError as exc:
            issues.append(Issue("warning", f"evidence '{rel}': {exc}", f"{EVIDENCE_DIR}/{rel}"))
            meta, body = {}, text

        if not meta.get("source"):
            issues.append(
                Issue("warning", f"evidence '{rel}': missing 'source' in frontmatter", f"{EVIDENCE_DIR}/{rel}")
            )

        files.append(
            EvidenceFile(
                path=rel,
                source=str(meta.get("source", "") or ""),
                url=str(meta.get("url", "") or ""),
                added=meta.get("added"),
                sha256=hash_text(text),
                body=body,
            )
        )
    return files, issues


def load_conclusions(root: Path) -> tuple[Conclusions, list[Issue]]:
    """Read ``evidence/CONCLUSIONS.md`` if it exists."""
    issues: list[Issue] = []
    path = root / EVIDENCE_DIR / CONCLUSIONS_FILE
    rel = f"{EVIDENCE_DIR}/{CONCLUSIONS_FILE}"
    if not path.is_file():
        return Conclusions(exists=False), issues

    text = path.read_text(encoding="utf-8")
    try:
        meta, body = split_frontmatter(text)
    except ParseError as exc:
        issues.append(Issue("error", f"{rel}: {exc}", rel))
        return Conclusions(exists=True, content=text), issues

    considered_raw = meta.pop("evidence_files_considered", []) or []
    considered: list[dict[str, str]] = []
    if isinstance(considered_raw, list):
        for entry in considered_raw:
            if isinstance(entry, dict) and entry.get("path"):
                considered.append({"path": str(entry["path"]), "hash": str(entry.get("hash", ""))})
            else:
                issues.append(Issue("warning", f"{rel}: bad entry in evidence_files_considered: {entry!r}", rel))
    else:
        issues.append(Issue("error", f"{rel}: evidence_files_considered must be a list", rel))

    return (
        Conclusions(
            exists=True,
            updated=meta.pop("updated", None),
            considered=considered,
            content=body.strip("\n"),
            extra=meta,
        ),
        issues,
    )


def evidence_status(files: list[EvidenceFile], conclusions: Conclusions) -> dict[str, list[str]]:
    """Diff current evidence hashes against the manifest in CONCLUSIONS.md.

    This is what tells the agent which evidence it still needs to read.
    """
    recorded = {entry["path"]: entry.get("hash", "") for entry in conclusions.considered}
    current = {item.path: item.sha256 for item in files}

    new = sorted(path for path in current if path not in recorded)
    modified = sorted(path for path, digest in current.items() if path in recorded and recorded[path] != digest)
    deleted = sorted(path for path in recorded if path not in current)
    unchanged = sorted(path for path, digest in current.items() if recorded.get(path) == digest)

    return {"new": new, "modified": modified, "deleted": deleted, "unchanged": unchanged}


def render_conclusions(content: str, files: list[EvidenceFile], *, updated: str, extra: dict[str, Any] | None = None) -> str:
    """Build the CONCLUSIONS.md text with a freshly computed hash manifest."""
    front: dict[str, Any] = {"updated": updated}
    front.update(extra or {})
    front["evidence_files_considered"] = [{"path": item.path, "hash": item.sha256} for item in files]
    return join_frontmatter(front, content.strip("\n") + "\n")


#: Sections the plan requires CONCLUSIONS.md to carry (§5.2). Missing ones are
#: reported as warnings, not hard failures — the agent may build up over time.
REQUIRED_CONCLUSION_SECTIONS = (
    "Skill priority ranking",
    "Minimum bar",
    "Per-skill topic requirements",
    "Open contradictions",
)


def check_conclusions_structure(content: str) -> list[str]:
    """Return the names of required sections missing from ``content``."""
    lowered = content.lower()
    return [name for name in REQUIRED_CONCLUSION_SECTIONS if name.lower() not in lowered]
