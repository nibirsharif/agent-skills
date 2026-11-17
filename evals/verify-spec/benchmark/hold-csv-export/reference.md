Set: hold. Domain: reporting. Scope: one phase of `plan.md`. Drift: a feature branch with one file no requirement covers.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | skipped | Outside phase 2. |
| FR-002 | skipped | Outside phase 2. It is not implemented (no quoting), which a phase 2 report must not judge. |
| FR-003 | met | `field` writes an empty field for `None`; `test_none_is_an_empty_field` passes. |
| FR-004 | partial | Dates are written as DD/MM/YYYY, not YYYY-MM-DD. `test_date_is_written` passes because it only looks for the year. |
| FR-005 | untested | `export` with no rows gives the header row alone. No test calls it with no rows. |
| FR-006 | unmet | Nothing raises `TooManyRows`, and the name is not defined. `test_large_report` passes because it only checks that text came back. |
| FR-007 | skipped | `Blocked by Q-001`, and listed in the plan's Blocked Requirements. |

Expected tally: `1 met, 1 partial, 1 unmet, 1 untested, 3 skipped`.

Expected drift: `reports/email.py` (added on the branch, covered by no requirement). `reports/export.py` and `tests/test_export.py` also changed on the branch and are not drift.

Faults a `met` would miss: FR-004, FR-005, FR-006. A verdict other than `skipped` on FR-001, FR-002, or FR-007 is a wrong verdict.
