Set: dev. Domain: command-line tool. Drift: none to check (`main`, nothing uncommitted).

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | `add --due` stores the date; `test_add_stores_the_due_date` passes. |
| FR-002 | partial | The message is printed, but the exit status is 1, not 2. `test_invalid_date_prints_a_message` checks only the message. |
| FR-003 | unmet | `overdue` uses `<=`, so a task due today is listed. `test_task_due_today_is_not_overdue` runs and fails; a failed test for the requirement makes it `unmet`. `partial` sees the fault but breaks the "failure beats presence" rule. |
| FR-004 | untested | `listing` sorts correctly. `test_listing_keeps_every_task` checks only the length, so it does not count. |
| FR-005 | unmet | No code marks a task done or records a date, and no test. |
| NFR-001 | cannot tell | "easy to use" has no criterion. |

Expected tally: `1 met, 1 partial, 2 unmet, 1 untested, 1 cannot tell`.

Expected tests line: the run has one failure.

Expected drift: `not checked (no feature branch)`.

Faults a `met` would miss: FR-002, FR-003, FR-004, FR-005.
