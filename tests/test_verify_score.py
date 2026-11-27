"""Tests for evals/verify-spec/benchmark/score.py, and that every verify-spec benchmark reference can be scored."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

BENCHMARK = Path(__file__).resolve().parent.parent / "evals" / "verify-spec" / "benchmark"
spec = importlib.util.spec_from_file_location("score", BENCHMARK / "score.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)

REFERENCE = """Set: dev.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | Right, with a test. |
| FR-002 | partial | A wrong value. |
| FR-003 | met or partial | Open row. |
| NFR-001 | untested | No benchmark. |

Expected drift: `shop/a.py, shop/b.py` (both uncommitted). `shop/cart.py` also changed and is not drift.
"""


def reply(verdicts, drift="shop/a.py, shop/b.py", before=""):
    rows = "\n".join(f"| {req} | {v} | shop/cart.py:3; tests/test_cart.py::test_x passed |" for req, v in verdicts.items())
    return f"{before}| ID | Verdict | Evidence |\n|----|---------|----------|\n{rows}\nTests: python3 -m unittest: 4 tests OK\nTally: x\nDrift: {drift}"


RIGHT = {"FR-001": "met", "FR-002": "partial", "FR-003": "met", "NFR-001": "untested"}


class Reference(unittest.TestCase):
    def setUp(self):
        self.reference = sc.read_reference(REFERENCE)

    def test_rows_and_open_rows(self):
        self.assertEqual(self.reference["rows"], {"FR-001": ["met"], "FR-002": ["partial"], "FR-003": ["met", "partial"], "NFR-001": ["untested"]})

    def test_drift_is_the_first_quoted_list(self):
        self.assertEqual(self.reference["drift"], ["shop/a.py", "shop/b.py"])

    def test_drift_not_checked(self):
        text = REFERENCE.split("Expected drift")[0] + "Expected drift: `not checked (no feature branch)`.\n"
        self.assertEqual(sc.read_reference(text)["drift"], sc.NOT_CHECKED)


class Score(unittest.TestCase):
    def setUp(self):
        self.reference = sc.read_reference(REFERENCE)

    def score(self, verdicts=RIGHT, **more):
        return sc.score(self.reference, reply(verdicts, **more))

    def test_every_row_right(self):
        result = self.score()
        self.assertEqual((result["right"], result["gaps_missed"], result["false_alarms"], result["drift_right"]), (4, [], [], True))

    def test_either_verdict_of_an_open_row_is_right(self):
        self.assertEqual(self.score({**RIGHT, "FR-003": "partial"})["right"], 4)
        self.assertEqual(self.score({**RIGHT, "FR-003": "unmet"})["right"], 3)

    def test_met_for_a_gap_is_a_gap_missed(self):
        result = self.score({**RIGHT, "FR-002": "met", "NFR-001": "met"})
        self.assertEqual((result["right"], result["gaps_missed"]), (2, ["FR-002", "NFR-001"]))

    def test_a_gap_named_differently_is_wrong_and_not_missed(self):
        result = self.score({**RIGHT, "FR-002": "unmet"})
        self.assertEqual((result["right"], result["gaps_missed"], result["false_alarms"]), (3, [], []))

    def test_a_gap_verdict_for_a_met_row_is_a_false_alarm(self):
        self.assertEqual(self.score({**RIGHT, "FR-001": "untested"})["false_alarms"], ["FR-001"])

    def test_met_on_an_open_row_is_not_a_gap_missed(self):
        self.assertEqual(self.score()["gaps_missed"], [])

    def test_a_missing_row_is_wrong(self):
        verdicts = {k: v for k, v in RIGHT.items() if k != "FR-002"}
        result = self.score(verdicts)
        self.assertEqual((result["right"], result["verdicts"]["FR-002"], result["false_alarms"]), (3, None, []))

    def test_an_extra_drift_file_is_a_false_alarm(self):
        result = self.score(drift="shop/b.py, shop/a.py, shop/cart.py")
        self.assertEqual((result["drift_right"], result["false_alarms"]), (False, ["shop/cart.py"]))

    def test_a_missing_drift_file_is_wrong(self):
        result = self.score(drift="shop/a.py")
        self.assertEqual((result["drift_right"], result["false_alarms"]), (False, []))

    def test_text_before_the_table_is_reported_and_the_rows_still_count(self):
        result = self.score(before="I read the code.\n")
        self.assertEqual(result["right"], 4)
        self.assertIn("text before the table", result["problems"])

    def test_agreement_counts_rows_every_run_gave_the_same(self):
        scores = [self.score(), self.score({**RIGHT, "FR-003": "partial"}), self.score()]
        self.assertEqual(sc.agreeing(self.reference, scores), ["FR-001", "FR-002", "NFR-001"])

    def test_report_totals(self):
        scores = [self.score(), self.score({**RIGHT, "FR-002": "met"})]
        lines, totals = sc.report("dev-x", self.reference, scores)
        self.assertEqual((totals["right"], totals["rows"], totals["gaps_missed"], totals["gaps"], totals["same"]), (7, 8, 1, 4, 3))
        self.assertIn("| FR-002 | partial | partial | met |  <- runs differ", lines)


class Replies(unittest.TestCase):
    def test_numbered_replies_come_in_run_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for name in ("dev-x-r10.md", "dev-x-r2.md", "dev-x-r1.md", "dev-x.json", "dev-xy-r1.md"):
                (tmp / name).write_text("")
            self.assertEqual([p.name for p in sc.replies_of(tmp, "dev-x")], ["dev-x-r1.md", "dev-x-r2.md", "dev-x-r10.md"])

    def test_single_reply(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "dev-x.md").write_text("")
            self.assertEqual([p.name for p in sc.replies_of(Path(tmp), "dev-x")], ["dev-x.md"])


class References(unittest.TestCase):
    """Every input's reference has one row for each ID of its requirements.md, in file order, and a drift line."""

    def test_each_reference_matches_its_requirements(self):
        inputs = sorted(p for p in BENCHMARK.iterdir() if (p / "reference.md").is_file())
        self.assertTrue(inputs)
        for folder in inputs:
            with self.subTest(folder.name):
                text = (folder / "reference.md").read_text()
                requirements = next((folder / "project" / "docs" / "specs").glob("*/requirements.md")).read_text()
                self.assertEqual(list(sc.read_reference(text)["rows"]), sc.parse_reply.requirement_ids(requirements))
                self.assertRegex(text, r"(?m)^Expected drift: `")


if __name__ == "__main__":
    unittest.main()
