"""Tests for skills/build-phase/scripts/summary.py: the summary lines it prints pass the eval's own reply checks."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "build-phase" / "scripts" / "summary.py"
sys.path.insert(0, str(ROOT / "evals"))
import grading  # noqa: E402

hooks = grading.load_hooks("build-phase")

BASE = ["--feature", "reading-time", "--phase", "1", "--branch", "reading-time/phase-1",
        "--implemented", "2", "--reworked", "0", "--verify", "2 met, 1 partial, 1 skipped"]


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class Summary(unittest.TestCase):
    def test_stopped(self):
        out = run(*BASE, "--stopped", "FR-001 still not met after 0 rework rounds")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "Phase 1 of reading-time: stopped\nBranch: reading-time/phase-1\n"
                         "Tasks: 2 implemented, 0 reworked\nVerify: 2 met, 1 partial, 1 skipped\n"
                         "Stopped: FR-001 still not met after 0 rework rounds\n")
        self.assertEqual(hooks.check(out.stdout), [])

    def test_done_with_checks_by_hand(self):
        out = run(*BASE, "--check-by-hand", "FR-002: click Copy", "--check-by-hand", "FR-005: open it on a phone",
                  "--title", "Core counts")
        self.assertEqual(out.returncode, 0, out.stderr)
        lines = out.stdout.splitlines()
        self.assertEqual(lines[0], "Phase 1 of reading-time: done")
        self.assertEqual(lines[4:6], ["Check by hand: FR-002: click Copy", "Check by hand: FR-005: open it on a phone"])
        self.assertEqual(lines[-1], 'Next: push reading-time/phase-1, open a PR titled '
                         '"reading-time phase 1: Core counts", and run /code-review')
        self.assertEqual(hooks.check(out.stdout), [])

    def test_usage_errors(self):
        for args in (BASE + ["--stopped", "x", "--title", "y"],  # both endings
                     BASE,  # neither
                     BASE + ["--stopped", "two\nlines"],
                     BASE + ["--stopped", "Stopped: x"],  # label given twice
                     [a if a != "2" else "-1" for a in BASE] + ["--stopped", "x"]):
            self.assertEqual(run(*args).returncode, 2, args)


if __name__ == "__main__":
    unittest.main()
