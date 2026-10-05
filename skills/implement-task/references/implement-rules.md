# Implement Rules

These rules are authoritative for `implement-task`. A change is checked against the [checklist](#validation-checklist) before it is committed.

## Reading tasks.md

`tasks.md` has phases (`### Phase <n>: <title>`) and tasks (`#### T-<phase>.<n>: <title>`). Each task has Covers, Files, Depends on, Done when, and Status (`Todo` or `Done`). The file's own `**Status:** Draft` line under the title is not a task's Status. Section 3 lists blocked requirements; they have no task and are never implemented.

## Picking the task

- **Named:** the task ID the user gave. If it is not in the file, stop. If it is `Done`, stop.
- **Not named:** the first `Todo` task in file order whose Depends on are all `Done`. If every task is `Done`, stop. If tasks are `Todo` but none has its dependencies `Done`, stop with the dependency line for the first `Todo` task.
- **Rework:** a `Todo` task that already has a commit (`git log --grep "^T-<p>.<n>:"` finds one) was reopened after a check found a gap. Implement it like any task, with these changes: take the failing requirement rows from the user's request (the verify-spec rows for the task's Covers) as extra context; fix only what they and the task's Done when show to be wrong, inside the task's Files; add or fix the test so it fails without the fix. Its commit subject ends with ` (rework)`. When the request has no rows and the Done when check already passes, stop with the no-gap line.
- A task whose Depends on lists a task that is not `Done`: stop. Never implement a dependency on the way.
- A requirement the user asks for that is blocked, or that no task covers: stop. Never implement work outside a task.
- A file with no Status lines was written before Status existed: stop with the no-Status line. Do not guess which tasks are done.

## Scope

1. **Only the task's Files.** Change only the files the task lists. A `new: <what it is>` file gets a path that follows the codebase's conventions for that kind of file (where the neighbouring modules and their tests live). `Files: None.` (a verify task) means no code changes.
2. **Only the task's behaviour.** Build what Covers and Done when say, within the phase's scope and interface changes in `plan.md`. No refactors, renames, formatting, or fixes outside the task, even ones that look right. No new dependency unless the plan names it.
3. **Never** change `requirements.md` or `plan.md`, another task, or a blocked requirement's code; never answer an open question.
4. **Doesn't fit:** a file the task names as existing is missing, or the task needs a file it does not list: stop with the task-mismatch line. Do not add the file anyway.
5. **A choice:** when the task, plan, requirements, and code leave a choice that changes behaviour (a value, a message, an error code), ask; do not pick.

## Tests

- Add the test Done when names, in the task's test file, before or with the code. The test must fail without the change.
- Run the project's existing test command (from its README, Makefile, package scripts, or CI config; else the language's standard runner). Use the same command in the done report's Check line.
- The full suite must be green, not only the new test.
- Never skip, delete, or weaken a test, and never change an assertion to match the code.
- **Verify task:** runs the phase's Verify list from `plan.md` and the full suite. It changes no code. Any failure is the failed-check stop line.
- A failure you cannot fix within the task's Files is the failed-check stop line. Leave the change uncommitted for the user to see and leave Status `Todo`.

## Git

- **Clean start.** Before changing anything, run `git status --porcelain`. Changes inside the feature's folder (the one holding `tasks.md`) are its spec files, saved by write-spec, write-plan, and write-tasks and not yet committed: they are allowed and are committed first (see Spec commit). A change to any other path: stop with the uncommitted-changes line, naming only those paths. With a pasted task list there is no feature folder, so any change stops.
- **Stops change nothing.** Every stop line that comes from picking the task (no such task, already done, dependency, blocked, no Status) is given before the branch switch and the spec commit.
- **Branch.** One branch per phase, named `<feature>/phase-<n>`, with `<feature>` the name of the `tasks.md` folder and `<n>` the task's phase. After the task is picked, when the current branch is the repository's default branch (`main`, `master`, or the branch `origin/HEAD` names) or any `<feature>/phase-*` branch, switch to the task's phase branch. If it does not exist, create it: from the default branch for the feature's first phase, otherwise from the previous phase's branch when that branch exists and is not merged into the default branch, else from the default branch. On any other branch, stay on it.
- **Spec commit.** If the feature's folder had uncommitted changes, stage that folder by path and commit it before implementing, once, with the subject `Add <feature-name> spec` and no body, on the branch the previous rule chose (the first phase's). Later runs find a clean tree and make no spec commit.
- **Stage by path.** Stage only the files you changed and `tasks.md`. Never `git add -A`, `git add .`, or `git commit -a`.
- **One commit per task**, after any spec commit, made only after every check passes and Status is `Done`. Subject `T-<p>.<n>: <task title>` (` (rework)` appended for a rework); body `Covers: <IDs>` and `Tasks: <path to tasks.md>`. Keep any commit trailer the environment requires.
- **Never** push, pull, merge, amend, rebase, reset, stash, or change another branch.
- **Not a git repository:** implement, set Status, and end the done report with `Commit: none (not a git repository)`.

## Stop lines

Reply with exactly one line, and nothing else: no text before it, and no backticks around it (they only mark the line here):

Wrong, because a sentence comes first:

```
`textstats/counts.py` is outside the spec folder, so the rules say stop.

Uncommitted changes in textstats/counts.py. Commit or stash them, then run implement-task again.
```

Right, the line alone as your last message, with no backticks:

```
Uncommitted changes in textstats/counts.py. Commit or stash them, then run implement-task again.
```

- No tasks file: `No tasks file found at <path>. Run write-tasks first, then run implement-task again.`
- No such task: `No task <id> in <path>.`
- Already done: `<id> is already Done.`
- Nothing left: `Every task in <path> is Done.`
- Dependency not done: `<id> depends on <ids>, not yet Done. Implement those first.`
- Blocked or untasked work: `<ID> has no task in <path>. Add it with write-tasks, then run implement-task again.`
- No Status lines: `<path> has no task Status lines. Re-run write-tasks to add them, then run implement-task again.`
- Uncommitted changes: `Uncommitted changes in <files outside the feature's folder>. Commit or stash them, then run implement-task again.`
- Task mismatch: `<id> <what does not fit>. Fix the task with write-tasks, then run implement-task again.`
- Rework with nothing to fix: `<id> is a rework but its check passes and no gap was given. Pass the failing verify rows, then run implement-task again.`
- Failed check: `<id> check failed: <command>: <one-line failure>. Status stays Todo; the changes are left uncommitted.`

## Validation checklist

Run every item before setting Status and committing.

1. Every changed file is in the task's Files (or is the path chosen for one of its `new:` files), plus `tasks.md`.
2. The test Done when names exists and passed; the full suite passed.
3. No test was skipped, deleted, or weakened.
4. `requirements.md`, `plan.md`, and every other task are unchanged; only this task's Status line changed in `tasks.md`.
5. No blocked requirement or open question was implemented or answered.
6. The commit holds only this task's changes, on the task's phase branch, and nothing was pushed. The only other commit this run made is the spec commit of the feature's folder.
