"""Tests for the size scripts of the write-tasks and write-spec benchmarks, and that every reference they read
can be read."""

import importlib.util
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent.parent / "evals"


def load(skill):
    spec = importlib.util.spec_from_file_location(f"{skill}_size", EVALS / skill / "benchmark" / "size.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tasks_size = load("write-tasks")
spec_size = load("write-spec")


def task(task_id, title, covers, files="new: a file"):
    return f"#### {task_id}: {title}\n\n**Covers:** {covers}\n\n**Files:** {files}\n\n**Depends on:** None.\n\n**Done when:** x\n\n**Status:** Todo\n\n"


TASKS = (
    "## 1. Overview\n\nNo codebase.\n\n## 2. Tasks\n\n### Phase 1: Booking\n\n"
    + task("T-1.1", "Add the bookings store", "FR-001")
    + task("T-1.2", "Book a time slot, and reject one with no free table", "FR-001, FR-002")
    + task("T-1.3", "Verify the phase", "FR-001, FR-002", "None.")
    + "### Phase 2: Text message\n\n"
    + task("T-2.1", "Verify the sender's signature", "FR-003")
    + task("T-2.2", "Verify the phase", "FR-003, NFR-001", "None.")
    + "## 3. Blocked Requirements\n\nNone.\n"
)


class TasksSize(unittest.TestCase):
    def test_verify_tasks_are_left_out(self):
        tasks = tasks_size.tasks_of(TASKS)
        self.assertEqual([t["id"] for t in tasks if t["verify"]], ["T-1.3", "T-2.2"])
        self.assertEqual([t["phase"] for t in tasks], ["1", "1", "1", "2", "2"])

    def test_a_build_task_named_verify_is_counted(self):
        s = tasks_size.size(["FR-001", "FR-002", "FR-003", "NFR-001"], TASKS)
        self.assertEqual((s["build"], s["verify"]), (3, 2))

    def test_tasks_with_several_ids_and_ids_not_covered(self):
        s = tasks_size.size(["FR-001", "FR-002", "FR-003", "NFR-001"], TASKS)
        self.assertEqual(s["several"], ["T-1.2"])
        # NFR-001 is only in the verify task, which builds nothing.
        self.assertEqual(s["uncovered"], ["NFR-001"])

    def test_a_phase_of_one_task_has_no_verify_task(self):
        reply = "### Phase 1: One\n\n" + task("T-1.1", "Verify the phase", "FR-001", "None.")
        self.assertEqual(tasks_size.size(["FR-001"], reply)["build"], 1)

    def test_a_last_task_that_misses_an_id_is_a_build_task(self):
        reply = "### Phase 1: One\n\n" + task("T-1.1", "Add a", "FR-001") + task("T-1.2", "Add b", "FR-002")
        self.assertEqual(tasks_size.size(["FR-001", "FR-002"], reply)["build"], 2)

    def test_reference_needs_its_count_to_match(self):
        self.assertEqual(tasks_size.read_reference("Set: dev.\n\nIDs (2): Phase 1: FR-001, NFR-001.\n"), ["FR-001", "NFR-001"])
        with self.assertRaises(ValueError):
            tasks_size.read_reference("IDs (3): FR-001, NFR-001.\n")
        with self.assertRaises(ValueError):
            tasks_size.read_reference("Set: dev.\n")

    def test_every_reference_can_be_read(self):
        references = sorted((EVALS / "write-tasks" / "benchmark").glob("*/reference.md"))
        self.assertTrue(references)
        for path in references:
            with self.subTest(input=path.parent.name):
                self.assertTrue(tasks_size.read_reference(path.read_text()))


TURN2 = """Earlier in this conversation I gave you this input:

> A statement.

You replied:

FR-001: When a thing happens, the widget service shall store the thing.

FR-002: When a thing is read, the widget service shall return the thing.

Q-001: How many things?

My answers:

Q-001: 5. FR-009: not a requirement line of the reply.
"""

FOLLOW_UP = """FR-002 (changed): Withdrawn. Moved to NFR-001.

FR-001 (changed): When a thing happens, the widget service shall store at most 5 things.

FR-003 (new): If a sixth thing happens, then the widget service shall reject the thing.

NFR-001 (new): The widget service shall return a thing within 2 seconds.

Q-002: What does the widget service return for a rejected thing?

Q-003: Which things are read?

3 more open questions after these.

Draft: When a thing is read, the [Q-003] shall return the thing.
"""

FILE = """## 3. Functional Requirements

FR-001: The tool shall read the key from KEY. <!-- Source: answer to Q-001 -->

FR-002: If KEY is missing, then the tool shall exit with code 2. <!-- Source: answer to Q-002 -->

FR-003: The tool shall write one row at a time. <!-- Source: "writes one row at a time" -->

FR-004: The tool shall skip a row that is written. <!-- Source: added input, rows are skipped; answer to Q-003 -->

FR-005: The tool shall not check the environment. <!-- Source: answer to Q-004 -->

FR-006: Withdrawn. <!-- Source: answer to Q-001 -->

FR-007: If the row is locked, then the tool shall wait. <!-- Source: answers to Q-005 and Q-001 -->

## 5. Open Questions

Q-001: Closed. Where is the key? Answer: KEY. <!-- Source: "a key" -->

Q-002: Closed. What if KEY is missing? Answer: exit 2. <!-- Source: coverage gap in FR-001 -->

Q-003: Closed. What about a written row? Answer: skip. <!-- Source: coverage gap in FR-003 -->

Q-004: Closed. Outside dev? Answer: no check. <!-- Source: answer to Q-001 -->

Q-005: Closed. What if the row is locked? Answer: wait. <!-- Source: coverage gap in FR-002 -->

Q-006: What does the tool print while it waits? <!-- Source: coverage gap in FR-007 -->
"""


class SpecSize(unittest.TestCase):
    def test_first_reply_requirements_come_from_the_reply_only(self):
        self.assertEqual(spec_size.first_reply(TURN2), ["FR-001", "FR-002"])

    def test_after_counts_new_and_withdrawn(self):
        s = spec_size.size(1, ["FR-001", "FR-002"], FOLLOW_UP)
        self.assertEqual((s["before"], s["new"], s["changed"], s["withdrawn"], s["after"]), (2, 2, 1, 1, 3))

    def test_questions_include_those_held_back_and_not_drafts(self):
        self.assertEqual(spec_size.size(1, ["FR-001", "FR-002"], FOLLOW_UP)["questions"], 5)

    def test_a_line_without_a_marker_is_new_when_its_id_is(self):
        s = spec_size.size(1, ["FR-001"], "FR-001: The widget service shall store a thing.\n\nFR-002: The widget service shall log.\n")
        self.assertEqual((s["new"], s["changed"], s["after"]), (1, 1, 2))

    def test_requirements_by_source(self):
        kinds = spec_size.by_source(FILE)["requirements"]
        self.assertEqual(kinds, {
            "FR-001": "answer", "FR-002": "coverage gap", "FR-003": "statement",
            # The first source named decides.
            "FR-004": "statement", "FR-005": "answer to an answer", "FR-007": "coverage gap",
        })

    def test_gap_questions_by_the_requirement_they_name(self):
        gaps = spec_size.by_source(FILE)["gap_questions"]
        self.assertEqual(gaps, {"Q-002": "answer", "Q-003": "statement", "Q-005": "coverage gap", "Q-006": "coverage gap"})

    def test_every_input_has_a_statement_count_and_a_gap_list(self):
        inputs = sorted(p.parent for p in (EVALS / "write-spec" / "benchmark").glob("*/turn2.md"))
        self.assertTrue(inputs)
        for folder in inputs:
            with self.subTest(input=folder.name):
                self.assertTrue(spec_size.STATEMENTS.search((folder / "reference.md").read_text()))
                self.assertIn("Coverage-gap questions in the first reply", (folder / "reference-turn2.md").read_text())


if __name__ == "__main__":
    unittest.main()
