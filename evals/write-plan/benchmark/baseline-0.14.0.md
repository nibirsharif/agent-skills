# Baseline: write-plan 0.14.0

One run per input on `claude-sonnet-5-5` (Claude Code 2.1.322), 2026-11-16, with the skill as on `master` after 0.14.0. Scored by hand against each `reference.md` as the [README](README.md) says. The references were written before the run.

| Input | Coverage | Phases (reference) | Before | Together | Blocked right |
|-------|----------|--------------------|--------|----------|---------------|
| dev-document-sharing | 10 of 10 | 6 (2 to 4) | 5 of 5 | 3 of 4 | yes |
| dev-feature-flags | 5 of 5 | 1 (1) | none listed | 2 of 2 | yes |
| dev-table-booking | 12 of 12 | 5 (2 to 4) | 7 of 7 | 4 of 4 | yes |
| **dev total** | 27 of 27 | 1 of 3 in range | 12 of 12 | 9 of 10 | 3 of 3 |
| hold-parking-permits | 11 of 11 | 4 (2 to 4) | 6 of 6 | 4 of 4 | yes |
| hold-profile-photo | 7 of 7 | 4 (1, or 2) | none listed | 2 of 3 | yes |
| **hold total** | 18 of 18 | 1 of 2 in range | 6 of 6 | 6 of 7 | 2 of 2 |
| **Total** | 45 of 45 | 2 of 5 in range | 18 of 18 | 15 of 17 | 5 of 5 |

hold-message-search is scored apart, because its right reply is not a plan: it asked Q-001 and wrote no plan (yes), and it chose neither answer (yes).

No reply invented a file, a requirement, or an answer to a question, and none planned a withdrawn or blocked requirement.

## Together items missed

- dev-document-sharing T4: the access log (FR-010) is Phase 4, after the phases that grant, revoke, and create links. Its scope says it "hooks into every path that changes access in Phases 1 and 3", so two merged phases change access with no log.
- hold-profile-photo T3: the thumbnail (FR-004, with NFR-001) is Phase 2, after the upload that stores the photo.

## Phases: more and smaller than the references

Three of five plans cut more phases than the reference range, and the phases are small: 22 requirements over 15 phases in those three plans, against a limit of 8 a phase. hold-profile-photo has 7 requirements in one flow, which the rules call one phase, and got 4 phases, one of them a single requirement and about 3 files.

The cause is the file limit, not the requirement limit. With no codebase, each phase is estimated at 3 to 9 files whatever it holds (a one-requirement email phase is "about 5 files"), so merging any two neighbours passes 10 files by the reply's own numbers. The estimates for hold-profile-photo add up to about 20 files. By those numbers the split follows rule 3 of Phases; the references assume estimates near 1 to 2 files a requirement. Which is right cannot be told without code, so read this column as "how finely the skill cuts", not as an error count. The eval cases do not catch it: `multi-phase` only asks for at least 3 phases.

## Other findings

- Every reply started at `## 1. Approach` and had no text outside the plan.
- hold-profile-photo's Approach notes that the scope names replacing and showing a photo but no written requirement covers them, and plans neither.
- dev-feature-flags, 5 requirements in one system, is one phase of about 7 files.

## After the too-large stop

The stop for a requirement too large for one phase was added the same day. A second run of the six inputs (`claude-sonnet-5-5`, Claude Code 2.1.322) checked only that the stop does not fire where a plan is due: all five inputs that need a plan got one, and hold-message-search asked its question as before. The phase counts were 5, 1, 5, 4, and 2 (dev-document-sharing, dev-feature-flags, dev-table-booking, hold-parking-permits, hold-profile-photo), against 6, 1, 5, 4, and 4 above; one run each, so the difference is not a result. The run was not scored further.

