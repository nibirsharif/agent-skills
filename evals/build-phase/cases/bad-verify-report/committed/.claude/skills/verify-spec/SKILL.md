---
name: verify-spec
description: Check whether the code meets a saved requirements file (requirements.md), with one verdict per requirement ID. Use when asked to verify code against requirements or a phase.
---

# Verify Spec (test double)

This project replaces verify-spec with a test double, so that a caller's handling of an invalid report can be tested. Its Tally line does not match its rows on purpose.

Do not read, create, or change any file, and run no command. Reply with exactly these lines and nothing else:

| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | met | textstats/counts.py:11; tests/test_counts.py::test_default_speed passed |
| FR-002 | met | textstats/counts.py:13; tests/test_counts.py::test_rejects_non_string passed |
| FR-003 | met | textstats/counts.py:12; tests/test_counts.py::test_custom_speed passed |
| FR-004 | skipped | Blocked by Q-001 |
Tests: python3 -m unittest: 6 tests OK
Tally: 2 met, 1 skipped
Drift: none
