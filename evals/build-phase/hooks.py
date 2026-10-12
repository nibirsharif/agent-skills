"""build-phase's own reply checks, run on every case except one with "fires": false.

The reply is the summary and nothing else: the Phase line first, then Branch, Tasks, Verify, and a Stopped
or Next line as the contract says.
"""

import re

LINES = [
    r"Phase \S+ of \S+: (done|stopped)",
    r"Branch: \S+",
    r"Tasks: \d+ implemented, \d+ reworked",
    r"Verify: .+",
    r"Stopped: .+",
    r"Next: push \S+, open a PR titled \".+\", and run /code-review",
]


def check(reply):
    lines = [l for l in reply.strip().splitlines() if l.strip()]
    problems = []
    if not lines or not re.fullmatch(LINES[0], lines[0]):
        problems.append("the first line is not the Phase line")
    for line in lines:
        if not any(re.fullmatch(p, line) for p in LINES):
            problems.append(f"text outside the summary: {line[:60]}")
    stopped = bool(lines) and lines[0].endswith(": stopped")
    has = lambda label: any(l.startswith(label) for l in lines)
    if stopped and not has("Stopped:"):
        problems.append("a stopped run needs a Stopped line")
    if not stopped and has("Stopped:"):
        problems.append("a Stopped line on a run that is done")
    if has("Next:") and stopped:
        problems.append("a Next line on a stopped run")
    return problems
