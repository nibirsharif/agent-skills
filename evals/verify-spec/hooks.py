"""verify-spec's own reply checks, run on every case except one with "fires": false.

The reply is either one stop line, or the report: the table, then the Tests, Tally, and Drift lines, and
nothing else. The checks that need no judgement: the shape, the verdict words, the tally against the rows,
and that a `met` row cites a line and a passing test.
"""

import re

VERDICTS = ["met", "partial", "unmet", "untested", "cannot tell", "skipped"]
STOPS = [
    r"No requirements file found at \S+\. Run write-spec first, then run verify-spec again\.",
    r"\S+ has no FR or NFR requirements\. Run write-spec first, then run verify-spec again\.",
    r"No requirement (?:FR|NFR)-\d+ in \S+\.",
    r"No phase \d+ in \S+\.",
    r"No plan file found at \S+, so phase \d+ has no requirements list\. Run write-plan first, then run verify-spec again\.",
]
ROW = re.compile(r"^\| ((?:FR|NFR)-\d+) \| (" + "|".join(VERDICTS) + r") \| (.+) \|$")


def check(reply):
    text = reply.strip()
    if any(re.fullmatch(stop, text) for stop in STOPS):
        return []
    lines = text.split("\n")
    failures = []
    if lines[:2] != ["| ID | Verdict | Evidence |", "|----|---------|----------|"]:
        return ["the reply is neither a stop line nor a report starting with the table header"]
    rows, rest = [], []
    for line in lines[2:]:
        match = ROW.match(line)
        if match and not rest:
            rows.append(match.groups())
        else:
            rest.append(line)
    if not rows:
        failures.append("the table has no valid rows")
    if len(rest) != 3 or not rest[0].startswith("Tests: ") or not rest[1].startswith("Tally: ") or not rest[2].startswith("Drift: "):
        failures.append("after the table there must be exactly a Tests line, a Tally line, and a Drift line")
        return failures
    counts = {v: sum(1 for r in rows if r[1] == v) for v in VERDICTS}
    expected = ", ".join(f"{n} {v}" for v, n in counts.items() if n)
    if rest[1] != f"Tally: {expected}":
        failures.append(f"the tally is {rest[1]!r}, the rows give 'Tally: {expected}'")
    for id_, verdict, evidence in rows:
        if verdict == "met" and not (re.search(r"\S+:\d+", evidence) and "passed" in evidence):
            failures.append(f"{id_} is met without a path:line and a passed test")
    return failures
