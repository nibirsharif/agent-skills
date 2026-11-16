"""Tests for evals/build-phase/hooks.py: a wrong summary and text outside the summary are reported apart."""

import sys
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent.parent / "evals"
sys.path.insert(0, str(EVALS))
import grading  # noqa: E402

hooks = grading.load_hooks("build-phase")

STOPPED = """Phase ? of invoice-export: stopped
Branch: main
Tasks: 0 implemented, 0 reworked
Verify: not run
Stopped: No tasks file found at docs/specs/invoice-export/tasks.md. Run write-tasks first, then run build-phase again."""

DONE = """Phase 1 of reading-time: done
Branch: reading-time-phase-1
Tasks: 2 implemented, 1 reworked
Verify: Tally: 3 met, 0 partial, 0 unmet, 0 untested, 0 cannot tell, 1 skipped
Check by hand: FR-002: click Copy and paste the text
Next: push reading-time-phase-1, open a PR titled "reading-time phase 1: Core", and run /code-review"""


class Hooks(unittest.TestCase):
    def test_a_summary_alone_passes(self):
        for reply in (STOPPED, DONE, "\n" + DONE + "\n"):
            self.assertEqual(hooks.check(reply), [])

    def test_a_sentence_before_a_correct_summary_is_only_outside(self):
        reply = "No `tasks.md` exists. Per the rules, this stops immediately.\n\n" + STOPPED
        self.assertEqual(hooks.check_summary(reply), [])
        self.assertEqual(hooks.check(reply), [
            "outside the summary: text before it: No `tasks.md` exists. Per the rules, this stops immediately."])

    def test_text_after_and_inside_is_placed(self):
        lines = DONE.splitlines()
        reply = "\n".join(lines[:2] + ["(two tasks)"] + lines[2:] + ["Let me know."])
        self.assertEqual(hooks.check_summary(reply), [])
        self.assertEqual(hooks.check_outside(reply), [
            "outside the summary: text inside it: (two tasks)",
            "outside the summary: text after it: Let me know."])

    def test_a_code_fence_around_the_summary_is_outside(self):
        self.assertEqual(len(hooks.check_outside("```\n" + STOPPED + "\n```")), 2)
        self.assertEqual(hooks.check_summary("```\n" + STOPPED + "\n```"), [])

    def test_a_wrong_summary_is_only_summary(self):
        cases = {
            STOPPED.replace("Stopped: ", "Reason: ").split("\n")[0] + "\nBranch: main": "summary: a stopped run needs a Stopped line",
            DONE + "\nStopped: the round limit": "summary: a Stopped line on a run that is done",
            STOPPED + '\nNext: push main, open a PR titled "x phase 1: y", and run /code-review': "summary: a Next line on a stopped run",
            "Branch: main\n" + STOPPED: "summary: the Phase line is not its first line",
            STOPPED + "\n" + STOPPED: "summary: more than one Phase line",
        }
        for reply, problem in cases.items():
            with self.subTest(problem=problem):
                self.assertEqual(hooks.check(reply), [problem])

    def test_no_summary_fails_both(self):
        self.assertEqual(hooks.check("There is no tasks file."), [
            "summary: no Phase line", "outside the summary: text instead of it: There is no tasks file."])
        self.assertEqual(hooks.check(""), ["summary: no Phase line"])


if __name__ == "__main__":
    unittest.main()
