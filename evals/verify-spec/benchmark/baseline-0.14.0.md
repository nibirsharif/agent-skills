# Baseline: verify-spec 0.14.0

One run per input on `claude-sonnet-5-5` (Claude Code 2.1.322), 2026-11-16, with the skill as on `master` after 0.14.0 (the `check_scope.py` script included). Scored by hand against each `reference.md` as the [README](README.md) says. The references were written before the run.

| Input | Verdicts right | Gaps missed | False alarms | Drift right |
|-------|----------------|-------------|--------------|-------------|
| dev-cart | 6 of 6 | 0 of 3 | 0 | yes |
| dev-rate-limiter | 5 of 5 | 0 of 4 | 0 | yes |
| dev-todo | 6 of 6 | 0 of 4 | 0 | yes |
| **dev total** | 17 of 17 | 0 of 11 | 0 | 3 of 3 |
| hold-csv-export | 7 of 7 | 0 of 3 | 0 | yes |
| hold-greenhouse | 7 of 7 | 0 of 3 | 0 | yes |
| hold-password-policy | 5 of 5 | 0 of 4 | 0 | yes |
| **hold total** | 19 of 19 | 0 of 10 | 0 | 3 of 3 |
| **Total** | 36 of 36 | 0 of 21 | 0 | 6 of 6 |

## What this baseline can show

Every row is right, so this set is at its ceiling: it can show a later change making verdicts worse, and it cannot show one making them better. The planted faults are each in one function and one test file of a project with fewer than 100 lines. Harder inputs would be a fault spread over two modules, a test that checks the requirement through a mock, or a project large enough that the search for an implementation can miss it.

## Other findings

- Every reply named the planted cause in its evidence: the constant the test reused (dev-cart FR-002), the skipped test (dev-cart FR-005), the boundary the test avoids (dev-cart FR-003, hold-greenhouse FR-003), the test that passes for another reason (dev-rate-limiter FR-004, hold-password-policy FR-004).
- hold-password-policy wrote its tally as `1 met, 1 partial, 2 untested, 1 unmet`. The contract's order puts `unmet` before `untested`. The counts are right.
- The `Tests:` line differs between replies in its command (`python3 -m unittest`, with or without `-v`) and in how it words the result. The contract fixes neither.
- No reply had text outside the report.
