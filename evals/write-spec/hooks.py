"""write-spec's own reply checks: the skill's lint must find no errors, and the reply holds only
requirement lines, question lines, and the "N more open questions" line."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("lint", ROOT / "skills" / "write-spec" / "scripts" / "lint.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


def check(reply):
    failures = []
    linter = lint.Linter(lint.banned_patterns())
    linter.lint("reply", reply)
    for where, level, ident, message in linter.findings:
        if level == "ERROR":
            failures.append(f"lint: {where} {ident}: {message}")

    for line in reply.splitlines():
        if line.strip() and not re.match(r"(FR|NFR|Q)-\d+\b|\d+ more open questions after these\b", line):
            failures.append(f"text outside the requirements and questions: {line[:100]}")
            break
    return failures
