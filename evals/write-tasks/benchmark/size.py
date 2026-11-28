#!/usr/bin/env python3
"""Count how many tasks a benchmark run's task lists hold for each requirement.

Usage: python3 evals/write-tasks/benchmark/size.py <label> [<label> ...]

Reads the replies bench.py saved in evals/write-tasks/runs/bench-<label>/: <input>.md, or <input>-r1.md,
<input>-r2.md, ... from a run with --runs. For each reply it prints the requirements of the input (the
`IDs (<n>):` line of its reference.md), the build tasks, the build tasks that cover two or more IDs, and the
IDs no build task covers, then the totals of the dev set, the hold set, and both. The measure is build tasks
per requirement: a phase's verify task is left out, as in the README's other counts.

A phase's verify task is its last task, when that task covers every ID the phase's other tasks cover.

The counting is mechanical. Whether a task that covers several IDs holds one behaviour is still read by hand.
Python 3 standard library only.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

ID = re.compile(r"\b(?:FR|NFR)-\d+\b")
REFERENCE_IDS = re.compile(r"^IDs \((\d+)\):(.*)$", re.M)
PHASE = re.compile(r"^### Phase (\d+)", re.M)
TASK = re.compile(r"^#### (T-\d+\.\d+): (.*)$", re.M)
COVERS = re.compile(r"^\*\*Covers:\*\*(.*)$", re.M)


def read_reference(text):
    """The IDs the input's plan has in its phases."""
    found = REFERENCE_IDS.search(text)
    ids = ID.findall(found.group(2)) if found else []
    if not found or len(ids) != int(found.group(1)):
        raise ValueError("reference.md needs one `IDs (<n>):` line that lists <n> IDs")
    return ids


def tasks_of(reply):
    """The reply's tasks in order: {"id", "title", "phase", "covers", "verify"}."""
    tasks = []
    marks = [(m.start(), "phase", m) for m in PHASE.finditer(reply)] + [(m.start(), "task", m) for m in TASK.finditer(reply)]
    marks.sort(key=lambda mark: mark[0])
    phase = None
    for i, (start, kind, m) in enumerate(marks):
        if kind == "phase":
            phase = m.group(1)
            continue
        body = reply[start:marks[i + 1][0] if i + 1 < len(marks) else len(reply)]
        covers = COVERS.search(body)
        tasks.append({"id": m.group(1), "title": m.group(2).strip(), "phase": phase or m.group(1)[2:].split(".")[0],
                      "covers": ID.findall(covers.group(1)) if covers else [], "verify": False})
    for phase in {t["phase"] for t in tasks}:
        of_phase = [t for t in tasks if t["phase"] == phase]
        built = {i for t in of_phase[:-1] for i in t["covers"]}
        last = of_phase[-1]
        last["verify"] = len(of_phase) > 1 and built <= set(last["covers"])
    return tasks


def size(ids, reply):
    """One reply's counts."""
    tasks = tasks_of(reply)
    build = [t for t in tasks if not t["verify"]]
    covered = {i for t in build for i in t["covers"]}
    return {
        "requirements": len(ids),
        "build": len(build),
        "several": [t["id"] for t in build if len(set(t["covers"])) > 1],
        "uncovered": [i for i in ids if i not in covered],
        "verify": len(tasks) - len(build),
    }


def replies_of(run_dir, name):
    """An input's replies, in run order: <name>-r1.md, <name>-r2.md, ..., or the single <name>.md."""
    numbered = sorted(run_dir.glob(f"{name}-r*.md"), key=lambda p: int(p.stem.rsplit("-r", 1)[1]))
    single = run_dir / f"{name}.md"
    return numbered or ([single] if single.is_file() else [])


def ratio(build, requirements):
    return f"{build / requirements:.2f}" if requirements else "none"


def row(label, s):
    return (f"| {label} | {s['requirements']} | {s['build']} | {ratio(s['build'], s['requirements'])} | {len(s['several'])} | "
            f"{s['requirements'] - len(s['uncovered'])} of {s['requirements']} |"
            + (f"  <- not covered: {', '.join(s['uncovered'])}" if s["uncovered"] else ""))


def add(total, s):
    for key in ("requirements", "build", "verify"):
        total[key] = total.get(key, 0) + s[key]
    for key in ("several", "uncovered"):
        total[key] = total.get(key, []) + s[key]
    total["replies"] = total.get("replies", 0) + 1
    return total


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    names = sorted(p.name for p in HERE.iterdir() if (p / "reference.md").is_file())
    references = {name: read_reference((HERE / name / "reference.md").read_text()) for name in names}
    sums = {}
    print("| Reply | Requirements | Build tasks | Build tasks per requirement | Tasks with two or more IDs | Covered |")
    print("|---|---|---|---|---|---|")
    for label in argv:
        run_dir = HERE.parent / "runs" / f"bench-{label}"
        for name in names:
            for path in replies_of(run_dir, name):
                s = size(references[name], path.read_text())
                print(row(f"{label}/{path.stem}", s))
                for group in (name.split("-")[0], "all"):
                    sums[group] = add(sums.get(group, {}), s)
    for group in sorted(sums, key=lambda g: (g == "all", g)):
        print(row(f"**{group}, {sums[group]['replies']} replies**", sums[group]))
    return 0 if sums else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
