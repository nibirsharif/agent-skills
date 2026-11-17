# verify-spec benchmark

The eval cases in [../cases/](../cases/) check that a report follows the skill's rules on one fixture the rules were written against. This benchmark measures something else: whether the verdicts are right on projects the skill has not seen, where the faults are hidden behind tests that pass.

Each folder holds an `input.md`, a `reference.md`, and a `project/`: a small Python project with a `requirements.md` under `docs/specs/`. The agent runs in a copy of the project and never sees the reference. Some inputs also have a `branch/` folder, committed over the project on the branch `feature-work`, or a `dirty/` folder, left uncommitted; these give the drift line something to find.

## The planted faults

Every project mixes requirements that are met with ones that are not, and the reference says which:

- **Unmet, test passes:** no implementation, and a test named after the requirement that passes without checking it. Right verdict: `unmet`.
- **Met, no test:** the code is right and no test drives it, or its only test is skipped or asserts nothing about it. Right verdict: `untested`.
- **Partial:** a value or a part of the response is wrong, and the test passes because it avoids that part. Right verdict: `partial`.
- **Drift:** a changed file that no requirement covers, beside changed files that one does.

Around these are rows that test the other direction: a requirement that is really met, an NFR whose benchmark test exists and passes, a blocked requirement that has code and a passing test, and projects with nothing to compare for drift.

## The two sets

- `dev-*`: read these replies when changing a rule.
- `hold-*`: never tune a rule on these. Run them only to check that a change which helped the dev set helps here too.

## Running

```bash
python3 evals/bench.py verify-spec --model claude-sonnet-5-5 --label <name>
```

This runs each input once and saves the replies in `../runs/bench-<name>/`, with the model ID and Claude Code version in each reply's `.json`. It costs tokens, about $0.10 an input. Nothing is graded automatically.

## Scoring

Score each reply by hand against its `reference.md`:

- **Verdicts right:** how many rows have the reference's verdict. A missing row is wrong.
- **Gaps missed:** how many rows the reference gives as `partial`, `unmet`, or `untested` that the reply calls `met`. This is the number that matters most: build-phase stops reworking a requirement once verify-spec calls it `met`.
- **False alarms:** how many rows the reference gives as `met` that the reply calls anything else, plus each file the reply lists as drift that the reference does not.
- **Drift right:** whether the drift line names exactly the reference's files, or says `not checked (no feature branch)` where the reference does.

A fault the reply sees but names differently (`partial` where the reference says `unmet`) is a wrong verdict and not a missed gap. Note each one under the table: it shows which rule was misread.

Compare the totals across all inputs, not single inputs: each input runs once, so one reply can vary. Treat a difference of fewer than two rows in a total as no change.

## Changing the references

A reference is the verdict the [rules](../../../skills/verify-spec/references/verify-rules.md) give for code that was planted on purpose. Change one only when the rules change or the planted code did not do what the reference says, never because of what the skill replied, and score the baseline again when it changes.
