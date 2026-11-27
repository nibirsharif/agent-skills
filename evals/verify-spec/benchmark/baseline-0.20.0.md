# Baseline: verify-spec 0.20.0

Three runs per input on `claude-sonnet-5-5` (Claude Code 2.1.327), 2026-11-26, with the skill as on `master` at 0.20.0. Ten inputs: the six of the [0.14.0 baseline](baseline-0.14.0.md) and the four harder ones added for [#23](https://github.com/nibirsharif/agent-skills/issues/23), which the [README](README.md#the-harder-inputs) describes. Counted by [score.py](score.py) against each `reference.md`; each row it marked wrong or differing was then read by hand. The references were written, and each planted fault was run to confirm it, before the first run.

Each cell counts all three runs. Agreement is the rows that have the same verdict in every run.

| Input | Verdicts right | Gaps missed | False alarms | Drift right | Agreement |
|-------|----------------|-------------|--------------|-------------|-----------|
| dev-bookings | 24 of 24 | 0 of 15 | 0 | 3 of 3 | 7 of 8 |
| dev-cart | 18 of 18 | 0 of 9 | 0 | 3 of 3 | 6 of 6 |
| dev-helpdesk | 21 of 24 | 3 of 15 | 0 | 3 of 3 | 8 of 8 |
| dev-rate-limiter | 15 of 15 | 0 of 12 | 0 | 3 of 3 | 5 of 5 |
| dev-todo | 17 of 18 | 0 of 12 | 0 | 3 of 3 | 5 of 6 |
| **dev total** | 95 of 99 | 3 of 63 | 0 | 15 of 15 | 31 of 33 |
| hold-csv-export | 21 of 21 | 0 of 9 | 0 | 3 of 3 | 7 of 7 |
| hold-depot | 27 of 30 | 3 of 15 | 0 | 3 of 3 | 10 of 10 |
| hold-greenhouse | 21 of 21 | 0 of 9 | 0 | 3 of 3 | 7 of 7 |
| hold-mailing | 27 of 27 | 0 of 15 | 0 | 3 of 3 | 8 of 9 |
| hold-password-policy | 15 of 15 | 0 of 12 | 0 | 3 of 3 | 5 of 5 |
| **hold total** | 111 of 114 | 3 of 60 | 0 | 15 of 15 | 37 of 38 |
| **Total** | 206 of 213 | 6 of 123 | 0 | 30 of 30 | 68 of 71 |

The four harder inputs alone: 99 of 105 verdicts right, 6 of 60 gaps missed, and 33 of 35 rows the same in every run. The six older ones: 107 of 108, no gap missed, 35 of 36.

## What the harder inputs show

**A rule that one path skips is called `met`, every time.** dev-helpdesk FR-006 and hold-depot FR-006 are `met` in 6 of 6 runs, and the reference is `partial`. Each requirement forbids something (escalating a closed ticket, ordering a discontinued item). The check is on the path the test drives, and a request handler reaches the same code without it. Every reply cites the check and the passing test and stops there; none names the handler. These are the only gaps called `met` in the 30 runs, and the runs agree, so repeating a run does not find them.

**A rule kept outside the system the requirement names gets two verdicts.** This is the verdict that changed on a retry in the [first real run](../../real-runs/2026-11-17.md). dev-bookings FR-002 is `partial`, `met`, `met`, and hold-mailing FR-002 is `met`, `partial`, `partial`. Every one of the six replies says the same thing in its evidence, that the check is in the service and not in the store, and then names either verdict. With hold-mailing's first three runs (below), 6 of 9 replies say `partial` and 3 say `met`. The references left these rows open when this page was scored, so neither verdict is counted wrong in the table. A rule now makes them `partial` ([after-verdict-rules.md](after-verdict-rules.md)); scored that way, the same replies are 203 of 213 right with 9 of 129 gaps called `met`.

**Code that is right with a test that checks too little is sometimes `partial`.** dev-todo FR-004 is `partial` in 1 of 3 runs, with the same evidence as the two `untested` replies. [after-shorter-rules.md](after-shorter-rules.md) found the same in 2 of 10 runs. Both verdicts report a gap.

**The other harder kinds were found in every run:**

- A fault across two modules: `partial` in 21 of 21 (dev-bookings FR-003 and FR-005, dev-helpdesk FR-002 and FR-005, hold-mailing FR-003 and FR-006, hold-depot FR-002), each naming the cause, such as minutes passed where hours are taken.
- A test that passes because of a mock: every row right. The rows where a mock hides the fault are `partial`, the rows where a mock replaces the code under test are `untested`, and the three rows where the mock is the boundary are `met`, with no false alarm.
- A benchmark of another size: `untested` in 6 of 6.
- An implementation the requirement's words do not find: `met` in 6 of 6 (dev-helpdesk FR-001, hold-depot FR-001), each citing the rule or the hook. No reply stopped at the file with the obvious name. At about 30 modules the search does not miss; a project of hundreds of files is still not measured.
- Code the trigger cannot reach, the other open row: `partial` in 6 of 6.

## Other findings

- **The tally is miscounted in 3 of 30 replies** (dev-bookings twice, hold-greenhouse once): one count is off by one while the rows are right. One of the three then wrote "Correction, the tally must match the rows:" and the whole report again, which is text outside the contract. build-phase counts the tally from the rows, so no verdict is lost. The other 27 replies hold nothing but the report.
- **Line numbers past the end of the file in 3 of the 12 runs on the harder inputs** (dev-bookings twice, dev-helpdesk once): 29 citations such as `bookings/notify.py:117` for a file of 13 lines. The path and the code described are right in each. None of the 18 runs on the older inputs has one. The rules say every cited line exists; why these do not is not known, since `bench.py` kept no transcript at the time.
- **hold-mailing was run twice.** In its first three runs one reply gave FR-007 `partial` because the subscribe and unsubscribe mails do not handle a refusal either, which the requirement, worded for any message, did cover: a gap that was not planted. The requirement now says a campaign's message, and the table has the three runs after that. FR-002 was `partial` in all three of the first runs.
- Every drift line is right, with or without a feature branch.
- A run costs about $0.14 on the six older inputs, $0.19 on the two of 10 modules, and $0.22 on the two of 30. The 30 runs cost $4.92.
