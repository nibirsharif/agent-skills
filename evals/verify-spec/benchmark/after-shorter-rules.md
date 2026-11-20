# After the shorter rules

The change for [#24](https://github.com/nibirsharif/agent-skills/issues/24): what verify-spec reads on every run (`SKILL.md`, `verify-rules.md`, `examples.md`) went from 3,506 to 2,917 words. One run per input on `claude-sonnet-5-5` (Claude Code 2.1.327), 2026-11-19, before and after the change, scored against each `reference.md` as the [README](README.md) says.

| Input | Verdicts right, before | Verdicts right, after | Gaps missed, after | False alarms, after | Drift right, after |
|-------|------------------------|-----------------------|--------------------|---------------------|--------------------|
| dev-cart | 6 of 6 | 6 of 6 | 0 of 3 | 0 | yes |
| dev-rate-limiter | 5 of 5 | 5 of 5 | 0 of 4 | 0 | yes |
| dev-todo | 6 of 6 | 5 of 6 | 0 of 4 | 0 | yes |
| **dev total** | 17 of 17 | 16 of 17 | 0 of 11 | 0 | 3 of 3 |
| hold-csv-export | 7 of 7 | 7 of 7 | 0 of 3 | 0 | yes |
| hold-greenhouse | 7 of 7 | 7 of 7 | 0 of 3 | 0 | yes |
| hold-password-policy | 5 of 5 | 5 of 5 | 0 of 4 | 0 | yes |
| **hold total** | 19 of 19 | 19 of 19 | 0 of 10 | 0 | 3 of 3 |
| **Total** | 36 of 36 | 35 of 36 | 0 of 21 | 0 | 6 of 6 |

The run before the change missed no gap, raised no false alarm, and had every drift line right, as the [0.14.0 baseline](baseline-0.14.0.md) did. One row of difference is no change by the README's measure.

## The row that differs

dev-todo FR-004: `partial` where the reference says `untested`. The code sorts correctly and the only test checks the length of the list. The reply's evidence says exactly that, and then names the wrong verdict: `partial` is for code that does part of the statement, and this code does all of it.

dev-todo run four more times on each wording:

| Wording | FR-004 `untested` | FR-004 `partial` | Every other row right |
|---|---|---|---|
| Before the change | 4 of 5 | 1 of 5 | 5 of 5 |
| After | 4 of 5 | 1 of 5 | 5 of 5 |

So about 1 reply in 5 misreads this row with the rules as they were, and the 0.14.0 baseline's single run did not show it. The rules do not say which of `partial` and `untested` is the weaker; the row is still reported as a gap either way.

## Other findings

- dev-todo opened with a sentence before the table in 1 of 5 runs on each wording ("Verifying due-dates: I've read the code and run the tests, ..." before, "I've read the code and run the tests. I'm now writing up the verdicts." after). No other input did, and no reply of the eval suite on either wording.
- Every tally was in the contract's order and matched its rows.
