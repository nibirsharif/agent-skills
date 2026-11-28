#!/usr/bin/env python3
"""Count how large a spec is: the requirements after the follow-up turn, or a saved file's requirements by source.

Usage: python3 evals/write-spec/benchmark/size.py <label> [<label> ...]
       python3 evals/write-spec/benchmark/size.py --file <requirements.md>

With labels, reads the follow-up replies bench.py saved in evals/write-spec/runs/bench-<label>/ from a run
with --file turn2.md: <input>.md, or <input>-r1.md, <input>-r2.md, ... from a run with --runs. For each reply
it prints the statements of the input (the `Statements: <n>` line of its reference.md), the requirements the
fixed first reply in turn2.md holds, the requirements the reply adds (`(new)`) and withdraws, the requirements
after the turn for each statement, and the questions still open, with the `<N> more open questions` the reply
holds back. Which of the new requirements come from a coverage-gap answer is counted by hand, with the list in
each reference-turn2.md.

With --file, reads a requirements file write-spec saved and counts its written requirements by the first
source their `<!-- Source: ... -->` comment names:

- statement: a statement of the input, first or added later;
- answer: the answer to a question about a statement;
- coverage gap: the answer to a question whose own source is `coverage gap in <ID>`;
- answer to an answer: the answer to a question whose own source is another answer.

It also counts the coverage-gap questions by where the requirement they name came from, which is what a limit
on the depth of coverage gaps would cut. Python 3 standard library only.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

STATEMENTS = re.compile(r"^Statements: (\d+)\b", re.M)
REQUIREMENT = re.compile(r"^((?:FR|NFR)-\d+)(?: \((new|changed)\))?: (.*)$", re.M)
QUESTION = re.compile(r"^(Q-\d+): (.*)$", re.M)
HELD_BACK = re.compile(r"^(\d+) more open questions? after these\.", re.M)
SOURCE = re.compile(r"<!-- Source: (.*?) -->\s*$")
ANSWER = re.compile(r"\banswers? to (Q-\d+)")
GAP = re.compile(r"\bcoverage gap in ((?:FR|NFR)-\d+)")
KINDS = ["statement", "answer", "coverage gap", "answer to an answer"]


def first_reply(turn2):
    """The IDs of the requirements the fixed first reply holds."""
    reply = turn2.split("You replied:", 1)[-1].split("My answers:", 1)[0]
    return [m.group(1) for m in REQUIREMENT.finditer(reply)]


def size(statements, before, reply):
    """One follow-up reply's counts. A requirement line without a marker counts as new when its ID is new."""
    new, withdrawn, changed = [], [], []
    for req, marker, text in REQUIREMENT.findall(reply):
        if text.startswith("Withdrawn"):
            withdrawn.append(req)
        elif marker == "new" or (not marker and req not in before):
            new.append(req)
        else:
            changed.append(req)
    held = HELD_BACK.search(reply)
    return {
        "statements": statements,
        "before": len(before),
        "new": len(new),
        "changed": len(changed),
        "withdrawn": len(withdrawn),
        "after": len(before) + len(new) - len(withdrawn),
        "questions": len(QUESTION.findall(reply)) + (int(held.group(1)) if held else 0),
    }


def by_source(text):
    """A saved file's written requirements by source kind, and its coverage-gap questions by the kind of the
    requirement they name."""
    sources, written = {}, []
    for line in text.splitlines():
        found = re.match(r"((?:FR|NFR|Q)-\d+): (.*)$", line)
        source = SOURCE.search(line)
        if not found or not source:
            continue
        sources[found.group(1)] = source.group(1)
        if not found.group(1).startswith("Q") and not found.group(2).startswith("Withdrawn"):
            written.append(found.group(1))

    def first(pattern, source):
        found = pattern.search(source)
        return (found.start(), found.group(1)) if found else None

    def kind(req):
        source = sources[req]
        answer = first(ANSWER, source)
        # The first source named decides: `added input, ...; answer to Q-005` is a statement.
        if not answer or source[:answer[0]].strip(" ,;"):
            return "statement"
        asked = sources.get(answer[1], "")
        if GAP.search(asked):
            return "coverage gap"
        return "answer to an answer" if ANSWER.search(asked) else "answer"

    kinds = {req: kind(req) for req in written}
    gaps = {}
    for q, source in sources.items():
        named = GAP.search(source) if q.startswith("Q") else None
        if named:
            gaps[q] = kinds.get(named.group(1), "a requirement the file does not have")
    return {"requirements": kinds, "gap_questions": gaps}


def replies_of(run_dir, name):
    """An input's replies, in run order: <name>-r1.md, <name>-r2.md, ..., or the single <name>.md."""
    numbered = sorted(run_dir.glob(f"{name}-r*.md"), key=lambda p: int(p.stem.rsplit("-r", 1)[1]))
    single = run_dir / f"{name}.md"
    return numbered or ([single] if single.is_file() else [])


def row(label, s):
    return (f"| {label} | {s['statements']} | {s['before']} | {s['new']} | {s['withdrawn']} | {s['after']} | "
            f"{s['after'] / s['statements']:.2f} | {s['questions']} |")


def report_file(path):
    counted = by_source(Path(path).read_text())
    kinds = list(counted["requirements"].values())
    print(f"{len(kinds)} written requirements")
    for kind in KINDS:
        ids = [req for req, k in counted["requirements"].items() if k == kind]
        print(f"- {kind}: {len(ids)}" + (f" ({', '.join(ids)})" if ids else ""))
    gaps = counted["gap_questions"]
    print(f"{len(gaps)} coverage-gap questions, by the source of the requirement each names")
    for kind in sorted(set(gaps.values()), key=lambda k: KINDS.index(k) if k in KINDS else len(KINDS)):
        ids = [q for q, k in gaps.items() if k == kind]
        print(f"- {kind}: {len(ids)} ({', '.join(ids)})")
    return 0 if kinds else 1


def main(argv):
    if len(argv) == 2 and argv[0] == "--file":
        return report_file(argv[1])
    if not argv or argv[0].startswith("-"):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    names = sorted(p.name for p in HERE.iterdir() if (p / "turn2.md").is_file())
    sums = {}
    print("| Reply | Statements | Requirements before | New | Withdrawn | After | After, for each statement | Questions open |")
    print("|---|---|---|---|---|---|---|---|")
    for label in argv:
        run_dir = HERE.parent / "runs" / f"bench-{label}"
        for name in names:
            statements = int(STATEMENTS.search((HERE / name / "reference.md").read_text()).group(1))
            before = first_reply((HERE / name / "turn2.md").read_text())
            for path in replies_of(run_dir, name):
                s = size(statements, before, path.read_text())
                print(row(f"{label}/{path.stem}", s))
                for group in (name.split("-")[0], "all"):
                    total = sums.setdefault(group, {"replies": 0})
                    for key, value in s.items():
                        total[key] = total.get(key, 0) + value
                    total["replies"] += 1
    for group in sorted(sums, key=lambda g: (g == "all", g)):
        print(row(f"**{group}, {sums[group]['replies']} replies**", sums[group]))
    return 0 if sums else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
