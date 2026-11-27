# After the verdict rules

The change for [#23](https://github.com/nibirsharif/agent-skills/issues/23): three rules that decide the verdicts the [0.20.0 baseline](baseline-0.20.0.md) showed missed or changing between runs. Three runs per input on `claude-sonnet-5-5` (Claude Code 2.1.327), 2026-11-26, before and after, counted by [score.py](score.py).

## The rules

All three are in [verify-rules.md](../../../skills/verify-spec/references/verify-rules.md):

- **Every way in.** Each caller of the code a statement is about is searched for, not only the one a test drives. A caller that reaches the trigger or the effect and skips the statement's check or response makes the row `partial`.
- **The named system.** When the statement names one part of the code, such as the store, and only a caller of that part does the behaviour, the row is `partial`. A name for the whole product is met anywhere in it.
- **`partial` is only for code that falls short.** Code that does all of the statement is `untested`, however weak its tests.

Workflow step 2 of `SKILL.md` and item 2 of the validation checklist name the callers too, since the rule has to act where the code is searched. What a run reads went from 2,917 to 3,034 words, and the budget from 3,020 to 3,040.

## Result

Both columns are scored against the references as they are now. The two rows for a rule kept outside the named system (dev-bookings FR-002, hold-mailing FR-002) were open, `met` or `partial`, when the baseline was scored, and are `partial` now that a rule decides them, so the "before" numbers here are lower than the baseline page's.

| | Before | After |
|---|--------|-------|
| Verdicts right, dev | 93 of 99 | 99 of 99 |
| Verdicts right, hold | 110 of 114 | 114 of 114 |
| Gaps called `met`, dev | 5 of 66 | 0 of 66 |
| Gaps called `met`, hold | 4 of 63 | 0 of 63 |
| False alarms | 0 | 0 |
| Drift right | 30 of 30 | 30 of 30 |
| Rows the same in every run | 68 of 71 | 70 of 71 |
| The four harder inputs: verdicts right | 96 of 105 | 105 of 105 |
| The four harder inputs: gaps called `met` | 9 of 66 | 0 of 66 |

The rules were worded once, on the dev inputs, and not changed after the dev run. The hold inputs were run after that, once.

Row by row, three runs each:

| Row | Kind | Before | After |
|-----|------|--------|-------|
| dev-helpdesk FR-006 | a second way in | `met`, `met`, `met` | `partial` in 3 of 3, each naming `post_handoff` |
| hold-depot FR-006 | a second way in | `met`, `met`, `met` | `partial` in 3 of 3 |
| dev-bookings FR-002 | outside the named system | `partial`, `met`, `met` | `partial` in 3 of 3 |
| hold-mailing FR-002 | outside the named system | `met`, `partial`, `partial` | `partial` in 3 of 3 |
| dev-todo FR-004 | code right, weak test | `untested`, `untested`, `partial` | `untested` in 3 of 3 |

No row that was right before is wrong after. The 20 rows whose reference is `met` are `met` in all 60 verdicts, so the search for other callers raised no false alarm, and no requirement that names the whole product ("the mailing service", for code in two classes) was called `partial` for where its code is.

The eval suite passed 27 of 27 at 3 runs after the change, as before it.

## What it costs

A run on the two inputs of about 30 modules costs $0.26, from $0.22, and takes 35 to 48 turns on dev-helpdesk, from 14 to 37: the callers are searched for. The other eight inputs cost the same within a cent. The 30 runs cost $5.24, from $4.92.

## What is left

- **The one row that still differs between runs** is dev-bookings FR-007, the open row for code the trigger cannot reach: `unmet`, `partial`, `partial`. It was `partial` in 6 of 6 before, and in 3 of 3 on hold-mailing FR-008 after. Both verdicts are gaps, and no rule decides between them.
- **The set is at its ceiling again** on this model: every row is right. It shows a later change making verdicts worse, and it cannot show one making them better. Not measured: a project of hundreds of files, a second way in that is more than one call away, another model, and the real run's project.
- **The tally is miscounted in 3 of 30 replies**, as in the baseline (hold-depot twice, dev-bookings once). The dev-bookings reply again wrote "Correction: the tally must match the rows." and a second Tally line. build-phase counts the tally from the rows.
- **Line numbers past the end of the file:** one citation in one reply (`depot/api/handlers.py:339` in hold-depot, for a file of 29 lines), against 29 citations in 3 replies in the baseline. Nothing in the change is about line numbers, so this may be chance. That reply's transcript has two `Read` calls: it read the code with `cat` over several files at once, which shows no line numbers.
