#!/usr/bin/env python3
"""Find requirements.md and check the scope verify-spec was asked for, or say what to reply when it cannot start.

Usage: python3 check_scope.py [--feature NAME | --path PATH] [--id ID | --phase N] [--root DIR]

Run it with the project as the current directory. It finds requirements.md as find_requirements.py does
(same folder, same options), then checks that the named ID or phase exists. Prints one of these and exits 0:

  found <path>      two lines: the file to use,
  scope <what>      and the scope: `all`, `<ID>`, or `phase <n>: <the IDs in that phase's Requirements list>`
  stop <line>       <line> is the whole reply: one of the skill's stop lines
  ask <what>        ask the user <what>

--id is the one requirement the user named (FR-003). --phase is the phase of plan.md the user named.
With neither, the scope is every requirement in the file.

Stops, in this order: no requirements file; no FR or NFR requirement in it; a named ID that is not in the
file; a named phase with no plan.md beside the file; a named phase that plan.md does not have.

Exits 2 on a usage error. Python 3 standard library only.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import find_requirements  # noqa: E402  (this skill's own lookup script)

REQ_LINE = re.compile(r"^((?:FR|NFR)-\d+):", re.M)
REQ_ID = re.compile(r"(?:FR|NFR)-\d+")
PHASE = re.compile(r"^### Phase (\d+):")
PHASE_REQS = re.compile(r"^\*\*Requirements:\*\*\s*(.*)$")


def phases(plan_text):
    """{phase number: the IDs of its Requirements list}, for the `### Phase <n>:` sections of a plan.md."""
    found, current = {}, None
    for line in plan_text.splitlines():
        m = PHASE.match(line)
        if m:
            current = m.group(1)
            found[current] = []
        elif line.startswith("## "):
            current = None
        elif current is not None and not found[current]:
            m = PHASE_REQS.match(line)
            if m:
                found[current] = REQ_ID.findall(m.group(1))
    return found


def scope(root, shown, req_id=None, phase=None):
    """The line after `found`: `scope <what>` or `stop <line>`."""
    ids = REQ_LINE.findall((root / Path(shown).expanduser()).read_text())
    if not ids:
        return f"stop {shown} has no FR or NFR requirements. Run write-spec first, then run verify-spec again."
    if req_id:
        return f"scope {req_id}" if req_id in ids else f"stop No requirement {req_id} in {shown}."
    if phase:
        plan = str(Path(shown).parent / "plan.md")
        try:
            plan_text = (root / Path(plan).expanduser()).read_text()
        except OSError:
            return (f"stop No plan file found at {plan}, so phase {phase} has no requirements list. "
                    "Run write-plan first, then run verify-spec again.")
        listed = phases(plan_text)
        if phase not in listed:
            return f"stop No phase {phase} in {plan}."
        return f"scope phase {phase}: {', '.join(listed[phase])}"
    return "scope all"


def run(root, home, feature=None, path=None, req_id=None, phase=None):
    """The text to print."""
    located = find_requirements.find(root, home, feature, path)
    if not located.startswith("found "):
        return located
    result = scope(root, located[len("found "):], req_id, phase)
    return f"{located}\n{result}" if result.startswith("scope ") else result


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1].strip().removeprefix("Usage: "))
    where = parser.add_mutually_exclusive_group()
    where.add_argument("--feature")
    where.add_argument("--path")
    what = parser.add_mutually_exclusive_group()
    what.add_argument("--id")
    what.add_argument("--phase")
    parser.add_argument("--root")
    args = parser.parse_args(argv)
    if args.feature is not None and (not args.feature.strip() or "/" in args.feature or args.feature in (".", "..")):
        parser.error("--feature is a folder name, without a slash")
    if args.id and not REQ_ID.fullmatch(args.id):
        parser.error("--id is an ID such as FR-003 or NFR-001")
    if args.phase and not args.phase.isdigit():
        parser.error("--phase is a number")
    root = Path(args.root).resolve() if args.root else find_requirements.project_root(Path.cwd())
    print(run(root, Path.home(), args.feature, args.path, args.id, args.phase))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
