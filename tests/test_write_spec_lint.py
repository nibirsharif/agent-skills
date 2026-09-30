"""Tests for skills/write-spec/scripts/lint.py.

The skill's own examples must pass the lint, and each rule the lint enforces must catch a bad line.
"""

import importlib.util
import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "write-spec"
spec = importlib.util.spec_from_file_location("lint", SKILL / "scripts" / "lint.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)
PATTERNS = lint.banned_patterns()


def run(text, name="t.md"):
    linter = lint.Linter(PATTERNS)
    linter.lint(name, text)
    return linter.findings


def errors(text):
    return [f for f in run(text) if f[1] == "ERROR"]


class SkillExamplesPass(unittest.TestCase):
    def test_examples_have_no_findings(self):
        self.assertEqual(run((SKILL / "references" / "examples.md").read_text()), [])

    def test_saved_file_example_passes_file_checks(self):
        text = (SKILL / "references" / "examples.md").read_text()
        saved = re.search(r"```markdown\n(.*?)```", text, re.S).group(1)
        self.assertEqual(run(saved), [])

    def test_right_examples_in_rules_have_no_errors(self):
        rules = (SKILL / "references" / "ears-rules.md").read_text()
        for line in rules.splitlines():
            if line.startswith("- **Right:**"):
                for sentence in re.findall(r"`([^`]+)`", line):
                    if "..." in sentence:
                        continue
                    text = sentence if re.match(r"(REQ|NFR|Q)-\d", sentence) else f"REQ-001: {sentence}"
                    self.assertEqual(errors(text), [], sentence)

    def test_banned_words_are_read_from_rules(self):
        words = {w for w, _ in PATTERNS}
        self.assertTrue({"gracefully", "handle", "etc.", "and/or", "TBD"} <= words)


class LintCatches(unittest.TestCase):
    def assertCaught(self, line, fragment, level="ERROR"):
        found = [f[3] for f in run(line) if f[1] == level]
        self.assertTrue(any(fragment in m for m in found), f"{fragment!r} not in {found}")

    def test_requirement_rules(self):
        cases = {
            "REQ-001: The system shall send a receipt.": "not a system name",
            "REQ-001: The billing service shall send a receipt": "full stop",
            "REQ-001: The billing service should send a receipt.": "exactly one `shall`",
            "REQ-001: When a user saves, the draft shall be stored.": "passive",
            "REQ-001: The reporting service shall be able to export reports.": "capability",
            "REQ-001: While a job is open, where the module is installed, the job service shall log the job.": "out of order",
            "REQ-001: When a user logs in, if the password is wrong, then the auth service shall log it.": "out of order",
            "REQ-001: If a login fails, the auth service shall lock the account.": ", then the",
            "REQ-001: The upload service shall accept files up to 25 MB.": "`up to`",
            "REQ-001: When a search is sent, the search API shall return results within 300 ms.": "no starting point",
            "REQ-001: When the time reaches 06:00, the report service shall send the report.": "time zone",
            "REQ-001: If a payment fails, then the billing service shall handle the failure gracefully.": "`gracefully`",
            "REQ-001: The billing service shall send a receipt, etc.": "`etc.`",
            "REQ-001: The billing service shall send the receipt TBD.": "`TBD`",
        }
        for line, fragment in cases.items():
            with self.subTest(line=line):
                self.assertCaught(line, fragment)

    def test_two_sense_words_are_checks(self):
        self.assertCaught("REQ-001: The chat service shall send a message about the order.", "`about`", "CHECK")
        self.assertEqual(errors("REQ-001: The chat service shall send a message about the order."), [])

    def test_schedule_in_response_is_a_check(self):
        self.assertCaught("REQ-001: The inverter gateway shall send a reading every 5 minutes.", "schedule", "CHECK")
        self.assertCaught("REQ-001: The report service shall email the report weekly.", "schedule", "CHECK")
        self.assertEqual(run("REQ-001: When 5 minutes have passed since the previous reading, "
                             "the inverter gateway shall send a reading."), [])

    def test_day_boundary_needs_time_zone(self):
        self.assertCaught("REQ-001: When the 1st day of a month begins, the report service shall email the report.",
                          "day boundary", "CHECK")
        self.assertEqual(run("REQ-001: When the 1st day of a month begins in UTC, "
                             "the report service shall email the report."), [])

    def test_quoted_text_is_exempt(self):
        self.assertEqual(run('REQ-001: The web client shall display "Something went wrong, try again soon".'), [])

    def test_question_rules(self):
        self.assertCaught("Q-001: What is the limit? Proposed: none.", "empty proposal")
        self.assertCaught("Q-001: What is the limit? What is the window?", "more than one question")
        self.assertCaught("Q-001: What is the limit", "does not end with `?`")
        self.assertCaught("Q-001: Closed.", "keeps its answer")
        self.assertCaught("Q-001: Which fields are required, and does the agent ask for each?", "two things", "CHECK")
        self.assertCaught("Q-001: Which alert preferences can a homeowner change, and in which system?", "two things", "CHECK")
        self.assertEqual(run("Q-001: How many alerts does the limit allow, and in what time window?"), [])
        self.assertEqual(run("Q-001: Within how many seconds must it reply, and for what percentage of messages?"), [])
        self.assertCaught("Q-001: When is production compared? Proposed: at midnight local time.", "number or time", "CHECK")
        self.assertCaught("Q-001: How long is the buffer? Proposed: 24 hours.", "number or time", "CHECK")
        self.assertEqual(run("Q-001: What happens when the address is not registered? Proposed: send no email."), [])

    def test_nfr_lines_follow_requirement_rules(self):
        self.assertCaught("NFR-001: The search API should return results within 300 ms of a request.", "modal")
        self.assertEqual(run("NFR-001: The search API shall return results within 300 ms of receiving a request "
                             "for 95% of requests."), [])

    def test_threshold_on_a_functional_response_is_a_check(self):
        self.assertCaught("REQ-001: When an admin clicks \"Export CSV\", the export service shall email the report "
                          "within 5 minutes of the click.", "is an NFR", "CHECK")
        self.assertCaught("REQ-001: The search API shall return results within 300 ms of receiving a request "
                          "for 95% of requests.", "is an NFR", "CHECK")
        self.assertEqual(run("REQ-001: If the payment gateway returns no response within 10 seconds of a charge "
                             "request, then the checkout service shall cancel the charge request."), [])

    def test_withdrawn_lines(self):
        self.assertEqual(run("REQ-001: Withdrawn."), [])
        self.assertEqual(run("REQ-001: Withdrawn. Moved to NFR-002."), [])
        self.assertCaught("REQ-001: Withdrawn because it moved.", "withdrawn line")

    def test_layout(self):
        self.assertCaught("REQ-001: The billing service shall send a receipt.\n"
                          "REQ-002: The billing service shall log the receipt.", "blank line")
        self.assertCaught("- Q-001: What is the limit?", "no bullet")


class FileChecks(unittest.TestCase):
    def file_text(self, body):
        head = "# Requirements Specification: X\n\n" + "\n\n".join(h + "\n\nNone given." for h in lint.FILE_HEADINGS)
        head = head.replace("## 2. Scope\n\nNone given.", "## 2. Scope\n\n**Systems:** billing service")
        # body holds one or more sections, each starting with its heading, and replaces them
        for section in re.split(r"\n(?=## )", body):
            head = head.replace(section.split("\n", 1)[0] + "\n\nNone given.", section)
        return head

    def file_errors(self, body):
        return [f[3] for f in run(self.file_text(body)) if f[1] == "ERROR"]

    def test_clean_file(self):
        self.assertEqual(self.file_errors("## 3. Functional Requirements\n\nREQ-001: The billing service shall send a receipt."), [])

    def test_system_missing_from_systems_line(self):
        found = self.file_errors("## 3. Functional Requirements\n\nREQ-001: The tax service shall send a receipt.")
        self.assertTrue(any("Systems line" in m for m in found), found)

    def test_instruction_text_left_in_section(self):
        found = self.file_errors("## 3. Functional Requirements\n\nOne EARS sentence per line.\n\n"
                                 "REQ-001: The billing service shall send a receipt.")
        self.assertTrue(any("not an ID line" in m for m in found), found)

    def test_nfr_system_missing_from_systems_line(self):
        found = self.file_errors("## 3. Functional Requirements\n\nNone given.\n\n## 4. Non-Functional Requirements\n\n"
                                 "NFR-001: The tax service shall comply with WCAG 2.2 level AA.")
        self.assertTrue(any("Systems line" in m for m in found), found)

    def test_ids_in_the_wrong_section(self):
        found = self.file_errors("## 3. Functional Requirements\n\n"
                                 "NFR-001: The billing service shall comply with WCAG 2.2 level AA.")
        self.assertTrue(any("only REQ lines" in m for m in found), found)
        text = self.file_text("## 4. Non-Functional Requirements\n\n"
                              "REQ-006: The billing service shall comply with WCAG 2.2 level AA.")
        self.assertTrue(any(f[1] == "CHECK" and "before NFR IDs" in f[3] for f in run(text)))
        self.assertFalse([f for f in run(text) if f[1] == "ERROR"])

    def test_duplicate_ids_and_placeholders(self):
        found = self.file_errors("## 3. Functional Requirements\n\nREQ-001: The billing service shall send a receipt.\n\n"
                                 "REQ-001: The billing service shall send [value].")
        self.assertTrue(any("duplicate ID" in m for m in found), found)
        self.assertTrue(any("placeholder" in m for m in found), found)


if __name__ == "__main__":
    unittest.main()
