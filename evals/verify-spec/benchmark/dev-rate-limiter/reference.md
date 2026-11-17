Set: dev. Domain: library. Drift: one uncommitted file on `main`.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | `Limiter.check` accepts under the limit; `test_accepts_up_to_the_limit` passes. |
| FR-002 | partial | `RateLimited` is raised, but it has no `retry_after`. `test_sixth_request_is_rejected` passes because it only checks the exception type. |
| FR-003 | untested | The window filter in `check` drops requests older than 60 seconds. No test moves the fake clock. |
| FR-004 | unmet | No allowlist anywhere. `test_allowlisted_client_is_accepted` passes because it stays within the limit. |
| NFR-001 | untested | A threshold (1 millisecond) and no test that measures it. |

Expected tally: `1 met, 1 partial, 1 unmet, 2 untested`.

Expected drift: `ratelimit/metrics.py` (uncommitted, covered by no requirement).

Faults a `met` would miss: FR-002, FR-003, FR-004, NFR-001.
