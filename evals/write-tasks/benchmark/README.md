# write-tasks benchmark

The eval cases in [../cases/](../cases/) check that a task list follows the skill's rules. This benchmark measures something else: whether the tasks are the right size, in the right order, and proved by checks that can be run, for plans the rules were not written against.

Each folder holds an `input.md` and a `reference.md`, which the agent never sees. There are two kinds of input:

- **A pasted plan, no codebase** (`dev-table-booking`, `hold-parking-permits`): the plan that write-plan 0.14.0 gave for its own [benchmark](../../write-plan/benchmark/README.md) input of the same name, in the file template. The plan is fixed, so a score does not depend on what write-plan would give today.
- **A project on disk** (`dev-note-tags`, `hold-backup-verify`): a `project/` folder with code, tests, and a `plan.md` under `docs/specs/`. The agent runs in a copy of it. These test what a pasted plan cannot: naming files that exist, and choosing `manual:` by what the project's own test runner can reach.

The reference lists the IDs of each phase, `O` items (a task that must come before another), `M` items (which checks are `manual:` and which are not), `F` items (files), and the blocked entries.

## The two sets

- `dev-*`: read these replies when changing a rule.
- `hold-*`: never tune a rule on these. Run them only to check that a change which helped the dev set helps here too.

The dev project has a check that only a person can make (a page with no test runner). The hold project has checks that look manual and are not (an email, a slow timing).

## Running

```bash
python3 evals/bench.py write-tasks --model claude-sonnet-5-5 --label <name>
```

This runs each input once and saves the replies in `../runs/bench-<name>/`, with the model ID and Claude Code version in each reply's `.json`. It costs tokens, about $0.15 an input. Nothing is graded automatically.

## Scoring

Score each reply by hand against its `reference.md`. A phase's verify task is left out of the task counts.

- **Coverage:** how many IDs are in the Covers of a task that builds them.
- **One behaviour:** how many tasks hold one behaviour, or one interface or data change. A task whose title joins two changes with "and", or that has more than 3 files, does not.
- **Order:** how many `O` items hold. A task that depends on a later task fails the item it touches.
- **Checks runnable:** how many Done when checks a reviewer can run as written: a named kind of test with its input and expected result, or a command. "Works", "reviewed", or a check with no expected result is not runnable.
- **Manual right:** how many `M` items hold.
- **Files right:** how many `F` items hold.

Also note whether the blocked entries are copied word for word, and anything invented: a path, a test tool, a requirement.

Compare the totals across all inputs, not single inputs: each input runs once, so one reply can vary. Treat a difference of fewer than two items in a total as no change.

## Changing the references

A reference is a reviewer's opinion of the order and the checks a plan needs. Change it, or a plan, only for a reason that does not depend on how good the skill's tasks were, and score the baseline again when it changes.
