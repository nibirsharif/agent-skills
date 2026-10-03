| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | unmet | textstats/counts.py:17 rounds down; tests/test_counts.py::ReadingTime::test_rounds_up_at_default_speed failed: 201 words gave 1, expected 2 |
Tests: python3 -m unittest: 1 failure in 4 tests
Tally: 1 unmet
Drift: none
