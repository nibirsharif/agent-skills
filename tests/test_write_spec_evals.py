"""Tests for evals/write-spec: every golden reply passes its checks and every bad reply fails."""

import importlib.util
import json
import re
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent.parent / "evals" / "write-spec"
spec = importlib.util.spec_from_file_location("grade", EVALS / "grade.py")
grade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grade)
CASES = sorted(p for p in (EVALS / "cases").iterdir() if p.is_dir())
spec = importlib.util.spec_from_file_location("parse_run", EVALS / "parse_run.py")
parse_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parse_run)


class EvalCases(unittest.TestCase):
    def test_cases_exist(self):
        self.assertGreaterEqual(len(CASES), 4)

    def test_case_files_and_patterns(self):
        for case in CASES:
            with self.subTest(case=case.name):
                for name in ("input.md", "checks.json", "golden.md"):
                    self.assertTrue((case / name).is_file(), name)
                checks = json.loads((case / "checks.json").read_text())
                for check in checks.get("must_match", []) + checks.get("must_not_match", []):
                    re.compile(check["pattern"])
                    self.assertTrue(check.get("why"), check["pattern"])

    def test_golden_replies_pass(self):
        for case in CASES:
            with self.subTest(case=case.name):
                failures, _ = grade.grade(case, (case / "golden.md").read_text())
                self.assertEqual(failures, [])

    def test_bad_replies_fail(self):
        for case in CASES:
            if (case / "bad.md").is_file():
                with self.subTest(case=case.name):
                    failures, _ = grade.grade(case, (case / "bad.md").read_text())
                    self.assertTrue(failures)



class ParseRun(unittest.TestCase):
    def test_counts_lint_runs_and_blocks(self):
        def use(i, command):
            return {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": i, "name": "Bash", "input": {"command": command}}]}}

        def result(i, error):
            return {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": i, "is_error": error, "content": "x"}]}}

        events = [
            use("a", "cat <<'EOF' | python3 skills/write-spec/scripts/lint.py -"), result("a", True),
            use("b", "python3 skills/write-spec/scripts/lint.py - <<'EOF'"), result("b", False),
            use("c", "ls"), result("c", False),
            {"type": "system", "subtype": "permission_denied", "message": "Redirect target is runtime-determined"},
            {"type": "user", "message": {"content": "plain text"}},
            {"type": "result", "result": "REQ-001: ...", "num_turns": 4},
        ]
        final, ran, blocked = parse_run.summarize(events)
        self.assertEqual((final["num_turns"], ran, blocked), (4, 1, 1))


if __name__ == "__main__":
    unittest.main()
