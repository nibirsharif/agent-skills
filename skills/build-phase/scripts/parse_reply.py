#!/usr/bin/env python3
"""Parse the reply of verify-spec or implement-task into data, or say why it is not a valid reply.

Usage: python3 parse_reply.py verify|implement [--strict] [--requirements PATH] [FILE]
       (reads standard input without FILE)

Prints one JSON object and exits 0 when the reply is valid, or exits 1 and prints {"kind": "invalid",
"problems": [...]}. The producer is strict, the consumer tolerant: by default the report, the done report,
or the stop line is found anywhere in the reply, so a sentence before it does not make the reply invalid,
and a verify report whose Tally line miscounts its rows is valid, with the tally counted from the rows.
--strict also fails a reply that has text outside the contract or a wrong Tally; the evals use it.
--requirements (verify only) names the requirements.md the report is of: the report must then have exactly
one row for every ID in it, in file order, as a whole-file or phase report does (not for one named ID).

kind is one of:
  report  (verify)     rows [{id, verdict, evidence}], tests, tally (counted from the rows), drift,
                       warnings (only when there are any, such as a Tally line that miscounts)
  done    (implement)  task, title, covers, changed, check, commit
  stop                 line: the one enumerated stop line, word for word; for implement also relay: the
                       line as build-phase passes it on, with "run implement-task again" made "run build-phase again"
  invalid              problems; for verify, also rows when the table had any, so a gap in a rejected
                       report can be compared with the retry

Python 3 standard library only.
"""

import json
import re
import sys

VERDICTS = ["met", "partial", "unmet", "untested", "cannot tell", "skipped"]
HEADER = "| ID | Verdict | Evidence |"
SEPARATOR = "|----|---------|----------|"
REQ_LINE = re.compile(r"^((?:FR|NFR)-\d+):", re.M)
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


def invalid(*problems, rows=None):
    result = {"kind": "invalid", "problems": list(problems)}
    if rows:
        result["rows"] = rows
    return result


def requirement_ids(text):
    """The requirement IDs of a requirements.md, in file order, read as verify-spec's check_scope.py reads them."""
    return list(dict.fromkeys(REQ_LINE.findall(text)))


def id_problems(rows, ids):
    """Why the rows are not exactly one row per ID of the file, in file order; empty when they are."""
    got = [r["id"] for r in rows]
    problems = []
    duplicated = [i for i in dict.fromkeys(got) if got.count(i) > 1]
    if duplicated:
        problems.append("more than one row for " + ", ".join(duplicated))
    unknown = [i for i in dict.fromkeys(got) if i not in ids]
    if unknown:
        problems.append("rows for IDs that are not in the requirements file: " + ", ".join(unknown))
    missing = [i for i in ids if i not in got]
    if missing:
        problems.append("no row for " + ", ".join(missing))
    if not problems and got != ids:
        problems.append("the rows are not in file order")
    return problems


def parse_verify(text, strict=False, ids=None):
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
    elif ids is not None:
        problems += id_problems(rows, ids)
    fields = {}
    for name in ("Tests", "Tally", "Drift"):
        found = [l for l in after if l.startswith(name + ": ")]
        if len(found) != 1:
            problems.append(f"expected one {name} line, found {len(found)}")
        else:
            fields[name.lower()] = found[0][len(name) + 2:]
    if problems:
        return invalid(*problems, rows=rows)
    counts = {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS}
    expected = ", ".join(f"{n} {v}" for v, n in counts.items() if n)
    warnings = []
    if fields["tally"] != expected:
        (problems if strict else warnings).append(f"the tally is {fields['tally']!r}, the rows give {expected!r}")
        fields["tally"] = expected
    for r in rows:
        if r["verdict"] == "met" and not (re.search(r"\S+:\d+", r["evidence"]) and "passed" in r["evidence"]):
            problems.append(f"{r['id']} is met without a path:line and a passed test")
    if strict:
        if start:
            problems.append("text before the table")
        if len(after) != 3 or [l.split(":")[0] for l in after] != ["Tests", "Tally", "Drift"]:
            problems.append("after the table there must be exactly a Tests, a Tally, and a Drift line")
    if problems:
        return invalid(*problems, rows=rows)
    return {"kind": "report", "rows": rows, **fields, **({"warnings": warnings} if warnings else {})}


DONE = re.compile(r"^(T-\d+\.\d+) done: (.+)$")
DONE_FIELDS = ["Covers", "Changed", "Check", "Commit"]


def relay(stop):
    """The stop line as build-phase passes it on: the user reruns build-phase, not implement-task."""
    return stop.replace("then run implement-task again.", "then run build-phase again.")


def parse_implement(text, strict=False):
    lines = lines_of(text)
    starts = [i for i, l in enumerate(lines) if DONE.match(l)]
    if not starts:
        stop = find_stop(lines, IMPLEMENT_STOPS)
        if stop:
            extra = [l for l in lines if l != stop]
            if strict and extra:
                return invalid("text outside the stop line")
            return {"kind": "stop", "line": stop, "relay": relay(stop)}
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


USAGE = "Usage: parse_reply.py verify|implement [--strict] [--requirements PATH] [FILE]"


def usage(message=None):
    print((message + "\n" if message else "") + __doc__.split("\n\n")[0] + "\n" + USAGE, file=sys.stderr)
    return 2


def main(argv):
    args, flags, requirements, i = [], set(), None, 0
    while i < len(argv):
        a = argv[i]
        if a == "--requirements" and i + 1 < len(argv):
            requirements, i = argv[i + 1], i + 2
            continue
        if a.startswith("--requirements="):
            requirements = a.split("=", 1)[1]
        elif a.startswith("--"):
            flags.add(a)
        else:
            args.append(a)
        i += 1
    if not args or args[0] not in ("verify", "implement") or len(args) > 2 or flags - {"--strict"}:
        return usage()
    if requirements is not None and args[0] != "verify":
        return usage("--requirements is for verify only")
    ids = None
    if requirements is not None:
        try:
            ids = requirement_ids(open(requirements).read())
        except OSError as e:
            return usage(f"cannot read {requirements}: {e.strerror}")
        if not ids:
            return usage(f"{requirements} has no FR or NFR requirements")
    text = open(args[1]).read() if len(args) == 2 else sys.stdin.read()
    if args[0] == "verify":
        result = parse_verify(text, strict="--strict" in flags, ids=ids)
    else:
        result = parse_implement(text, strict="--strict" in flags)
    print(json.dumps(result, indent=2))
    return 1 if result["kind"] == "invalid" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
