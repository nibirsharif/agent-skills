# Baseline: write-plan 0.18.1

One run per input on `claude-sonnet-5-5` (Claude Code 2.1.327), 2026-11-24, with the skill as changed for [#10](https://github.com/nibirsharif/agent-skills/issues/10): cut the fewest phases that fit the limits, merge neighbours that fit as one, and let the requirement limit alone size the phases where there is no code to count files in. Scored by hand against each `reference.md` as the [README](README.md) says. The references are those of [baseline-0.14.0.md](baseline-0.14.0.md), unchanged, and its phase counts are beside the new ones.

| Input | Coverage | Phases (0.14.0; reference) | Before | Together | Blocked right |
|-------|----------|----------------------------|--------|----------|---------------|
| dev-document-sharing | 10 of 10 | 3 (6; 2 to 4) | 5 of 5 | 3 of 4 | yes |
| dev-feature-flags | 5 of 5 | 1 (1; 1) | none listed | 2 of 2 | yes |
| dev-table-booking | 12 of 12 | 2 (5; 2 to 4) | 7 of 7 | 4 of 4 | yes |
| **dev total** | 27 of 27 | 3 of 3 in range (1 of 3) | 12 of 12 | 9 of 10 | 3 of 3 |
| hold-parking-permits | 11 of 11 | 2 (4; 2 to 4) | 6 of 6 | 4 of 4 | yes |
| hold-profile-photo | 7 of 7 | 1 (4; 1, or 2) | none listed | 3 of 3 | yes |
| **hold total** | 18 of 18 | 2 of 2 in range (1 of 2) | 6 of 6 | 7 of 7 | 2 of 2 |
| **Total** | 45 of 45 | 5 of 5 in range (2 of 5) | 18 of 18 | 16 of 17 | 5 of 5 |

hold-message-search is scored apart, because its right reply is not a plan: it asked Q-001 and wrote no plan (yes), and it chose neither answer (yes).

Against 0.14.0, the totals other than the phase counts differ by one item (Together, 16 of 17 against 15 of 17), which the README reads as no change. No reply planned a withdrawn or blocked requirement or answered a question.

## Phases

The five plans have 9 phases, against 20 in 0.14.0, for the same 45 requirements. Three of the nine hold 7 or 8 requirements, and the two one-phase plans hold 5 and 7. The smallest are the availability target of dev-document-sharing on its own, as the rules allow, and the second phases of the three plans over the limit, which hold what the first left (3, 4, and 3 requirements).

With no codebase the file limit cuts nothing now. The sizes written are 3 to 10 files, so no plan shows a phase over the file limit, but they are guesses: an earlier run of dev-table-booking wrote `about 24 files` for the same 8-requirement phase that this run calls `about 10 files`.

## Together item missed

- dev-document-sharing T4, as in 0.14.0: the access log (FR-010) is in Phase 2 with the public links, after Phase 1 grants and revokes access. Its scope says the log records "every access change, from Phase 1 shares and from public links". Phase 1 has 6 requirements, so the limit did not force it.

## What the plans add

- hold-profile-photo plans that the web app shows the photo: a component "that shows the photo beside the user's name", and FR-001's check ends "and that the web app then shows it". The scope names showing a photo, but no written requirement states it; FR-006 covers only the initials. The 0.14.0 run said so in its Approach and planned neither. Replacing a photo, which the scope also names, is not planned.
- hold-parking-permits repeats the answer of the closed Q-003 in an interface line ("a resident may hold permits for several plates (closed Q-003)"). It is in the file, not invented, and the question is listed neither as blocked nor as open.

No reply names a file, and every Reuse is `None found.`

## The dev runs while the rules were written

The dev set ran three times; the table above is the third, on the final wording. The phase counts were 3, 1, and 2 in all three, with the same requirements in each phase of dev-feature-flags and dev-table-booking.

- dev-document-sharing T4 held in the first run (FR-010 in Phase 1) and missed in the second and third.
- The first wording said to "write Size as a rough guess", and two of the three replies then wrote `**Size:** about 14 files (rough guess, no code to count)`. The Size field now says `about <n> files` and nothing more, and no reply since has added to the line.

## The chain: write-tasks on the new plan

A phase filled to 8 requirements is larger than any the old rules cut, so the dev-table-booking plan was pasted into write-tasks (`claude-sonnet-5-5`, Claude Code 2.1.327). Its Phase 1 holds FR-001 to FR-005, FR-010, NFR-001, and NFR-002.

| `tasks_max_per_phase` | Runs | Result for Phase 1 |
|---|---|---|
| 12, the default until now | 3 | One run stopped with `Phase 1 needs more than 12 tasks.`; the others wrote 12 and 11 tasks. |
| 16, the default from this change | 3 | 10, 9, and 9 tasks; no stop. |

write-tasks counts one task per behaviour or interface and data change, plus the verify task, so a phase of 8 requirements sat at the old limit. The default is 16 from the same change. Phase 2, with 4 requirements, got 6 to 8 tasks in the five runs that wrote a list.
