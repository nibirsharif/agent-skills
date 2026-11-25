# Baseline: write-plan 0.18.1

One run per input on `claude-sonnet-5-5` (Claude Code 2.1.327), 2026-11-24, with the skill as changed for [#10](https://github.com/nibirsharif/agent-skills/issues/10): cut the fewest phases that fit the limits, merge neighbours that fit as one, and let the requirement limit alone size the phases where there is no code to count files in. Scored by hand against each `reference.md` as the [README](README.md) says. The references of the six inputs that [baseline-0.14.0.md](baseline-0.14.0.md) scored are unchanged, and its phase counts are beside the new ones. The two `dev-note-tags` inputs are new with this change: they have a project with code, and their references were written before their first run.

| Input | Coverage | Phases (0.14.0; reference) | Before | Together | Code | Blocked right |
|-------|----------|----------------------------|--------|----------|------|---------------|
| dev-document-sharing | 10 of 10 | 3 (6; 2 to 4) | 5 of 5 | 4 of 4 | no project | yes |
| dev-feature-flags | 5 of 5 | 1 (1; 1) | none listed | 2 of 2 | no project | yes |
| dev-table-booking | 12 of 12 | 2 (5; 2 to 4) | 7 of 7 | 4 of 4 | no project | yes |
| **dev total, without code** | 27 of 27 | 3 of 3 in range (1 of 3) | 12 of 12 | 10 of 10 | | 3 of 3 |
| dev-note-tags | 5 of 5 | 1 (new; 1) | none listed | 2 of 2 | 4 of 4 | yes |
| dev-note-tags-small-limit | 5 of 5 | 2 (new; 2 to 3) | 2 of 2 | 2 of 2 | 4 of 4 | yes |
| **dev total, with code** | 10 of 10 | 2 of 2 in range | 2 of 2 | 4 of 4 | 8 of 8 | 2 of 2 |
| hold-parking-permits | 11 of 11 | 2 (4; 2 to 4) | 6 of 6 | 4 of 4 | no project | yes |
| hold-profile-photo | 7 of 7 | 1 (4; 1, or 2) | none listed | 3 of 3 | no project | yes |
| **hold total** | 18 of 18 | 2 of 2 in range (1 of 2) | 6 of 6 | 7 of 7 | | 2 of 2 |
| **Total of the five plans 0.14.0 scored** | 45 of 45 | 5 of 5 in range (2 of 5) | 18 of 18 | 17 of 17 | | 5 of 5 |

hold-message-search is scored apart, because its right reply is not a plan: it asked Q-001 and wrote no plan (yes), and it chose neither answer (yes).

Against 0.14.0, the totals other than the phase counts differ by two items (Together, 17 of 17 against 15 of 17). No reply planned a withdrawn or blocked requirement or answered a question.

## Phases

The five plans that 0.14.0 scored have 9 phases, against 20, for the same 45 requirements. Three of the nine hold 7 or 8 requirements, and the two one-phase plans hold 5 and 7. The smallest are the availability target of dev-document-sharing on its own, as the rules allow, and the second phases of the three plans over the limit, which hold what the first left (2, 4, and 3 requirements).

With no codebase the file limit cuts nothing now. The sizes written are 3 to 10 files, so no plan shows a phase over the file limit, but they are guesses: earlier runs of dev-table-booking wrote `about 24 files`, `about 14 files`, and `about 12 files` for the same 8-requirement phase that this run calls `about 9 files`.

## With code

The two `dev-note-tags` inputs run in a project: a Python package with tests and a page in plain JavaScript, with the requirements read from `docs/specs/note-tags/requirements.md`. Five requirements change about six files.

- dev-note-tags, default limits: one phase, `about 6 files`. Reuse names `notes/store.py`, `notes/cli.py`, `web/app.js`, and both test files, each with the function or pattern to build on, and no path that is not in the project.
- dev-note-tags-small-limit, `plan_max_files_per_phase: 4`: two phases, tags in the store with the filter (4 requirements, `about 4 files`) and tags on the page (1 requirement, `about 2 files`). Its Approach says the limit is 4 files a phase, so the page is its own phase, because it shares no file with the store and command-line work. The four requirements of Phase 1 share two source files and two test files, so a count of files per requirement would have cut it further; each file is counted once.
- Neither names a tool the project lacks, and both check FR-004 by opening the page, saying it has no tests.

Both inputs ran three times while the rules were written, with the same phases and sizes each time. They are one small project: a feature of many files, and a phase that the file limit cuts while it also holds 8 requirements, are not measured.

## The together item that 0.14.0 missed

dev-document-sharing T4: the access log (FR-010) belongs in the first phase that changes access. 0.14.0 put it in a fourth phase, and the first wording of this change put it in Phase 2, with the public links, in 2 of 3 runs, though Phase 1 had room. The Order step now says that a requirement that applies to what several phases build goes in the first of them. With that sentence FR-010 is in Phase 1 in 5 of 5 runs.

## What the plans add

- hold-profile-photo plans that the web app shows the photo: a component "that shows the photo, or the user's initials when the user has no photo". The scope names showing a photo, but no written requirement states it; FR-006 covers only the initials, "in place of the profile photo". The 0.14.0 run said so in its Approach and planned neither. Both hold runs of this change plan it, the first also in FR-001's check. Replacing a photo, which the scope also names, is not planned. It is left as it is: a rule made from a hold reply would end the hold set's use.
- In the first of the two hold runs, hold-parking-permits repeated the answer of the closed Q-003 in an interface line. It is in the file, not invented, and the question was listed neither as blocked nor as open. The second run does not mention it.

No reply for an input without a project names a file, and each of their Reuse lines is `None found.`

## The runs while the rules were written

The three dev inputs without code ran at least five times each, and the hold set twice: once on the wording without the Order sentence and once on the final wording, which the table shows. The phase counts were the same every time: 3, 1, and 2 for the dev inputs, 2 and 1 for the hold plans, and the question for hold-message-search.

The first wording said to "write Size as a rough guess", and two of the three replies then wrote `**Size:** about 14 files (rough guess, no code to count)`. The Size field now says `about <n> files` and nothing more, and no reply since has added to the line.

## The chain: write-tasks on the new plan

A phase filled to 8 requirements is larger than any the old rules cut, so the dev-table-booking plan was pasted into write-tasks (`claude-sonnet-5-5`, Claude Code 2.1.327). Its Phase 1 holds FR-001 to FR-005, FR-010, NFR-001, and NFR-002, in every run of that input.

| `tasks_max_per_phase` | Runs | Result for Phase 1 |
|---|---|---|
| 12, the default until now | 3 | One run stopped with `Phase 1 needs more than 12 tasks.`; the others wrote 12 and 11 tasks. |
| 16, the default from this change | 3 | 10, 9, and 9 tasks; no stop. |

write-tasks counts one task per behaviour or interface and data change, plus the verify task, so a phase of 8 requirements sat at the old limit. The default is 16 from the same change. Phase 2, with 4 requirements, got 6 to 8 tasks in the five runs that wrote a list. These runs used the plans of earlier dev runs, before the Order sentence, which have the same requirements in each phase as the final one.
