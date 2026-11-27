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

## The harder inputs

In the six inputs above (`dev-cart`, `dev-rate-limiter`, `dev-todo`, `hold-csv-export`, `hold-greenhouse`, `hold-password-policy`) each fault is in one function and one test file of a project with fewer than 100 lines, and every reply finds them. Four inputs have faults that reading one function does not show ([#23](https://github.com/nibirsharif/agent-skills/issues/23)). `dev-bookings` and `hold-mailing` have about 10 modules, `dev-helpdesk` and `hold-depot` about 30.

- **Two modules:** each module is right by itself and its own tests pass; the fault is in how one calls the other, such as minutes passed to a function that takes hours. Right verdict: `partial`.
- **Behind a mock:** a test passes because the part with the fault is a mock. Right verdict: `partial`, or `untested` when the code is right and the mock replaces the very code the requirement is about.
- **A mock at the boundary:** the test checks a call on a mock gateway, mailer, or transport, and the code under test runs. Right verdict: `met`. Anything else is a false alarm.
- **A benchmark of another size:** an NFR's test measures 100 records where the statement says 10,000. Right verdict: `untested`.
- **An implementation the words do not find** (the two large projects): the behaviour is in a rule or hook whose names share no word with the requirement, and a file with the obvious name holds something else. Right verdict: `met`.
- **A second way in** (the two large projects): the rule holds on the path the test drives, and another request reaches the same code without it. Right verdict: `partial`.
- **A rule kept outside the named system:** the requirement says the store shall reject something, and the check is in the one service that writes to the store. This is the row whose verdict changed on a retry in the [first real run](../../real-runs/2026-11-17.md). Right verdict: `partial`.

## Open rows

A reference names two verdicts where the [rules](../../../skills/verify-spec/references/verify-rules.md) do not decide between them. One kind of row is open now:

- **Code the trigger cannot reach** (`partial` or `unmet`): the handler exists and its test calls it directly, and no command or route leads to it.

Either verdict is right on an open row. What the row measures is agreement: whether every run of the same input gives it the same verdict. When a rule is added that decides such a row, its reference becomes one verdict, as happened to the rows for a rule kept outside the named system ([after-verdict-rules.md](after-verdict-rules.md)).

## The two sets

- `dev-*`: read these replies when changing a rule.
- `hold-*`: never tune a rule on these. Run them only to check that a change which helped the dev set helps here too.

## Running

```bash
python3 evals/bench.py verify-spec --model claude-sonnet-5-5 --label <name>
```

This runs each input once and saves the replies in `../runs/bench-<name>/`, with the model ID and Claude Code version in each reply's `.json`. It costs tokens: about $0.14 a run on the six older inputs and $0.19 to $0.26 on the harder four, so three runs of all ten are about $5. Each reply's transcript is saved beside it as `.jsonl`. Add `--runs 3` to run each input three times, which a baseline needs: a verdict that is right once can differ on the next run.

## Scoring

```bash
python3 evals/verify-spec/benchmark/score.py <name>
```

This prints, for each input, every run's verdict beside the reference's, and these counts for each run and in total:

- **Verdicts right:** how many rows have the reference's verdict. A missing row is wrong.
- **Gaps missed:** how many rows the reference gives as `partial`, `unmet`, or `untested` that the reply calls `met`. This is the number that matters most: build-phase stops reworking a requirement once verify-spec calls it `met`.
- **False alarms:** how many rows the reference gives as `met` that the reply calls anything else, plus each file the reply lists as drift that the reference does not.
- **Drift right:** whether the drift line names exactly the reference's files, or says `not checked (no feature branch)` where the reference does.
- **Agreement:** with more than one run, how many rows have the same verdict in every run. A row can agree and be wrong, and a row that is right twice and wrong once does not agree.

The script only counts. Read by hand each row it marks wrong or `runs differ`: whether the evidence names the planted cause, and which rule the reply misread. A fault the reply sees but names differently (`partial` where the reference says `unmet`) is a wrong verdict and not a missed gap. Note each one under the table.

Compare the totals across all inputs, not single inputs. With one run an input, one reply can vary: treat a difference of fewer than two rows in a total as no change.

## Changing the references

A reference is the verdict the [rules](../../../skills/verify-spec/references/verify-rules.md) give for code that was planted on purpose. Change one only when the rules change or the planted code did not do what the reference says, never because of what the skill replied, and score the baseline again when it changes.
