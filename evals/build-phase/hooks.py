"""build-phase's own reply checks, run on every case except one with "fires": false.

The reply is the summary and nothing else: the Phase line first, then Branch, Tasks, Verify, any Check by hand
lines, and a Stopped or Next line as the contract says.

Two things are graded apart, so a run shows which one went wrong. Each failure starts with its name:

- "summary: ...": the summary lines themselves are wrong (check_summary).
- "outside the summary: ...": the summary is wrapped in other text, such as a sentence before it (check_outside).
"""

import re

LINES = [
    r"Phase \S+ of \S+: (done|stopped)",
    r"Branch: \S+",
    r"Tasks: \d+ implemented, \d+ reworked",
    r"Verify: .+",
    r"Check by hand: (?:FR|NFR)-\d+: .+",
    r"Stopped: .+",
    r"Next: push \S+, open a PR titled \".+\", and run /code-review",
]


def is_summary_line(line):
    return any(re.fullmatch(p, line) for p in LINES)


def split(reply):
    """The reply's non-blank lines as (summary lines, other lines with where each one is)."""
    lines = [l for l in reply.strip().splitlines() if l.strip()]
    at = [i for i, l in enumerate(lines) if is_summary_line(l)]
    summary = [lines[i] for i in at]
    other = []
    for i, line in enumerate(lines):
        if i in at:
            continue
        where = "instead of" if not at else "before" if i < at[0] else "after" if i > at[-1] else "inside"
        other.append((where, line))
    return summary, other


def check_summary(reply):
    """Problems with the summary lines, wherever they are in the reply."""
    summary, _ = split(reply)
    phase = [l for l in summary if re.fullmatch(LINES[0], l)]
    if not phase:
        return ["summary: no Phase line"]
    problems = []
    if summary[0] != phase[0]:
        problems.append("summary: the Phase line is not its first line")
    if len(phase) > 1:
        problems.append("summary: more than one Phase line")
    stopped = phase[0].endswith(": stopped")
    has = lambda label: any(l.startswith(label) for l in summary)
    if stopped and not has("Stopped:"):
        problems.append("summary: a stopped run needs a Stopped line")
    if not stopped and has("Stopped:"):
        problems.append("summary: a Stopped line on a run that is done")
    if has("Next:") and stopped:
        problems.append("summary: a Next line on a stopped run")
    return problems


def check_outside(reply):
    """Every line of the reply that is not a summary line."""
    _, other = split(reply)
    return [f"outside the summary: text {where} it: {line[:60]}" for where, line in other]


def check(reply):
    return check_summary(reply) + check_outside(reply)
