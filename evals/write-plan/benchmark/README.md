# write-plan benchmark

The eval cases in [../cases/](../cases/) check that a plan follows the skill's rules. This benchmark measures something else: whether the phase cuts are sensible for requirements the rules were not written against.

Each folder holds an `input.md`, a requirements file pasted into the prompt, and a `reference.md`, which the agent never sees. There is no codebase, so a plan is judged on its cuts, not on what it reuses. The reference lists:

- the written IDs, and any withdrawn lines that must not be planned;
- a range for the number of phases;
- `D` items, "before": a requirement that must be in the same phase as another one, or an earlier phase, because the second builds on the first;
- `T` items, "together": requirements that belong in one phase, such as an `NFR` and the `FR` it limits;
- the blocked entries the plan must list, and what it must not plan;
- one sensible cut, as an example. Other cuts that hold every item are as good.

The files list their requirements out of build order on purpose, so a plan that follows the order of the IDs breaks `D` items.

## The two sets

- `dev-*`: read these replies when changing a rule.
- `hold-*`: never tune a rule on these. Run them only to check that a change which helped the dev set helps here too.

Both sets have a feature that fits one phase, a feature that needs several, blocked requirements, and withdrawn or closed lines. `hold-message-search` has an open question that decides the architecture, so its right reply is the question and no plan.

## Running

```bash
python3 evals/bench.py write-plan --model claude-sonnet-5-5 --label <name>
```

This runs each input once and saves the replies in `../runs/bench-<name>/`, with the model ID and Claude Code version in each reply's `.json`. It costs tokens, about $0.12 an input. Nothing is graded automatically.

## Scoring

Score each reply by hand against its `reference.md`:

- **Coverage:** how many written IDs are in exactly one phase's `**Requirements:**` list. An ID in two phases, in none, or named only in a scope is not covered.
- **Phases:** the number of phases, and whether it is in the reference's range.
- **Before:** how many `D` items hold.
- **Together:** how many `T` items hold.
- **Blocked right:** whether section 3 has exactly the reference's entries, no blocked or withdrawn requirement is planned, and no question is answered.

Also note anything the plan invents: a file, a requirement, a value, or an answer to a question.

Compare the totals across all inputs, not single inputs: each input runs once, so one reply can vary. Treat a difference of fewer than two items in a total as no change.

## Changing the references

A reference is a reviewer's opinion of which cuts make sense. Change it only for a reason that does not depend on what the skill replied, and score the baseline again when it changes.
