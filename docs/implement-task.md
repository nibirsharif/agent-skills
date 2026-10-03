# implement-task

Instructions the agent follows: [skills/implement-task/SKILL.md](../skills/implement-task/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Implements one task from a saved `tasks.md`: the task you name (`T-1.2`), or the next `Todo` task whose dependencies are `Done`. It reads the task's phase in `plan.md`, the requirements the task covers, and the code; changes only the files the task lists; adds the test its Done when names; and runs the full test suite. When everything passes, it sets the task's Status to `Done` and commits the change on the feature branch, one commit per task. It never pushes.

Run it again for the next task. When every task is `Done`, the feature branch holds one commit per task, ready for review.

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
Commit: 3f9c2e1 on password-reset
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

The full list is in [the rules](../skills/implement-task/references/implement-rules.md#stop-lines).

## FAQ

**Which branch does it commit to?** On `main` (or your default branch) it creates or switches to a branch named after the feature folder, for example `password-reset`. On any other branch it stays where it is.

**Why does it refuse a dirty working tree?** So each commit holds only its own task. Commit or stash your changes first.

**What about the spec files that write-spec, write-plan, and write-tasks just saved?** They are the one exception. On its first run the skill commits the feature's folder as `Add <feature-name> spec` on the feature branch, then commits the task. It does this without asking, so review those files first if you want to change them; the commit is local and you can amend or drop it before merging.

**Can it do several tasks in one run?** No. One task per run keeps each commit small and each check meaningful. Run it again for the next one.

**What if the task is not in a git repository?** It implements the task and sets Status, and the report says `Commit: none (not a git repository)`.

**Does it push?** Never. Pushing and merging stay with you.

## Verifying results

- `git show` on the commit holds only the task's files and the Status change in `tasks.md`.
- The new test fails without the change.
- No test was skipped or weakened, and `requirements.md` and `plan.md` are unchanged.

## Related skills

Final step of the chain: [write-spec](write-spec.md) → [write-plan](write-plan.md) → [write-tasks](write-tasks.md) → **implement-task**. It reads all three files from `spec_output_dir`. When tasks are done, [verify-spec](verify-spec.md) checks the result against the requirements.
