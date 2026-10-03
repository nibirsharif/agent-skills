| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | met | textstats/counts.py:17; tests/test_counts.py::ReadingTime::test_rounds_up_at_default_speed passed |
| FR-002 | untested | textstats/counts.py:15; no test passes a non-string to reading_time |
| FR-003 | unmet | no implementation found: reading_time takes no words-per-minute argument; searched textstats/ |
| FR-004 | skipped | Blocked by Q-001 |
| FR-005 | met | textstats/counts.py:17; tests/test_counts.py::ReadingTime::test_empty_text_is_zero passed |
| NFR-001 | cannot tell | no criterion; clarify with write-spec |
| NFR-002 | untested | textstats/counts.py:17; no test measures 100 milliseconds for 100,000 words |
Tests: python3 -m unittest: 4 tests OK
Tally: 2 met, 1 unmet, 2 untested, 1 cannot tell, 1 skipped
Drift: textstats/formatting.py
