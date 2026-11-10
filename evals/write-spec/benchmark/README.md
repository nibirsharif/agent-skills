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

- **Gaps found:** how many `R` items the reply asks about. An item that the reply decides on its own, in a requirement, counts as not found and as an invented value.
- **Needed questions:** how many of the reply's questions a reviewer needs answered before the feature can be built and tested. A question that matches an `R` item is needed. A question outside the list is judged on its own.
- **Invented values:** how many systems, values, names, or behaviours appear in a requirement that the input did not give.

Compare the totals across all inputs, not single inputs: each input runs once, so one reply can vary. Treat a difference of fewer than three items in a total as no change.

## Changing the references

A reference list is a reviewer's opinion of what the input leaves open. Change it only for a reason that does not depend on what the skill replied, and score the baseline again when it changes.
