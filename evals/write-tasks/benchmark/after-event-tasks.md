# After one event per task

The change for [#44](https://github.com/nibirsharif/agent-skills/issues/44): a task builds one behaviour, and a behaviour is one event with everything the phase's requirements say about it: the requirement the event triggers, each `If ... then` requirement for that event going wrong, and an `NFR` that sets a threshold on its response. One task covers their IDs and has a check for each. Before, a requirement, its exception, and its `NFR` were three tasks, also when they changed the same function and the same test file. This record is also the first with a size measure, build tasks for each requirement, counted by [size.py](size.py).

Three runs of each input on each wording, `claude-sonnet-5-5` (Claude Code 2.1.327), 27 November 2026. "Before" is the skill as on `master` after 0.20.0.

## Size

| Input | Requirements | Build tasks before | Build tasks after |
|-------|--------------|--------------------|-------------------|
| dev-note-tags | 5 | 5, 5, 5 | 3, 3, 3 |
| dev-table-booking | 12 | 19, 18, 18 | 14, 14, 14 |
| **dev total, three runs** | 51 | 70 | 51 |
| hold-backup-verify | 6 | 7, 7, 8 | 4, 4, 4 |
| hold-parking-permits | 11 | 16, 15, 18 | 14, 15, 13 |
| **hold total, three runs** | 51 | 71 | 54 |
| **Total, three runs** | 102 | 141 | 105 |
| **Build tasks for each requirement** | | 1.38 | 1.03 |

- A build task covers two or more IDs in 43 of 105 tasks after, against 11 of 141 before.
- The held-out half moved as the dev half did: 1.39 to 1.06, against 1.37 to 1.00.
- The count is still above one task for each requirement where a plan lists interface and data items: each store, event, and endpoint of dev-table-booking and hold-parking-permits has a task of its own, as the rules ask since [#8](https://github.com/nibirsharif/agent-skills/issues/8). That rule is unchanged.

## The other columns

Run 1 of each wording, scored by hand against each `reference.md` as the [README](README.md) says.

Before:

| Input | Coverage | One behaviour | Order | Checks runnable | Manual right | Files right |
|-------|----------|---------------|-------|-----------------|--------------|-------------|
| dev-note-tags | 5 of 5 | 5 of 5 | 4 of 4 | 5 of 5 | 3 of 3 | 3 of 3 |
| dev-table-booking | 12 of 12 | 18 of 19 | 5 of 6 | 19 of 19 | 2 of 2 | 1 of 1 |
| hold-backup-verify | 6 of 6 | 7 of 7 | 3 of 3 | 7 of 7 | 3 of 3 | 3 of 3 |
| hold-parking-permits | 11 of 11 | 15 of 16 | 4 of 4 | 15 of 16 | 1 of 1 | 1 of 1 |
| **Total** | 34 of 34 | 45 of 47 | 16 of 17 | 46 of 47 | 9 of 9 | 8 of 8 |

After:

| Input | Coverage | One behaviour | Order | Checks runnable | Manual right | Files right |
|-------|----------|---------------|-------|-----------------|--------------|-------------|
| dev-note-tags | 5 of 5 | 3 of 3 | 4 of 4 | 3 of 3 | 3 of 3 | 3 of 3 |
| dev-table-booking | 12 of 12 | 12 of 14 | 5 of 6 | 14 of 14 | 2 of 2 | 1 of 1 |
| hold-backup-verify | 6 of 6 | 4 of 4 | 3 of 3 | 4 of 4 | 3 of 3 | 2 of 3 |
| hold-parking-permits | 11 of 11 | 14 of 14 | 4 of 4 | 14 of 14 | 1 of 1 | 1 of 1 |
| **Total** | 34 of 34 | 33 of 35 | 16 of 17 | 35 of 35 | 9 of 9 | 7 of 8 |

Every reply of both wordings copied the plan's blocked entries word for word, or wrote `None.`, and ended each phase with a verify task. No task of either has more than 3 files.

What three runs of each wording show, counted over all 24 replies:

| | Before | After |
|---|---|---|
| Coverage, by `size.py` | 102 of 102 | 102 of 102 |
| Order, by hand | 16, 17, 15 (48 of 51) | 16, 16, 16 (48 of 51) |
| An ID in a build task's Covers with its own check in that task's Done when | 152 of 152 | 152 of 152 |
| Tasks that hold two changes, by hand | 10 of 141 | 8 of 105 |
| hold-backup-verify `F2`, no guessed path | 1 of 3 | 0 of 3 |

- **Coverage** is unchanged: no ID lost its build task when tasks were joined.
- **Order** is unchanged. The items that fail are the two that [after-shorter-rules.md](after-shorter-rules.md) found the rules do not decide. dev-table-booking `O6` fails when the `no_show` status, with the lookup that frees its table, is built before the job that marks a no-show (2 of 3 before, 3 of 3 after). hold-backup-verify `O3` fails when no Phase 2 task depends on the Phase 1 task that verifies (1 of 3 before, 0 of 3 after).
- **Checks** are unchanged. A joined task writes one check for each ID, separated by `;`, in every one of the 43. The one check scored as not runnable, before, is hold-parking-permits FR-001, copied from the plan's Verify line, which names three inputs and no expected result. It is copied in 2 of 3 runs before, in 2 of 3 on the [first wording](#the-first-wording), and in none on the final one, where each reply adds the expected results.
- **One behaviour** has the same kind of miss on both wordings, a title that joins two interface or data items, and no task after joins two events. The two stores of dev-table-booking are one task in 3 of 3 runs before and after, and its tables store comes with the define-table endpoint in 2 of 3 and 3 of 3. Once each after: the two email templates of hold-parking-permits in one task, and hold-backup-verify's `mail_to` argument joined to the report. hold-parking-permits' retention setting with its purge job is one task in 2 of 3 runs before and none after.
- **Files:** hold-backup-verify `F2`, a test file that does not exist written as `` new: `tests/test_cli.py` ``, is the miss it was in the two earlier records (8 of 13 replies, then 11 of 19).

## What a joined task looks like

- An exception with its requirement: dev-note-tags `Add Store.add_tag with the 30-character limit` (FR-001, FR-002); dev-table-booking `Book a time slot and reject it when no free table fits` (FR-002, FR-003); hold-parking-permits `Submit a permit application` (FR-002, FR-003). All 9 replies to these three inputs after, and none before.
- An `NFR` with the requirement it limits: dev-note-tags `Filter notes list with --tag` (FR-003, NFR-001), with a timing test beside the filter test; dev-table-booking `Send the confirmation text within 30 seconds` (FR-004, NFR-001), with the load test script as the task's third file; hold-backup-verify `Add the backup verify command` (FR-002, FR-003, NFR-001).
- Two requirements that one event triggers: hold-backup-verify `Verify the nightly archive and report a failure` (FR-004, FR-005), the email and the red light for the same failed verification. Before, they were two tasks of the same file.
- Still apart: hold-parking-permits NFR-002, a retention period that limits no single response, and every interface and data item.

## The real run's plan

The plan of the [real run](../../real-runs/2026-11-17.md), 29 requirements in 5 phases, was tasked again in a copy of the project at the commit that saved the spec, three runs on each wording. The project is private, so only the counts are here.

| | Build tasks | For each requirement |
|---|---|---|
| The real run, 17 November | 24 | 0.83 |
| Before, three runs | 25, 29, 25 | 0.91 |
| After, three runs | 19, 19, 22 | 0.69 |

All 29 IDs are covered in every reply. Joined after: two ways the same value can be invalid, an option with its two exceptions, a failure with the exit code it sets, the last line of a report with the exit code that follows it, and two things the output must never hold. The run with 22 still wrote the option's two exceptions, and the failure's exit code, as tasks of their own, so the rule is not applied every time. The plan's two phases of 8 requirements have 3 to 7 build tasks after, against 5 to 8.

## The first wording

The first wording ended `it covers all their IDs and has a check for each. Only when its files would pass the limit does the exception or the NFR become the next task.` It gave the same size on the benchmark: 105 build tasks in three runs (53 dev, 52 hold), coverage 102 of 102, order 48 of 51. The new eval case [event-tasks](../cases/event-tasks/) showed its fault: with no codebase, 2 of 6 replies gave an exception a test file of its own, counted the files over the limit, and wrote the exception as the next task. The final wording says the exception's check goes in the test file of the requirement it is an exception to: 8 of 8, against 0 of 6 before the change.

## The phase limit, not changed

The issue's second option is that write-plan's limit of 8 requirements a phase counts `FR` IDs only, so an `FR` and its `NFR` do not take two places. It was tried on write-plan's six dev inputs, one run, with one sentence changed in its rules:

| | dev-document-sharing | dev-feature-flags | dev-note-tags | dev-note-tags-small-limit | dev-saved-searches | dev-table-booking | Total |
|---|---|---|---|---|---|---|---|
| Phases, `FR` and `NFR` counted ([baseline-0.19.0.md](../../write-plan/benchmark/baseline-0.19.0.md)) | 3 | 1 | 1 | 2 | 1 | 2 | 10 |
| Phases, `FR` only | 2 | 1 | 1 | 2 | 1 | 2 | 9 |

One plan lost one phase: dev-document-sharing has 8 `FR` and 2 `NFR`, and its first two phases became one of 9 IDs. dev-table-booking has 10 `FR` and still needs two. write-plan's benchmark calls a difference of fewer than two items no change, and the real run's file has no `NFR` at all, so it would have had the same phases. It is not taken. What a requirement costs in a phase is less now: the real plan's two phases of 8 requirements have 3 to 7 build tasks, against 5 to 8. A spec of many small requirements can still raise `plan_max_requirements_per_phase`.

## Not measured

- A build from the new task lists. implement-task and build-phase were not run on a joined task, so whether one commit for a requirement with its exception is built and verified as well as two is not known.
- A plan written by today's write-plan. The two pasted plans are the ones 0.14.0 gave, of 2 to 5 requirements a phase, and the real plan was written before [#10](https://github.com/nibirsharif/agent-skills/issues/10).
- `tasks_max_per_phase`. Its default stays 16, though a phase now needs fewer tasks.
