# After the shorter instructions

The change for [#20](https://github.com/nibirsharif/agent-skills/issues/20): what write-spec reads on every run (`SKILL.md`, `ears-rules.md`, `examples.md`) went from about 8,000 to about 4,600 words. Saving and updating a file, follow-up replies, and the banned-word list moved to files read only in that situation. A run that saves a file read about 8,500 words before, with the template, and reads about 6,100 now, with `saving.md`; the benchmark runs are chat only, so they read the 4,600. One run per input on `claude-sonnet-5-5` with Claude Code 2.1.327, 2026-11-19, scored by hand the same way as [baseline-0.10.0.md](baseline-0.10.0.md). The benchmark ran before the last two wording fixes (the timeout keyword and the deadline percentage), which the eval cases cover.

The first turn was scored again on 2026-11-23, after hold-workspaces R1 was withdrawn ([#27](https://github.com/nibirsharif/agent-skills/issues/27)): no reply was run again. R1 asked what the notes service does with an invite opened after its 72 hours. This run's reply wrote the reject as FR-002, which counted as a missed gap and as an invented value, the only one in a first turn. "Valid for 72 hours" gives that refusal, as the skill's own example writes it for a link that expires, so it is now neither. Before, this record had 41 of 50 gaps found against the baseline's 44 of 50, and 1 invented value.

## First turn

| Input | Requirements written | Gaps found | Needed questions | Invented values |
|-------|----------------------|------------|------------------|-----------------|
| dev-invoice-export | 0 | 5 of 7 | 9 of 10 | 0 |
| dev-thermostat | 2 | 3 of 4 | 5 of 5 | 0 |
| dev-two-factor | 0 | 5 of 5 | 7 of 8 | 0 |
| dev-webhooks | 1 | 5 of 5 | 10 of 10 | 0 |
| dev-wishlist | 0 | 5 of 5 | 8 of 9 | 0 |
| **dev total** | 3 | 23 of 26 | 39 of 42 | 0 |
| hold-reminders | 2 | 3 of 4 | 5 of 6 | 0 |
| hold-search-api | 1 | 4 of 5 | 10 of 10 | 0 |
| hold-signup-form | 0 | 5 of 5 | 9 of 10 | 0 |
| hold-smart-lock | 2 | 4 of 5 | 5 of 6 | 0 |
| hold-workspaces | 6 | 2 of 4 | 5 of 5 | 0 |
| **hold total** | 11 | 18 of 23 | 34 of 37 | 0 |
| **Total** | 14 | 41 of 49 | 73 of 79 | 0 |

Questions held back behind `<N> more open questions after these.` are not counted: 3 in dev-invoice-export, 1 in hold-search-api, 2 in hold-signup-form.

### Gaps missed

- dev-invoice-export R6, R7: a day with no finalised invoices, and what "by morning" means (both may be among the 3 held back).
- dev-thermostat R4: the setpoint changing while the relay is on or off.
- hold-reminders R2: a moved appointment.
- hold-search-api R5: FR-001 wrote "sorted by relevance" into a requirement without asking what it means.
- hold-smart-lock R4: the reply asked where the 20% boundary falls, not whether the warning repeats.
- hold-workspaces R2, R5: an invite to an existing member, and what "leaves" means. Both were missed in both earlier records too.

## Follow-up turn

| Input | Requirements written | Gaps found | Needed questions | Invented values | `(new)` markers |
|-------|----------------------|------------|------------------|-----------------|-----------------|
| dev-invoice-export | 5 | 1 of 2 | 2 of 2 | 0 | present |
| dev-thermostat | 3 | 2 of 2 | 2 of 2 | 0 | present |
| dev-two-factor | 4 | 1 of 3 | 2 of 2 | 0 | present |
| dev-webhooks | 4 | 1 of 1 | 6 of 8 | 0 | present |
| dev-wishlist | 8 | none listed | 1 of 1 | 0 | present |
| **dev total** | 24 | 5 of 8 | 13 of 15 | 0 | |
| hold-reminders | 6 | 1 of 1 | 2 of 3 | 0 | present |
| hold-search-api | 10 | 1 of 2 | 4 of 4 | 0 | present |
| hold-signup-form | 9 | none listed | 2 of 2 | 0 | present |
| hold-smart-lock | 5 | none listed | 1 of 1 | 0 | present |
| hold-workspaces | 4 | 1 of 3 | 4 of 4 | 0 | present |
| **hold total** | 34 | 3 of 6 | 13 of 14 | 0 | |
| **Total** | 58 | 8 of 14 | 26 of 29 | 0 | |

"The held-back questions are now asked" (dev-invoice-export T2, hold-search-api T2) counts as found only when the reply asks at least that many questions beyond the listed decisions; both asked fewer.

## Compared

| | Baseline 0.10.0 | After coverage gaps | After shorter instructions |
|---|---|---|---|
| First turn: gaps found | 43 of 49 | 39 and 43 of 49 (two dev runs) | 41 of 49 |
| First turn: invented values | 0 | | 0 |
| Follow-up turn: gaps found | 7 of 14 | 10 of 14 | 8 of 14 |
| Follow-up turn: needed questions | 25 of 33 | 30 of 40 | 26 of 29 |
| Follow-up turn: invented values | 1 | | 0 |

## Reading

- First-turn gaps found are 2 below the baseline (43 to 41 of 49). The [README](README.md) treats a difference of fewer than three as no change, so this is no change by its measure. With R1 counted it was 3, a drop. Both items are in the held-out half (20 to 18 of 23); the dev half is unchanged (23 of 26). Against the coverage-gaps record the total is within that record's two-run spread, and the held-out half is 1 lower (19 to 18).
- Follow-up gaps found are 2 below the coverage-gaps record and 1 above the baseline: no change by the README's measure.
- No reply invented a value, in either turn. hold-workspaces FR-002 rejects an acceptance made more than 72 hours after the invite was sent, from "an invite is valid for 72 hours": that was scored as one until R1 was withdrawn. Two follow-up requirements, an expired code and an expired cursor, look invented until you check the first reply: it had asked about "incorrect or expired" codes and "invalid or expired" cursors.
- Every follow-up requirement carries its marker, as in the coverage-gaps record.
