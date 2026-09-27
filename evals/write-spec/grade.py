#!/usr/bin/env python3
"""Grade a write-spec reply against one eval case.

Usage: python3 grade.py <case-dir> <reply-file>

Runs the skill's lint on the reply (0 errors required), then the case's checks.json:
no text besides ID lines and the "N more open questions" line,
requirement and open-question counts, patterns that must appear, and patterns that must not.
Prints the case's manual checklist for a person to review. Exits 1 when any automatic check fails.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("lint", ROOT / "skills" / "write-spec" / "scripts" / "lint.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


def grade(case_dir, reply):
    """Return (failures, manual) for a reply. Each failure is one line of text."""
    checks = json.loads((Path(case_dir) / "checks.json").read_text())
    failures = []

    linter = lint.Linter(lint.banned_patterns())
    linter.lint("reply", reply)
    for where, level, ident, message in linter.findings:
        if level == "ERROR":
            failures.append(f"lint: {where} {ident}: {message}")

    for line in reply.splitlines():
        if line.strip() and not re.match(r"(REQ|Q)-\d+\b|\d+ more open questions after these\b", line):
            failures.append(f"text outside the requirements and questions: {line[:100]}")
            break

    counts = {
        "requirements": len(re.findall(r"^REQ-\d+", reply, re.M)),
        "questions": len(re.findall(r"^Q-\d+: (?!Closed\.)", reply, re.M)),
    }
    for kind, count in counts.items():
        bounds = checks.get(kind, {})
        if count < bounds.get("min", 0) or count > bounds.get("max", float("inf")):
            failures.append(f"{kind}: {count}, expected {bounds.get('min', 0)} to {bounds.get('max', 'any')}")

    for check in checks.get("must_match", []):
        if not re.search(check["pattern"], reply, re.M):
            failures.append(f"missing: {check['why']}")
    for check in checks.get("must_not_match", []):
        m = re.search(check["pattern"], reply, re.M)
        if m:
            line = reply[m.start():].split("\n", 1)[0]
            failures.append(f"present: {check['why']}\n    {line[:120]}")
    return failures, checks.get("manual", [])


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    case_dir, reply_file = argv
    failures, manual = grade(case_dir, Path(reply_file).read_text())
    for failure in failures:
        print(f"FAIL {failure}")
    if manual:
        print("\nReview by hand:")
        for item in manual:
            print(f"- [ ] {item}")
    print(f"\n{Path(case_dir).name}: {'FAIL' if failures else 'PASS'} ({len(failures)} automatic checks failed)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
