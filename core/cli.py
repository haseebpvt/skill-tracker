"""Small CLI over ``core``: ``skilltracker validate`` / ``state`` / ``overview``."""

from __future__ import annotations

import argparse
import json
import sys

from .repo import Repo
from .validate import validate


def _add_repo_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", default=None, help="path to the skill-tracker repo (default: auto-detect)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skilltracker", description="Skill tracker repo tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_cmd = subparsers.add_parser("validate", help="check the repo for errors and warnings")
    _add_repo_arg(validate_cmd)
    validate_cmd.add_argument("--json", action="store_true", help="emit JSON instead of text")

    state_cmd = subparsers.add_parser("state", help="dump the full parsed state as JSON")
    _add_repo_arg(state_cmd)

    overview_cmd = subparsers.add_parser("overview", help="print a short progress summary")
    _add_repo_arg(overview_cmd)

    args = parser.parse_args(argv)
    repo = Repo(args.repo)
    state = repo.load()

    if args.command == "state":
        json.dump(state.to_dict(), sys.stdout, indent=2)
        print()
        return 0

    if args.command == "overview":
        summary = state.summary()
        role = state.role
        print(f"{role.role if role else '(no role)'} — {summary['overall_percent']}% overall")
        print(f"Min bar: {summary['min_bar']['met']}/{summary['min_bar']['total']}")
        for skill in state.skills:
            progress = skill.progress()
            print(f"  {skill.priority:>2}. {skill.name:<28} {progress['percent']:>5}%  ({progress['total']} topics)")
        return 0

    report = validate(state)
    if args.json:
        json.dump(report, sys.stdout, indent=2)
        print()
    else:
        for issue in report["errors"]:
            print(f"ERROR  {issue['path']}: {issue['message']}", file=sys.stderr)
        for issue in report["warnings"]:
            print(f"WARN   {issue['path']}: {issue['message']}", file=sys.stderr)
        counts = report["counts"]
        print(f"{counts['errors']} error(s), {counts['warnings']} warning(s)")
    return 0 if report["ok"] else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
