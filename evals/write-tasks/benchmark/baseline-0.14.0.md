# Baseline: write-tasks 0.14.0

One run per input on `claude-sonnet-5-5` (Claude Code 2.1.322), 2026-11-16, with the skill as on `master` after 0.14.0. Scored by hand against each `reference.md` as the [README](README.md) says. The references were written before the run.

| Input | Coverage | One behaviour | Order | Checks runnable | Manual right | Files right |
|-------|----------|---------------|-------|-----------------|--------------|-------------|
| dev-note-tags | 5 of 5 | 5 of 5 | 4 of 4 | 5 of 5 | 3 of 3 | 3 of 3 |
| dev-table-booking | 12 of 12 | 18 of 19 | 6 of 6 | 19 of 19 | 2 of 2 | 1 of 1 |
| **dev total** | 17 of 17 | 23 of 24 | 10 of 10 | 24 of 24 | 5 of 5 | 4 of 4 |
| hold-backup-verify | 6 of 6 | 6 of 7 | 3 of 3 | 8 of 8 | 3 of 3 | 2 of 3 |
| hold-parking-permits | 11 of 11 | 11 of 13 | 4 of 4 | 13 of 13 | 1 of 1 | 1 of 1 |
| **hold total** | 17 of 17 | 17 of 20 | 7 of 7 | 21 of 21 | 4 of 4 | 3 of 4 |
| **Total** | 34 of 34 | 40 of 44 | 17 of 17 | 45 of 45 | 9 of 9 | 7 of 8 |

Every reply copied the plan's blocked entries word for word, or wrote `None.`, and ended each phase with a verify task. No task had more than 3 files, and no task depended on a later one.

## Tasks that hold two changes

Four titles join two changes with "and":

- dev-table-booking T-3.2: "Add the SMS provider configuration and send call".
- hold-backup-verify T-2.1: "Verify the nightly archive and turn the light red on failure".
- hold-parking-permits T-1.1: "Add the application endpoint and record".
- hold-parking-permits T-2.2: "Index permits for the plate check and measure the deadline": a migration and a load test.

## Files item missed

- hold-backup-verify F2: two files that do not exist are written as `` new: `tests/test_cli.py` `` and `` new: `tests/test_schedule.py` ``. The rules ask for `new: <what it is>`, never a guessed path. Later tasks then name those paths as existing files.

## Other findings

- The `manual:` choice was right every time it was tested. dev-note-tags made the page check `manual:` and the four others tests; hold-backup-verify tested the email with a stand-in for `send` and did not fall back to a real inbox; dev-table-booking kept the plan's screen-reader pass as `manual:` beside the automated scan.
- dev-table-booking T-2.3 writes its two checks for one ID as `NFR-002: <scan>; manual: <pass>`. The second has no ID before `manual:`, so a reader that looks for `<ID>: manual:` misses it there. The verify task writes it as `NFR-002: manual:`.
- hold-backup-verify proves NFR-001 with a new script that is run by hand, not with a test in the suite. A command to run is allowed; `make test` will not repeat it.
- hold-backup-verify ran twice. The plan first said the mail address came from "the config", and the project has no config loader. The skill wrote no task and asked where the setting lives, which is what the rules say for a phase too vague to task. The plan was a fixture mistake: it now passes the address to `run` as an argument, and the row above is the second run.
- Like the verify-spec baseline, most columns are at their ceiling, so this set can show a change making tasks worse more easily than better. "One behaviour" and "Files right" are the two with room.
