# After the shorter rules

The change for [#24](https://github.com/nibirsharif/agent-skills/issues/24): what write-tasks reads on every run (`SKILL.md`, `task-rules.md`, `examples.md`, `tasks-template.md`) went from 3,928 to 3,225 words. One run per input on `claude-sonnet-5-5` (Claude Code 2.1.327), 19 November 2026, before and after the change, scored against each `reference.md` as the [README](README.md) says.

Before the change:

| Input | Coverage | One behaviour | Order | Checks runnable | Manual right | Files right |
|-------|----------|---------------|-------|-----------------|--------------|-------------|
| dev-note-tags | 5 of 5 | 5 of 5 | 4 of 4 | 5 of 5 | 3 of 3 | 3 of 3 |
| dev-table-booking | 12 of 12 | 16 of 17 | 5 of 6 | 17 of 17 | 2 of 2 | 1 of 1 |
| **dev total** | 17 of 17 | 21 of 22 | 9 of 10 | 22 of 22 | 5 of 5 | 4 of 4 |
| hold-backup-verify | 6 of 6 | 7 of 8 | 3 of 3 | 8 of 8 | 3 of 3 | 2 of 3 |
| hold-parking-permits | 11 of 11 | 19 of 19 | 4 of 4 | 19 of 19 | 1 of 1 | 1 of 1 |
| **hold total** | 17 of 17 | 26 of 27 | 7 of 7 | 27 of 27 | 4 of 4 | 3 of 4 |
| **Total** | 34 of 34 | 47 of 49 | 16 of 17 | 49 of 49 | 9 of 9 | 7 of 8 |

After:

| Input | Coverage | One behaviour | Order | Checks runnable | Manual right | Files right |
|-------|----------|---------------|-------|-----------------|--------------|-------------|
| dev-note-tags | 5 of 5 | 5 of 5 | 4 of 4 | 5 of 5 | 3 of 3 | 3 of 3 |
| dev-table-booking | 12 of 12 | 15 of 17 | 5 of 6 | 17 of 17 | 2 of 2 | 1 of 1 |
| **dev total** | 17 of 17 | 20 of 22 | 9 of 10 | 22 of 22 | 5 of 5 | 4 of 4 |
| hold-backup-verify | 6 of 6 | 7 of 8 | 2 of 3 | 8 of 8 | 3 of 3 | 2 of 3 |
| hold-parking-permits | 11 of 11 | 15 of 16 | 4 of 4 | 16 of 16 | 1 of 1 | 1 of 1 |
| **hold total** | 17 of 17 | 22 of 24 | 6 of 7 | 24 of 24 | 4 of 4 | 3 of 4 |
| **Total** | 34 of 34 | 42 of 46 | 15 of 17 | 46 of 46 | 9 of 9 | 7 of 8 |

Every reply on either wording copied the plan's blocked entries word for word, or wrote `None.`, and ended each phase with a verify task. No task had more than 3 files.

Two columns differ, and two rows changed on the way to the final wording. Each was run again to tell the change from the spread between runs.

## One behaviour: the spread between runs is as wide as the difference

Four tasks hold two changes after (dev-table-booking `Add the time_slots and bookings stores` and `Add the no_show status and release its table`, hold-backup-verify ``Add `mail_to` to `run` and verify the archive it wrote``, hold-parking-permits `Add the 6-year retention setting and purge job`), against two before. The whole benchmark run three times on each wording:

| Wording | Run 1 | Run 2 | Run 3 | Tasks holding two changes |
|---|---|---|---|---|
| Before the change | 47 of 49 | 46 of 49 | 45 of 49 | 9 of 147 |
| The cut wording, before two examples were restored (below) | 43 of 47 | 46 of 49 | 46 of 48 | 9 of 144 |

The same titles come back on both: the two stores of dev-table-booking in one task in 8 of 8 runs before and 21 of 21 after, and the `mail_to` argument joined to the verification in most runs of hold-backup-verify. The [0.14.0 baseline](baseline-0.14.0.md) had 4 of 44.

## A `manual:` check without its ID: two examples restored

dev-table-booking's NFR-002 has two checks, a scan and a pass by a person. Some replies write them as `NFR-002: <scan>; manual: <pass>`, so the second has no ID before `manual:` and a reader that looks for `<ID>: manual:` misses it. The 0.14.0 baseline had it too. dev-table-booking run again:

| Wording | `manual:` without its ID |
|---|---|
| Before the change | 1 of 8 |
| The first cuts | 4 of 13 |
| Final: the cuts with two examples restored | 0 of 8 |

The first cuts had taken out the two places that show the format outside the rule itself: the example in the rule that a check says what to do and see (`FR-007: manual: in the browser, ...`), and the wrong example of a check for a person with the word missing. 4 of 13 against 1 of 8 is a small sample, but both removed texts bear on what missed, so both are back. The rules still do not say what an ID with two checks looks like; that would be a new rule, not a trim.

## Order: two items that the rules do not decide

- dev-table-booking O6 (marking a no-show comes before releasing its table) fails in the row above on both wordings. The plan lists a `no_show` status under Interface and data changes, and since 0.17.0 every such item gets a task: the reply builds the status first, with FR-009's check, and the job that marks a no-show second. O6 held in 1 of 8 runs before the change, 7 of 13 on the first cuts, and 3 of 8 on the final wording. The reference was written before that rule.
- hold-backup-verify O3 (the task that reports a failed verification depends on the Phase 1 task that verifies, and on no task after it) fails in the row after: Phase 2's first task depends on Phase 1's verify task. Run side by side in two batches, O3 held in 5 of 10 runs on each wording; the other runs depend on Phase 1's verify task (6 of the 10 misses) or on no Phase 1 task at all (4). In the runs made earlier the same evening it held in 3 of 3 before the change and 4 of 4 on the cuts, then in 1 of 5 on the final wording, so it moved between batches more than between wordings. The rules allow a dependency on any task of an earlier phase and do not say which.

## Other findings

- Files: hold-backup-verify F2 fails on both wordings, as in the 0.14.0 baseline: test files that do not exist are written as `` new: `tests/test_cli.py` `` and `` new: `tests/test_schedule.py` ``, a guessed path. 8 of 13 replies to this input did it before the change and 11 of 19 after.
- Text the contract does not allow at the end of a chat reply: 3 of the 27 replies before the change (dev-note-tags ended with `Not saved: chat only, as requested.`, and hold-backup-verify twice with a `## 4. Revision History` table), and none of the 50 after. The reply contract now holds the chat-reply rules that were in a separate Output section.
- One hold-backup-verify reply before the change wrote a task's `**Depends on:**` as `**Depends:**`.
- The `manual:` choice was right every time it was tested, on both wordings.
