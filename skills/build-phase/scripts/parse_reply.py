#!/usr/bin/env python3
"""Parse the reply of verify-spec or implement-task into data, or say why it is not a valid reply.

Usage: python3 parse_reply.py verify|implement [--strict] [FILE]     (reads standard input without FILE)

Prints one JSON object and exits 0 when the reply is valid, or exits 1 and prints {"kind": "invalid",
"problems": [...]}. The producer is strict, the consumer tolerant: by default the report, the done report,
or the stop line is found anywhere in the reply, so a sentence before it does not make the reply invalid.
--strict also fails a reply that has text outside the contract; the evals use it.

kind is one of:
  report  (verify)     rows [{id, verdict, evidence}], tests, tally, drift
  done    (implement)  task, title, covers, changed, check, commit
  stop                 line: the one enumerated stop line, word for word
  invalid              problems

Python 3 standard library only.
"""

import json
import re
import sys

VERDICTS = ["met", "partial", "unmet", "untested", "cannot tell", "skipped"]
HEADER = "| ID | Verdict | Evidence |"
SEPARATOR = "|----|---------|----------|"
ROW = re.compile(r"^\| ((?:FR|NFR)-\d+) \| (" + "|".join(VERDICTS) + r") \| (.+) \|$")

VERIFY_STOPS = [
    r"No requirements file found at \S+\. Run write-spec first, then run verify-spec again\.",
    r"\S+ has no FR or NFR requirements\. Run write-spec first, then run verify-spec again\.",
    r"No requirement (?:FR|NFR)-\d+ in \S+\.",
    r"No phase \d+ in \S+\.",
    r"No plan file found at \S+, so phase \d+ has no requirements list\. Run write-plan first, then run verify-spec again\.",
]
IMPLEMENT_STOPS = [
    r"No tasks file found at \S+\. Run write-tasks first, then run implement-task again\.",
    r"No task T-\d+\.\d+ in \S+\.",
    r"T-\d+\.\d+ is already Done\.",
    r"Every task in \S+ is Done\.",
    r"T-\d+\.\d+ depends on .+, not yet Done\. Implement those first\.",
    r"(?:FR|NFR)-\d+ has no task in \S+\. Add it with write-tasks, then run implement-task again\.",
    r"\S+ has no task Status lines\. Re-run write-tasks to add them, then run implement-task again\.",
    r"Uncommitted changes in .+\. Commit or stash them, then run implement-task again\.",
    r"T-\d+\.\d+ .+\. Fix the task with write-tasks, then run implement-task again\.",
    r"T-\d+\.\d+ is a rework but its check passes and no gap was given\. Pass the failing verify rows, then run implement-task again\.",
    r"T-\d+\.\d+ check failed: .+\. Status stays Todo; the changes are left uncommitted\.",
]


def lines_of(text):
    """Non-empty lines, trimmed, without code-fence lines."""
    return [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("```")]


def find_stop(lines, stops):
    for line in lines:
        if any(re.fullmatch(s, line) for s in stops):
            return line
    return None


def invalid(*problems):
    return {"kind": "invalid", "problems": list(problems)}


def parse_verify(text, strict=False):
    lines = lines_of(text)
    if HEADER not in lines:
        stop = find_stop(lines, VERIFY_STOPS)
        if stop:
            extra = [l for l in lines if l != stop]
            return invalid("text outside the stop line") if strict and extra else {"kind": "stop", "line": stop}
        return invalid("neither a stop line nor a report with the table header")
    start = lines.index(HEADER)
    if lines[start + 1:start + 2] != [SEPARATOR]:
        return invalid("the table header is not followed by the separator line")
    rows, i = [], start + 2
    while i < len(lines) and ROW.match(lines[i]):
        rows.append(dict(zip(("id", "verdict", "evidence"), ROW.match(lines[i]).groups())))
        i += 1
    after = lines[i:]
    problems = []
    if not rows:
        problems.append("the table has no valid rows")
    fields = {}
    for name in ("Tests", "Tally", "Drift"):
        found = [l for l in after if l.startswith(name + ": ")]
        if len(found) != 1:
            problems.append(f"expected one {name} line, found {len(found)}")
        else:
            fields[name.lower()] = found[0][len(name) + 2:]
    if problems:
        return invalid(*problems)
    counts = {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS}
    expected = ", ".join(f"{n} {v}" for v, n in counts.items() if n)
    if fields["tally"] != expected:
        problems.append(f"the tally is {fields['tally']!r}, the rows give {expected!r}")
    for r in rows:
        if r["verdict"] == "met" and not (re.search(r"\S+:\d+", r["evidence"]) and "passed" in r["evidence"]):
            problems.append(f"{r['id']} is met without a path:line and a passed test")
    if strict:
        if start:
            problems.append("text before the table")
        if len(after) != 3 or [l.split(":")[0] for l in after] != ["Tests", "Tally", "Drift"]:
            problems.append("after the table there must be exactly a Tests, a Tally, and a Drift line")
    return invalid(*problems) if problems else {"kind": "report", "rows": rows, **fields}


DONE = re.compile(r"^(T-\d+\.\d+) done: (.+)$")
DONE_FIELDS = ["Covers", "Changed", "Check", "Commit"]


def parse_implement(text, strict=False):
    lines = lines_of(text)
    starts = [i for i, l in enumerate(lines) if DONE.match(l)]
    if not starts:
        stop = find_stop(lines, IMPLEMENT_STOPS)
        if stop:
            extra = [l for l in lines if l != stop]
            return invalid("text outside the stop line") if strict and extra else {"kind": "stop", "line": stop}
        return invalid("neither a stop line nor a done report")
    start = starts[0]
    block = lines[start + 1:start + 5]
    if [l.split(":")[0] for l in block] != DONE_FIELDS:
        return invalid("the done report needs Covers, Changed, Check, and Commit lines right after the first line")
    task, title = DONE.match(lines[start]).groups()
    values = [l.split(": ", 1)[1] if ": " in l else "" for l in block]
    problems = [f"{name} line is empty" for name, v in zip(DONE_FIELDS, values) if not v]
    if strict and (start or len(lines) != 5):
        problems.append("text outside the five-line done report")
    if problems:
        return invalid(*problems)
    covers, changed, check, commit = values
    return {"kind": "done", "task": task, "title": title, "covers": [c.strip() for c in covers.split(",")],
            "changed": [c.strip() for c in changed.split(",")], "check": check, "commit": commit}


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args or args[0] not in ("verify", "implement") or len(args) > 2:
        print(__doc__.split("\n\n")[0] + "\n" + "Usage: parse_reply.py verify|implement [--strict] [FILE]", file=sys.stderr)
        return 2
    text = open(args[1]).read() if len(args) == 2 else sys.stdin.read()
    parse = parse_verify if args[0] == "verify" else parse_implement
    result = parse(text, strict="--strict" in argv)
    print(json.dumps(result, indent=2))
    return 1 if result["kind"] == "invalid" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
