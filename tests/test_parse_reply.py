"""Tests for skills/build-phase/scripts/parse_reply.py: the tolerant parse the driver uses and the strict one the evals use."""

import importlib.util
import json
import subprocess
import tempfile
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

    def test_wrong_tally_is_recounted_but_not_strict(self):
        text = REPORT.replace("1 met, 1 untested", "2 met")
        r = pr.parse_verify(text)
        self.assertEqual((r["kind"], r["tally"]), ("report", "1 met, 1 untested"))
        self.assertEqual(r["warnings"], ["the tally is '2 met', the rows give '1 met, 1 untested'"])
        self.assertNotIn("warnings", pr.parse_verify(REPORT))
        self.assertEqual(pr.parse_verify(text, strict=True)["kind"], "invalid")

    def test_unproven_met_is_invalid_and_keeps_its_rows(self):
        bad = REPORT.replace("textstats/counts.py:17; tests/test_counts.py::test_x passed", "looks fine")
        bad = bad.replace("| FR-002 | untested |", "| FR-002 | partial |").replace("1 untested", "1 partial")
        r = pr.parse_verify(bad)
        self.assertEqual(r["kind"], "invalid")
        self.assertEqual([(x["id"], x["verdict"]) for x in r["rows"]], [("FR-001", "met"), ("FR-002", "partial")])
        self.assertNotIn("rows", pr.parse_verify("All requirements look met."))

    def test_missing_line_or_garbage(self):
        self.assertEqual(pr.parse_verify(REPORT.rsplit("\n", 1)[0])["kind"], "invalid")
        self.assertEqual(pr.parse_verify("All requirements look met.")["kind"], "invalid")


REQUIREMENTS = """# Requirements Specification: Text stats

## 3. Functional Requirements

FR-001: The counter shall count words. <!-- Source: x -->

FR-002: If the text is not a string, then the counter shall reject it. <!-- Source: x -->

FR-003: Withdrawn.

## 4. Non-Functional Requirements

NFR-001: The counter shall count 1 MB of text within 1 second. <!-- Source: x -->
"""
IDS = ["FR-001", "FR-002", "FR-003", "NFR-001"]
PHASE_REPORT = """| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | met | textstats/counts.py:17; tests/test_counts.py::test_x passed |
| FR-002 | untested | textstats/counts.py:15; no test |
| FR-003 | skipped | outside phase 1 |
| NFR-001 | skipped | outside phase 1 |
Tests: python3 -m unittest: 4 tests OK
Tally: 1 met, 1 untested, 2 skipped
Drift: none"""


class Ids(unittest.TestCase):
    def test_requirement_ids_in_file_order(self):
        self.assertEqual(pr.requirement_ids(REQUIREMENTS), IDS)

    def test_every_id_once_in_order(self):
        r = pr.parse_verify(PHASE_REPORT, strict=True, ids=IDS)
        self.assertEqual(r["kind"], "report")

    def test_left_out_skipped_rows_are_invalid_and_keep_the_rows(self):
        # The real run's retry: only the phase's rows, none of the skipped ones (issue #3).
        r = pr.parse_verify(REPORT, ids=IDS)
        self.assertEqual(r["kind"], "invalid")
        self.assertEqual(r["problems"], ["no row for FR-003, NFR-001"])
        self.assertEqual([x["id"] for x in r["rows"]], ["FR-001", "FR-002"])
        self.assertEqual(pr.parse_verify(REPORT)["kind"], "report")

    def test_duplicate_unknown_and_order(self):
        rows = PHASE_REPORT.splitlines()
        dup = "\n".join(rows[:3] + rows[2:])
        self.assertIn("more than one row for FR-001", pr.parse_verify(dup, ids=IDS)["problems"])
        unknown = PHASE_REPORT.replace("| NFR-001 |", "| NFR-009 |")
        self.assertEqual(pr.parse_verify(unknown, ids=IDS)["problems"],
                         ["rows for IDs that are not in the requirements file: NFR-009", "no row for NFR-001"])
        swapped = "\n".join(rows[:4] + [rows[5], rows[4]] + rows[6:])
        self.assertEqual(pr.parse_verify(swapped, ids=IDS)["problems"], ["the rows are not in file order"])


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
                     "T-1.2 check failed: python3 -m unittest: 1 failure. Status stays Todo; the changes are left uncommitted.",
                     "T-1.2 cannot run its tests: PostgreSQL on localhost:5432 is not available "
                     "(uv run pytest: 11 errors at setup, connection refused). Make it available, then run implement-task again."]:
            with self.subTest(line=line):
                result = pr.parse_implement(line, strict=True)
                self.assertEqual((result["kind"], result["line"]), ("stop", line))
                self.assertEqual(result["relay"], line.replace("run implement-task again", "run build-phase again"))
                self.assertNotIn("implement-task", result["relay"])

    def test_incomplete_report_and_questions(self):
        self.assertEqual(pr.parse_implement(DONE.rsplit("\n", 1)[0])["kind"], "invalid")
        self.assertEqual(pr.parse_implement("Which message should the error use?")["kind"], "invalid")


class Cli(unittest.TestCase):
    def run_cli(self, mode, text, *options):
        return subprocess.run([sys.executable, str(SCRIPT), mode, *options], input=text, capture_output=True, text=True)

    def test_exit_codes(self):
        ok = self.run_cli("verify", REPORT)
        self.assertEqual((ok.returncode, json.loads(ok.stdout)["kind"]), (0, "report"))
        bad = self.run_cli("implement", "nothing useful")
        self.assertEqual((bad.returncode, json.loads(bad.stdout)["kind"]), (1, "invalid"))
        self.assertEqual(self.run_cli("other", "").returncode, 2)

    def test_requirements_option(self):
        with tempfile.TemporaryDirectory() as d:
            req = Path(d) / "requirements.md"
            req.write_text(REQUIREMENTS)
            ok = self.run_cli("verify", PHASE_REPORT, "--requirements", str(req))
            self.assertEqual((ok.returncode, json.loads(ok.stdout)["kind"]), (0, "report"))
            bad = self.run_cli("verify", REPORT, f"--requirements={req}")
            self.assertEqual((bad.returncode, json.loads(bad.stdout)["problems"]), (1, ["no row for FR-003, NFR-001"]))
            self.assertEqual(self.run_cli("verify", REPORT, "--requirements", str(Path(d) / "none.md")).returncode, 2)
            self.assertEqual(self.run_cli("implement", DONE, "--requirements", str(req)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
