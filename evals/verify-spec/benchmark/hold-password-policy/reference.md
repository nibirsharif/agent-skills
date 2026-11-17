Set: hold. Domain: accounts. Drift: two uncommitted files on `main`.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | partial | The minimum length is 8, not 12. `test_short_password_is_rejected` passes because it tries 4 characters. |
| FR-002 | met | A password with no digit is rejected; `test_password_without_digit_is_rejected` passes. |
| FR-003 | untested | `problems` lower-cases the password before the list lookup. No test tries a common password. |
| FR-004 | unmet | Nothing stores or compares earlier passwords. `test_reused_password_is_rejected` passes because its password is too short. |
| NFR-001 | untested | A threshold (50 milliseconds) and no test that measures it. |

Expected tally: `1 met, 1 partial, 1 unmet, 2 untested`.

Expected drift: `accounts/session.py, tests/test_session.py` (both uncommitted; no requirement covers sessions).

Faults a `met` would miss: FR-001, FR-003, FR-004, NFR-001.
