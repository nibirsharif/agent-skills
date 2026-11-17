Set: hold. Domain: device. Drift: none to check (`main`, nothing uncommitted).

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | A reading above 35.0 raises `high`; `test_reading_above_35_raises_high` passes and checks 35.0 itself. |
| FR-002 | met | No second `high` while one is active; `test_no_second_high_alert` passes. |
| FR-003 | partial | The alert clears at 35.0 or below, not 33.0. `test_cool_reading_clears_the_alert` passes because it tries 30.0. |
| FR-004 | untested | `tick` raises `sensor-lost` after 120 seconds. No test calls `tick`. |
| FR-005 | unmet | There is no alert log. `test_alert_is_logged` passes because it only checks what `reading` returns. |
| NFR-001 | met | `test_reading_is_fast` measures each of 1,000 readings against 10 milliseconds and passes. An NFR with a benchmark is `met`, not `untested`. |
| NFR-002 | cannot tell | "reliable" has no criterion. |

Expected tally: `3 met, 1 partial, 1 unmet, 1 untested, 1 cannot tell`.

Expected drift: `not checked (no feature branch)`.

Faults a `met` would miss: FR-003, FR-004, FR-005. Anything but `met` on FR-001, FR-002, or NFR-001 is a false alarm.
