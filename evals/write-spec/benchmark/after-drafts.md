# After drafts for statements that wait on a question

The change for [#21](https://github.com/nibirsharif/agent-skills/issues/21): a statement that lacks only a system name or a value is shown as a `Draft:` line below the questions, the EARS sentence it will become with `[Q-NNN]` where the missing part goes. A draft has no ID and is never saved. The rules for drafts are in `references/drafts.md`, which the workflow opens only after the requirements and questions are linted.

All runs on `claude-sonnet-5-5` with Claude Code 2.1.327, 2026-11-25, first turn only. Needed questions were not scored, and the follow-up turn was not run. The benchmark ran before the last two wording fixes to `drafts.md` (what the reply's first line is when no draft is added, and three example words for an impression), which the eval cases cover: see the [eval README](../README.md#drafts).

## How the replies were scored

Gaps found were scored by a judge model, `claude-opus-5-5`, given the reference list, the reply, and the rules of the [README](README.md): an item is found when a question in the reply asks for it or for a main part of it, a neighbouring case does not count, and questions held back behind the `<N> more open questions` line do not count. The 35 replies scored by hand first (the after-code-facts replies, option 3 below, and two runs of the first build on all ten inputs) got the same score from the judge on every item, and so did six replies of the final runs checked by hand afterwards. Requirements, drafts, and questions are line counts. Invented values were read by hand in every requirement and draft of the final runs.

## Before: the skill without drafts

The skill as it was on `master`, four runs of each half: the [after-code-facts](after-code-facts.md) replies, scored here for gaps for the first time, and three new runs.

| | Run 1 (after-code-facts) | Run 2 | Run 3 | Run 4 | Mean |
|---|---|---|---|---|---|
| dev: gaps found, of 26 | 24 | 21 | 23 | 24 | 23.0 |
| hold: gaps found, of 23 | 19 | 18 | 18 | 18 | 18.3 |
| dev: replies with no requirement | 3 of 5 | 3 of 5 | 3 of 5 | 3 of 5 | |
| hold: replies with no requirement | 1 of 5 | 2 of 5 | 1 of 5 | 2 of 5 | |

The total is about 41 of 49, and 4 or 5 replies of 10 write nothing. One run varies by three items in the dev half alone.

## The three options, on the dev set

The issue lists three options. Each was written into a copy of the skill and run once on the five dev inputs.

| | Gaps found | Requirements | Drafts | Replies with neither |
|---|---|---|---|---|
| 1. Ask only the question that blocks most statements | 11 of 26 | 4 | | 3 of 5 |
| 3. `(blocks N)` after the ID of a question that blocks two or more statements | 23 of 26 | 4 | | 3 of 5 |
| 2. Drafts | 20 of 26 | 4 | 11 | 1 of 5 |

- Option 1 holds back what the benchmark counts: its three empty replies each asked one question, and two of them, dev-two-factor and dev-wishlist, did not say that more were open.
- Option 3 labelled 3 questions of 39. The replies are otherwise the same as before.
- Option 2 is the only one that leaves fewer replies empty, so it was built.

## Where the draft rules are read decides the questions

The first builds put the draft rules in `SKILL.md`, read before the reply is written. Every one of them asked fewer questions and found fewer gaps than the skill without drafts, wherever the drafts stood in the reply.

| Build | dev: gaps found, of 26 | hold: gaps found, of 23 |
|-------|------------------------|-------------------------|
| Without drafts | 24, 21, 23, 24 | 19, 18, 18, 18 |
| Rules in `SKILL.md`, drafts above the questions | 20, 21, 22, 21, 22, 21, 19 | 19, 17 |
| The same, with the coverage-gap check as its own step | 20, 23 | |
| The same, "settle the questions first, a draft changes neither" | 22, 19, 22 | |
| Rules in `SKILL.md`, drafts below the questions | 23, 22, 21 | 15, 17, 18 |
| The same, with a lint before the drafts and one after | 21, 21, 23 | |
| Rules in `drafts.md`, opened after the lint (two earlier wordings of that file) | 23, 24, 21, 22, 21, 24, 21, 23, 22 | 17, 19, 17 |
| The same, final wording | 23, 23, 23 | 17, 18, 16 |

- With the rules read up front, the five dev replies together held 33 to 37 questions in 10 of the 11 runs counted, and 42 in one, against 36 to 43 without drafts. With the rules in `drafts.md` they hold 33 to 41. A draft's slots also split one question into several, which pushed questions past the limit of 10: dev-invoice-export R6 was not asked in 4 of the 9 runs of the first build.
- No dev-wishlist reply of the first build, in nine runs, asked whether a shopper must be signed in. With the rules opened after the lint, 3 of 12 did; without drafts, 3 of 4.
- With the rules in `drafts.md`, the model writes and lints the same reply as before, then opens the file and adds the drafts. In ten transcripts every run linted a reply with no draft before it read `drafts.md` (one read it in the same command as that lint), and the final reply held as many questions as the linted one. Where a question's wording changed, the first lint had noted a question that asked two things, which the skill without drafts fixes the same way.

## The final wording, all ten inputs

Three runs. Gaps found for each input, then the totals.

| Input | Before (mean of 4) | Run 1 | Run 2 | Run 3 |
|-------|--------------------|-------|-------|-------|
| dev-invoice-export | 6.8 of 7 | 7 | 7 | 7 |
| dev-thermostat | 3 of 4 | 3 | 3 | 3 |
| dev-two-factor | 5 of 5 | 5 | 5 | 5 |
| dev-webhooks | 4.5 of 5 | 5 | 5 | 5 |
| dev-wishlist | 3.8 of 5 | 3 | 3 | 3 |
| **dev total** | 23.0 of 26 | 23 | 23 | 23 |
| hold-reminders | 3 of 4 | 3 | 3 | 1 |
| hold-search-api | 4 of 5 | 4 | 4 | 4 |
| hold-signup-form | 5 of 5 | 5 | 5 | 5 |
| hold-smart-lock | 4.3 of 5 | 4 | 4 | 5 |
| hold-workspaces | 2 of 4 | 1 | 2 | 1 |
| **hold total** | 18.3 of 23 | 17 | 18 | 16 |
| **Total** | 41.3 of 49 | 40 | 41 | 39 |
| Requirements written | 11 to 22 | 13 | 17 | 18 |
| Drafts shown | | 19 | 15 | 15 |
| Replies with neither | 4 or 5 of 10 | 0 | 1 | 0 |
| Invented values | 0 | 0 | 0 | 0 |

## Reading

- Fewer first replies write nothing: 0, 1, and 0 of 10 against 4 or 5. The one reply with neither is dev-two-factor, whose reference says no requirement can be written from it.
- Gaps found are 40, 41, and 39 of 49 against a mean of 41.3 without drafts, whose own four runs pair up to between 39 and 43. The README calls a difference of fewer than three no change, and each of the three runs is within three of the mean. The dev half is the same, 23 against 23.0. The held-out half is 17.0 against 18.3: hold-workspaces R3, what a refused delete returns, was asked in 1 of 6 runs with `drafts.md` and in 3 of 4 without, and one hold-reminders reply asked 4 questions and missed two more items than any other. With three and four runs a difference of one item in a half is not shown to be real or to be noise.
- No requirement or draft of the final runs holds a system, value, or name the input does not give. Every draft of the final wording keeps to the input's words and its slots, such as `shall retry the delivery [Q-003] [Q-004]`. Earlier wordings framed a slot with words taken from its question: "in the [Q-007] header" once in the first build, "with the secret held [Q-006]" once in 15 dev replies of an earlier `drafts.md`. The rule now says to add no word around a slot, not even one its question uses, and shows a wrong and a right draft.
- Two wordings in requirements are scored as not invented because after-code-facts.md scored them so: the 10 seconds "of the request being sent" in one dev-webhooks reply, and a refused delete written as a rejected request in hold-workspaces.
- dev-two-factor got a draft in 2 of the 3 final dev runs, such as `When a user logs in, the [Q-001] shall request [Q-002].` The rule says to write none when the input does not say what the system does. The drafts hold no value, and both replies asked every item of the reference.
- Of 46 dev replies to dev-invoice-export, dev-webhooks, and dev-wishlist run with `drafts.md`, 2 showed no draft: one dev-invoice-export reply and one dev-wishlist reply, on earlier wordings of the file. The ten transcripts that were kept all read the file and added drafts, so why those two did not is not known.
- Requirements written are 13, 17, and 18, inside the 11 to 22 of the four runs without drafts.
- A reply costs about $0.16 against $0.14, for the second file and the second lint.

## Not measured

- The follow-up turn: whether a draft whose slots are answered comes back as a requirement marked `(new)`, and whether a draft with one slot still open is shown again.
- Needed questions.
- A reply that saves a file. The lint fails a `Draft:` line in a file, and no run saved one.
