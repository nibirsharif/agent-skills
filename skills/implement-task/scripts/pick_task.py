#!/usr/bin/env python3
"""Find tasks.md and pick the task implement-task works on, or say what to reply when it cannot start.

Usage: python3 pick_task.py [--feature NAME | --path PATH] [--task T-P.N | --requirement ID] [--root DIR]

Run it with the project as the current directory. It finds tasks.md as find_tasks.py does (same folder,
same options), then checks the working tree and picks the task. Prints one of these and exits 0:

  found <path>          two lines: the file to use,
  task <id>[ rework]    and the task to implement; `rework` when the task already has a commit
  stop <line>           <line> is the whole reply: one of the skill's stop lines
  ask <what>            ask the user <what>

--task is the task the user named. --requirement is an FR or NFR ID the user asked for in place of a task:
it stands for the first task not yet Done that builds it (the verify task does not), else the first that
builds it. With neither, the task is the first Todo task in file order whose dependencies are all Done.

Stops, in this order: no tasks file; uncommitted changes outside the feature's folder; no Status lines;
then for a named task: not in the file, already Done, a dependency not Done; for a requirement: no task
covers it; with nothing named: every task Done, or no Todo task with its dependencies Done.

Exits 2 on a usage error. Python 3 standard library only.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import find_tasks  # noqa: E402  (this skill's own lookup script)

TASK = re.compile(r"^#### (T-\d+\.\d+): (.+?)\s*$")
FIELD = re.compile(r"^\*\*(Covers|Files|Depends on|Status):\*\*\s*(.*?)\s*$")
TASK_ID = re.compile(r"T-\d+\.\d+")
REQ_ID = re.compile(r"(?:FR|NFR)-\d+")
FIX = "Fix the task with write-tasks, then run implement-task again."


def read_tasks(text):
    """The tasks of a tasks.md in file order: [{id, title, covers, depends, status, verify}]. status is None when
    missing; verify marks a task with `Files: None.`"""
    tasks, current = [], None
    for line in text.splitlines():
        m = TASK.match(line)
        if m:
            current = {"id": m.group(1), "title": m.group(2), "covers": [], "depends": [], "status": None, "verify": False}
            tasks.append(current)
            continue
        if line.startswith("## ") or line.startswith("### "):
            current = None  # a new section or phase ends the task above it
        m = FIELD.match(line)
        if m and current:
            name, value = m.groups()
            if name == "Covers":
                current["covers"] = REQ_ID.findall(value)
            elif name == "Files":
                current["verify"] = value.rstrip(".").strip() == "None"
            elif name == "Depends on":
                current["depends"] = TASK_ID.findall(value)
            else:
                current["status"] = value
    return tasks


def dirty_outside(root, folder):
    """Paths with uncommitted changes that are not inside the feature's folder, as git status names them.

    The project's .agent-skills-config.yaml is never one: it holds the user's settings for these skills, which
    they may keep out of the repository, and it is never committed with a task.
    """
    # Not find_tasks.git: it trims the output, and the first line's status columns can start with a space.
    out = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True).stdout
    inside = folder.rstrip("/") + "/"
    paths = []
    for line in out.splitlines():
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        if path == ".agent-skills-config.yaml":
            continue
        if path and not path.startswith(inside) and not inside.startswith(path):
            paths.append(path)
    return paths


def pick(tasks, shown, task=None, requirement=None):
    """The line after `found`: `task <id>`, `stop <line>`, or `ask <what>`."""
    if not tasks:
        return f"stop {shown} has no task Status lines. Re-run write-tasks to add them, then run implement-task again."
    if all(t["status"] is None for t in tasks):
        return f"stop {shown} has no task Status lines. Re-run write-tasks to add them, then run implement-task again."
    by_id = {t["id"]: t for t in tasks}

    def waiting(t):
        return [d for d in t["depends"] if d not in by_id or by_id[d]["status"] != "Done"]

    def ready(t):
        if t["status"] not in ("Todo", "Done"):
            return f"stop {t['id']} has no Status of Todo or Done. {FIX}"
        unknown = [d for d in t["depends"] if d not in by_id]
        if unknown:
            return f"stop {t['id']} depends on {', '.join(unknown)}, which is not in the file. {FIX}"
        if waiting(t):
            return f"stop {t['id']} depends on {', '.join(waiting(t))}, not yet Done. Implement those first."
        return None

    if requirement:
        covering = [t for t in tasks if requirement in t["covers"]]
        if not covering:
            return f"stop {requirement} has no task in {shown}. Add it with write-tasks, then run implement-task again."
        # The tasks that build it, not the phase's verify task; the first that is still to do, else the first.
        build = [t for t in covering if not t["verify"]] or covering
        task = next((t["id"] for t in build if t["status"] != "Done"), build[0]["id"])
    if task:
        if task not in by_id:
            return f"stop No task {task} in {shown}."
        chosen = by_id[task]
        if chosen["status"] == "Done":
            return f"stop {task} is already Done."
        return ready(chosen) or f"task {task}"
    todo = [t for t in tasks if t["status"] != "Done"]
    if not todo:
        return f"stop Every task in {shown} is Done."
    for t in todo:
        if t["status"] == "Todo" and not waiting(t):
            return f"task {t['id']}"
    return ready(todo[0]) or f"stop {todo[0]['id']} depends on {', '.join(waiting(todo[0]))}, not yet Done. Implement those first."


def run(root, home, feature=None, path=None, task=None, requirement=None):
    """The text to print."""
    located = find_tasks.find(root, home, feature, path)
    if not located.startswith("found "):
        return located
    shown = located[len("found "):]
    in_repo = bool(find_tasks.git(root, "rev-parse", "--is-inside-work-tree"))
    if in_repo:
        outside = dirty_outside(root, str(Path(shown).parent))
        if outside:
            return f"stop Uncommitted changes in {', '.join(outside)}. Commit or stash them, then run implement-task again."
    result = pick(read_tasks((root / Path(shown).expanduser()).read_text()), shown, task, requirement)
    if not result.startswith("task "):
        return result
    picked = result[len("task "):]
    rework = in_repo and find_tasks.git(root, "log", "--oneline", "-1", "--grep", f"^{re.escape(picked)}:")
    return f"{located}\n{result}{' rework' if rework else ''}"


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1].strip().removeprefix("Usage: "))
    where = parser.add_mutually_exclusive_group()
    where.add_argument("--feature")
    where.add_argument("--path")
    what = parser.add_mutually_exclusive_group()
    what.add_argument("--task")
    what.add_argument("--requirement")
    parser.add_argument("--root")
    args = parser.parse_args(argv)
    if args.feature is not None and (not args.feature.strip() or "/" in args.feature or args.feature in (".", "..")):
        parser.error("--feature is a folder name, without a slash")
    if args.task and not TASK_ID.fullmatch(args.task):
        parser.error("--task is an ID such as T-1.2")
    if args.requirement and not REQ_ID.fullmatch(args.requirement):
        parser.error("--requirement is an ID such as FR-004 or NFR-001")
    root = Path(args.root).resolve() if args.root else find_tasks.project_root(Path.cwd())
    print(run(root, Path.home(), args.feature, args.path, args.task, args.requirement))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
