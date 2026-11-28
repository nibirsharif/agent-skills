# write-spec benchmark

The eval cases in [../cases/](../cases/) check that a reply follows the skill's rules. This benchmark measures something else: how good the requirements and questions are for inputs the rules were not written against.

Each folder holds an `input.md` and a `reference.md`. The agent sees only the input. The reference lists the decisions the input leaves open (`R1`, `R2`, ...) and the values the input does not give.

## The two sets

- `dev-*`: read these replies when changing a rule.
- `hold-*`: never tune a rule on these. Run them only to check that a change which helped the dev set helps here too.

Both sets cover a device, an API, a user interface, and a scheduled or permission-based feature, in different forms: statements, bullets, a user story, meeting notes, a one-line idea.

## Running

```bash
python3 evals/bench.py write-spec --model sonnet --label <name>
```

This runs each input once and saves the replies in `../runs/bench-<name>/`. It costs tokens. Nothing is graded automatically.

Add `--file turn2.md` to run the follow-up turn instead. Each `turn2.md` holds the input, the first reply that release 0.10.0 gave, and scripted answers to its questions; `reference-turn2.md` lists the decisions still open after those answers. The first reply is fixed, so a turn-2 score does not depend on what a new first reply would ask.

## Scoring

Score each reply by hand, or with a judge model, against its `reference.md`:

- **Gaps found:** how many `R` items the reply asks about. An item that the reply decides on its own, in a requirement or a draft, counts as not found and as an invented value.
- **Requirements written** and **drafts shown:** counts of `FR` and `NFR` lines, and of `Draft:` lines. A reply with neither wrote nothing ([#21](https://github.com/nibirsharif/agent-skills/issues/21)).
- **Needed questions:** how many of the reply's questions a reviewer needs answered before the feature can be built and tested. A question that matches an `R` item is needed. A question outside the list is judged on its own.
- **Invented values:** how many systems, values, names, or behaviours appear in a requirement or a draft that the input did not give. A `[Q-NNN]` slot in a draft is not a value. A time that something expires after, or is valid for, gives the refusal that follows it: a requirement that rejects the late use is not invented, as in the skill's own example for "The link expires 30 minutes after it is sent" ([#27](https://github.com/nibirsharif/agent-skills/issues/27)).

Compare the totals across all inputs, not single inputs: each input runs once, so one reply can vary. Treat a difference of fewer than three items in a total as no change.

## Size

How large a spec grows is measured on the follow-up turn, where the answers become requirements ([#44](https://github.com/nibirsharif/agent-skills/issues/44)). A size is not a score: a larger spec is not a worse one. It is recorded so that a change which makes specs larger or smaller is seen.

```bash
python3 evals/bench.py write-spec --model claude-sonnet-5-5 --label <name> --file turn2.md --runs 3
python3 evals/write-spec/benchmark/size.py <name>
```

[size.py](size.py) counts, for each reply:

- **Statements:** the `Statements: <n>` line of the input's `reference.md`. A statement is a sentence or a list item of the input that states a behaviour or a property of a system. A title, the story line above a user story's acceptance criteria, and a question that the next sentence answers are not counted on their own.
- **Requirements after the turn:** those of the fixed first reply in `turn2.md`, plus the reply's `(new)` lines, less its withdrawn ones, and the same number for each statement.
- **Questions open:** the reply's `Q` lines, with the `<N> more open questions` it holds back. Each can add requirements in a turn the benchmark does not run.

One count is made by hand:

- **From coverage gaps:** how many of the requirements after the turn state a case in the `Coverage-gap questions in the first reply` list of the input's `reference-turn2.md`. The list names the questions of the fixed first reply that ask about a case the input does not mention (a failure, the other side of a condition, a refusal), not about what a statement of the input means or lacks. A requirement the reply changes, and one it writes from another answer, is not counted.

The first record is [baseline-size.md](baseline-size.md). Its three runs each had 71 requirements, but one input's count differed by up to 5 between runs, and so did each half's total. Treat a difference of fewer than six requirements in a total as no change.

For a saved file, `python3 evals/write-spec/benchmark/size.py --file <requirements.md>` counts the written requirements by the first source their `Source` comment names, and the coverage-gap questions by the source of the requirement each names. It is how a [real run](../../real-runs/) records where its requirements came from.

## Changing the references

A reference list is a reviewer's opinion of what the input leaves open. Change it only for a reason that does not depend on what the skill replied, and score the baseline again when it changes.

An item that is withdrawn keeps its number and says why, so the records that name the other items still read correctly. It is not counted: hold-workspaces has four items since R1 was withdrawn, and the totals are of 49.
