"""Tests for skills/build-phase/scripts/parse_reply.py: the tolerant parse the driver uses and the strict one the evals use."""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "build-phase" / "scripts" / "parse_reply.py"
spec = importlib.util.spec_from_file_location("parse_reply", SCRIPT)
pr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr)

REPORT = """| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | met | textstats/counts.py:17; tests/test_counts.py::test_x passed |
| FR-002 | untested | textstats/counts.py:15; no test |
Tests: python3 -m unittest: 4 tests OK
Tally: 1 met, 1 untested
Drift: none"""

DONE = """T-1.2 done: Reject text that is not a string
Covers: FR-002
Changed: textstats/counts.py, tests/test_counts.py
Check: python3 -m unittest: 6 tests OK
Commit: 4b1e9a2 on reading-time/phase-1"""

STOP = "No requirement FR-009 in docs/specs/x/requirements.md."


class Verify(unittest.TestCase):
    def test_report(self):
        r = pr.parse_verify(REPORT, strict=True)
        self.assertEqual(r["kind"], "report")
        self.assertEqual([x["id"] for x in r["rows"]], ["FR-001", "FR-002"])
        self.assertEqual(r["drift"], "none")

    def test_narration_before_is_tolerated_but_not_strict(self):
        text = "Now I have everything.\n\n" + REPORT
        self.assertEqual(pr.parse_verify(text)["kind"], "report")
        self.assertEqual(pr.parse_verify(text, strict=True)["kind"], "invalid")

    def test_fenced_report_is_tolerated(self):
        self.assertEqual(pr.parse_verify("```\n" + REPORT + "\n```")["kind"], "report")

    def test_stop_line(self):
        self.assertEqual(pr.parse_verify(STOP, strict=True), {"kind": "stop", "line": STOP})
        self.assertEqual(pr.parse_verify("I looked.\n" + STOP)["kind"], "stop")
        self.assertEqual(pr.parse_verify("I looked.\n" + STOP, strict=True)["kind"], "invalid")

    def test_wrong_tally_and_unproven_met(self):
        self.assertEqual(pr.parse_verify(REPORT.replace("1 met, 1 untested", "2 met"))["kind"], "invalid")
        bad = REPORT.replace("textstats/counts.py:17; tests/test_counts.py::test_x passed", "looks fine")
        self.assertEqual(pr.parse_verify(bad)["kind"], "invalid")

    def test_missing_line_or_garbage(self):
        self.assertEqual(pr.parse_verify(REPORT.rsplit("\n", 1)[0])["kind"], "invalid")
        self.assertEqual(pr.parse_verify("All requirements look met.")["kind"], "invalid")


class Implement(unittest.TestCase):
    def test_done(self):
        r = pr.parse_implement(DONE, strict=True)
        self.assertEqual((r["kind"], r["task"], r["covers"]), ("done", "T-1.2", ["FR-002"]))
        self.assertEqual(r["changed"], ["textstats/counts.py", "tests/test_counts.py"])

    def test_narration_is_tolerated_but_not_strict(self):
        text = "T-1.4 depends on T-1.2, so I did it first.\n\n" + DONE
        self.assertEqual(pr.parse_implement(text)["task"], "T-1.2")
        self.assertEqual(pr.parse_implement(text, strict=True)["kind"], "invalid")

    def test_stop_lines(self):
        for line in ["T-1.2 is already Done.", "Every task in a/tasks.md is Done.",
                     "T-1.4 depends on T-1.2, T-1.3, not yet Done. Implement those first.",
                     "Uncommitted changes in textstats/counts.py. Commit or stash them, then run implement-task again.",
                     "T-1.2 check failed: python3 -m unittest: 1 failure. Status stays Todo; the changes are left uncommitted."]:
            with self.subTest(line=line):
                self.assertEqual(pr.parse_implement(line, strict=True), {"kind": "stop", "line": line})

    def test_incomplete_report_and_questions(self):
        self.assertEqual(pr.parse_implement(DONE.rsplit("\n", 1)[0])["kind"], "invalid")
        self.assertEqual(pr.parse_implement("Which message should the error use?")["kind"], "invalid")


class Cli(unittest.TestCase):
    def run_cli(self, mode, text):
        return subprocess.run([sys.executable, str(SCRIPT), mode], input=text, capture_output=True, text=True)

    def test_exit_codes(self):
        ok = self.run_cli("verify", REPORT)
        self.assertEqual((ok.returncode, json.loads(ok.stdout)["kind"]), (0, "report"))
        bad = self.run_cli("implement", "nothing useful")
        self.assertEqual((bad.returncode, json.loads(bad.stdout)["kind"]), (1, "invalid"))
        self.assertEqual(self.run_cli("other", "").returncode, 2)


if __name__ == "__main__":
    unittest.main()
