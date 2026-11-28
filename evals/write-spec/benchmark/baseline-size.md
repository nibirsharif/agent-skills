# Baseline: the size of a spec

The first record of how large a spec grows ([#44](https://github.com/nibirsharif/agent-skills/issues/44)), with the skill as on `master` after 0.20.0. Three runs of each input's follow-up turn (`turn2.md`) on `claude-sonnet-5-5` (Claude Code 2.1.327), 27 November 2026, counted as the [README](README.md#size) says: the requirements and the open questions by [size.py](size.py), and the requirements from coverage gaps by hand, against the list in each `reference-turn2.md`. The statement counts and those lists were written before the runs were counted.

Each cell holds the three runs.

| Input | Statements | Requirements after the turn | Of them, from coverage gaps | Questions open |
|-------|------------|-----------------------------|-----------------------------|----------------|
| dev-invoice-export | 5 | 4, 7, 5 | 0, 0, 0 | 5, 4, 5 |
| dev-thermostat | 4 | 5, 6, 6 | 1, 2, 2 | 2, 3, 2 |
| dev-two-factor | 1 | 4, 4, 4 | 3, 3, 3 | 2, 3, 3 |
| dev-webhooks | 5 | 6, 6, 10 | 1, 1, 1 | 10, 9, 7 |
| dev-wishlist | 3 | 9, 10, 8 | 6, 6, 4 | 1, 3, 2 |
| **dev total** | 18 | 28, 33, 33 | 11, 12, 10 | 20, 22, 19 |
| hold-reminders | 4 | 8, 5, 4 | 5, 2, 1 | 5, 4, 3 |
| hold-search-api | 4 | 14, 11, 9 | 4, 4, 2 | 5, 4, 10 |
| hold-signup-form | 4 | 8, 8, 11 | 2, 3, 4 | 2, 2, 1 |
| hold-smart-lock | 4 | 4, 5, 5 | 2, 2, 2 | 2, 1, 2 |
| hold-workspaces | 5 | 9, 9, 9 | 2, 2, 2 | 3, 3, 3 |
| **hold total** | 21 | 43, 38, 38 | 15, 13, 11 | 17, 14, 19 |
| **Total** | 39 | 71, 71, 71 | 26, 25, 21 | 37, 36, 38 |

- **1.82 requirements for each input statement** after the follow-up turn: 213 for 117 in the three runs. 36 of the 213 are the 12 requirements of the fixed first replies.
- **About a third come from coverage-gap answers:** 72 of 213. Without them the specs hold 1.21 requirements for each statement. The fixed first replies ask 81 questions, 23 of them coverage-gap questions. A run turns those 23 answers into 24 requirements, about one each, and the other 58 answers into 35, since several of those fill one requirement (its system and its value).
- **111 questions are open after the turn,** 37 a run, each of which can add requirements in a turn the benchmark does not run.

## Reading

- The three totals are equal by chance. One input's count differs by up to 5 between runs (hold-search-api, 14 against 9), and the dev half ran from 28 to 33.
- The spread inside an input is not in what is asked or answered, which is fixed, but in how finely one answer is cut. The same answers of hold-search-api gave 14 requirements when the match in the name and the match in the description, and the order of each group, were each a requirement, and 9 when they were not. One dev-webhooks reply wrote the retry schedule as five requirements, one for each delay; the other two wrote it as one. A refusal is one requirement in some replies and two in others (dev-wishlist: display the sign-in page, and not add the product).
- An answer that names two cases is two requirements by rule, since an `or` between conditions is one requirement for each alternative: a cursor that is invalid or expired, a `q` that is missing or empty, an email that fails to send or bounces. In hold-search-api these are 4 of the 14.
- No `NFR` was written beside an `FR` for the same answer except in dev-invoice-export, where the 06:00 deadline is an `NFR` in every run, as the rules ask.

## What a limit on coverage gaps would cut

The issue's third option is to ask about the gaps of requirements that come from the input, and not about the gaps of a requirement that came from a gap answer.

- **In this turn it cannot change the requirement count.** Every requirement the follow-up turn writes comes from an answer to a question of the first reply, and a first reply has no requirement from a gap answer to ask about.
- **In the next turn it would cut about one question in five.** Read by hand, about 20 of the 111 open questions ask about a requirement that came from a coverage-gap answer (6, 7, and 7 in the three runs): what resets the count of wrong codes, what a log entry holds, when a cursor expires. One of them is an open decision of a reference, dev-two-factor `T3`, what a login does while the account is locked, which all three runs ask.
- **In the real run it would have cut nothing.** Its saved file has 7 coverage-gap questions, and none names a requirement that came from a coverage-gap answer ([2026-11-17.md](../../real-runs/2026-11-17.md#the-29-requirements-by-source)).

The option was also tried: one sentence added to the coverage-gap rule (`The check is one level deep: a requirement written from the answer to a coverage-gap question is not checked for gaps of its own, and no question is asked about it, unless the user asks for more.`), three runs of the five dev inputs.

| Dev set, three runs | Requirements after the turn | Questions open |
|---|---|---|
| Without the sentence | 28, 33, 33 (94) | 20, 22, 19 (61) |
| With it | 30, 33, 30 (93) | 18, 22, 21 (61) |

Neither count moved, and dev-two-factor still asked about the locked account in 3 of 3 runs, and about the count of wrong codes in 2 of 3. It is not taken: it would give up a decision the reference wants for a requirement count it does not lower.

## A size line in the reply

The issue's fourth option is a last line such as `12 requirements, 6 from coverage gaps.`, so the user sees the spec grow and can stop answering. It was tried with one rule in the Output section, one run of the five dev inputs.

| Input | The reply's last line | Requirements after the turn | From coverage gaps, by hand |
|-------|-----------------------|-----------------------------|-----------------------------|
| dev-invoice-export | `6 requirements, 0 from coverage gaps.` | 6 | 0 |
| dev-thermostat | `6 requirements, 0 from coverage gaps.` | 6 | 2 |
| dev-two-factor | `4 requirements, 0 from coverage gaps.` | 4 | 3 |
| dev-webhooks | `6 requirements, 0 from coverage gaps.` | 6 | 1 |
| dev-wishlist | `10 requirements, 0 from coverage gaps.` | 10 | 6 |

Every reply ended with the line and counted its requirements right, which tells the user what the reply already shows. The second number was 0 in all five and is right only where there were none. In a chat conversation the questions of an earlier reply carry no source, so the reply does not know which of the answers it wrote from were answers to coverage-gap questions. A saved file keeps that, as `Source: coverage gap in <ID>` on each such question, and `size.py --file` counts from it without a reply line. The line is not taken: its half that would show the spec growing from coverage gaps is wrong, and it would change the reply format of every write-spec case.

## Not measured

- A third turn, where the open questions are answered. The size after two turns is a floor.
- The first turn's size. Its requirement counts are in [after-drafts.md](after-drafts.md): 13, 17, and 18 for the ten inputs.
- A saved file's size on the benchmark. Every input is run in chat, where a requirement carries no `Source` comment, so its source is read by hand. The one saved file counted is the real run's.
