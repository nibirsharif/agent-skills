# implement-task

Instructions the agent follows: [skills/implement-task/SKILL.md](../skills/implement-task/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Implements one task from a saved `tasks.md`: the task you name (`T-1.2`), or the next `Todo` task whose dependencies are `Done`. It reads the task's phase in `plan.md`, the requirements the task covers, and the code; changes only the files the task lists; adds the test its Done when names; and runs the full test suite. A check marked `manual:` is for a person: the skill builds the behaviour, adds no test for it, and does not make the check ([rule](../skills/implement-task/references/implement-rules.md#tests)). When everything passes, it sets the task's Status to `Done` and commits the change on the feature branch, one commit per task. It never pushes.

Run it again for the next task. When every task is `Done`, each phase branch holds one commit per task, ready for review as one PR.

## When to use it

- You have a `tasks.md` from [write-tasks](write-tasks.md) and want the next step built and proven.
- You want each task as its own small commit, citing the requirement IDs it covers.

It does not write requirements, the plan, or the task list, and it does not take work that has no task.

## Output

When the task is done, five lines:

```
T-1.2 done: Reject an expired reset link
Covers: FR-002
Changed: reset/tokens.py, tests/test_tokens.py, docs/specs/password-reset/tasks.md
Check: python3 -m unittest: 14 tests OK
Commit: 3f9c2e1 on password-reset/phase-1
```

It stops with a single line instead when:

| Situation | Where to go |
|-----------|-------------|
| No `tasks.md` for the feature | write-tasks |
| The task depends on tasks that are not `Done` | implement those first |
| The work is blocked or has no task | write-tasks |
| The task's files do not fit the code | fix the task with write-tasks |
| Files outside the feature's folder have uncommitted changes | commit or stash them |
| The check fails | the change is left uncommitted for you to see; Status stays `Todo`. Commit or discard it before the next run |
| A service the tests need, such as a database, is not running | start it; nothing was changed, so rerun as is |

The full list is in [the rules](../skills/implement-task/references/implement-rules.md#stop-lines).

## FAQ

**Which branch does it commit to?** One branch per phase, named `<feature>/phase-<n>`, for example `password-reset/phase-1` (set `branch_prefix` in `.agent-skills-config.yaml` to put a prefix such as `team/` in front). From your default branch (the one `origin/HEAD` names, else `main`, else `master`; set `base_branch` to use another), or from another phase branch of the feature, it switches to the task's phase branch, creating it when needed: phase 1 from the default branch, later phases from the previous phase's branch while that is unmerged (so they stack), else from the default branch. Each phase branch is one reviewable PR. On any other branch it stays where it is.

**What if the feature I name has no task list?** It replies with one line, `No tasks file found at <path>. Run write-tasks first, then run implement-task again.`, and changes nothing. It never falls back to another feature's `tasks.md`, even when that is the only one in the project: a script does the lookup at the one path your feature name gives.

**Why does it refuse a dirty working tree?** So each commit holds only its own task. Commit or stash your changes first.

**My test command creates a file, such as `uv.lock`. Will it stop the next task?** No. The skill starts from a clean tree, so after its commit any new untracked file came from its own commands, and it removes each one by path. It leaves your `.agent-skills-config.yaml` and anything `.gitignore` covers alone. To keep such a file, commit it or add it to `.gitignore`.

**My tests need a database (or another service). Will the skill start one?** No. It never starts, stops, or installs a service, container, or tool. Before it edits anything it runs the tests once; when they cannot reach something they need, it stops with `T-1.2 cannot run its tests: <what> is not available (...). Make it available, then run implement-task again.` That is not a failed check, since the code was never tested, and nothing was edited, so after you start the service the next run picks up from the same tree.

**What about the spec files that write-spec, write-plan, and write-tasks just saved?** They are the one exception. On its first run the skill commits the feature's folder as `Add <feature-name> spec` on the first phase's branch, then commits the task. It does this without asking, so review those files first if you want to change them; the commit is local and you can amend or drop it before merging.

**What if [verify-spec](verify-spec.md) finds a gap in a `Done` task?** Set that task's Status back to `Todo`, commit it, and run implement-task on it with the verify rows in your message. It treats a `Todo` task that already has a commit as a rework: it fixes only what the rows show, inside the task's Files, and commits `T-1.2: <title> (rework)`. [build-phase](build-phase.md) does this loop for you.

**Can it do several tasks in one run?** No. One task per run keeps each commit small and each check meaningful. Run it again for the next one.

**What if the task is not in a git repository?** It implements the task and sets Status, and the report says `Commit: none (not a git repository)`.

**Does it push?** Never. Pushing and merging stay with you.

## Verifying results

- `git show` on the commit holds only the task's files and the Status change in `tasks.md`.
- The new test fails without the change.
- No test was skipped or weakened, and `requirements.md` and `plan.md` are unchanged.

## Related skills

Final step of the chain: [write-spec](write-spec.md) → [write-plan](write-plan.md) → [write-tasks](write-tasks.md) → **implement-task**. It reads all three files from `spec_output_dir`. When tasks are done, [verify-spec](verify-spec.md) checks the result against the requirements.
