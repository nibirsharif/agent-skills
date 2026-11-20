# Implement Rules

These rules are authoritative for `implement-task`.

The settings named here (`test_command`, `base_branch`, `branch_prefix`) come from `.agent-skills-config.yaml` in the project root, else from `~/.agent-skills-config.yaml`.

## Reading tasks.md

`tasks.md` has phases (`### Phase <n>: <title>`) and tasks (`#### T-<phase>.<n>: <title>`). Each task has Covers, Files, Depends on, Done when, and Status (`Todo` or `Done`). Section 3 lists blocked requirements; they have no task and are never implemented.

## Picking the task

[pick_task.py](../scripts/pick_task.py) picks the task: the one the user named, else the first `Todo` task in file order whose Depends on are all `Done`. Its stop is final: never implement a dependency on the way, a blocked requirement, or work no task covers.

**Rework:** `task <T-id> rework` means the task already has a commit and was reopened after a check found a gap. Implement it like any task, with these changes: the failing requirement rows in the user's request (the verify-spec rows for the task's Covers) are extra context; fix only what they and the task's Done when show to be wrong, inside the task's Files; add or fix the test so it fails without the fix. Its commit subject ends with ` (rework)`. When the request has no rows and the Done when check already passes, stop with the no-gap line.

## Scope

1. **Only the task's Files.** Change only the files the task lists. A `new: <what it is>` file gets a path that follows the codebase's conventions for that kind of file (where the neighbouring modules and their tests live). `Files: None.` (a verify task) means no code changes.
2. **Only the task's behaviour.** Build what Covers and Done when say, within the phase's scope and interface changes in `plan.md`. No refactors, renames, formatting, or fixes outside the task, even ones that look right. No new dependency unless the plan names it.
3. **Doesn't fit:** a file the task names as existing is missing, or the task needs a file it does not list: stop with the task-mismatch line. Do not add the file anyway.
4. **A choice:** when the task, plan, requirements, and code leave a choice that changes behaviour (a value, a message, an error code), ask; do not pick.

## Tests

- Add the test Done when names, in the task's test file, before or with the code. The test must fail without the change: see it fail by running it before you edit the code (or by reasoning from the old code when the test is added with it), never by stashing or reverting your files.
- Run `test_command` when set, else the project's existing test command (from its README, Makefile, package scripts, or CI config; else the language's standard runner). Use the same command in the done report's Check line.
- The full suite must be green, not only the new test. Never skip, delete, or weaken a test, and never change an assertion to match the code.
- A failure you cannot fix within the task's Files is the failed-check stop line. Leave the change uncommitted and Status `Todo`.
- **Manual check:** a Done when check that starts with `manual:` after its ID (`FR-007: manual: ...`) is made by a person, later. Build the behaviour it describes, add no test for it, and never make the check yourself or report it as made. The task's other checks and the full suite still run. A check without the word is never treated as manual.
- **Verify task:** runs the phase's Verify list from `plan.md` and the full suite, leaving out each ID whose check in its Done when starts with `manual:`. It changes no code. Any failure is the failed-check stop line, except a missing service.
- **Missing service.** Before you edit any file, run the test command once as the tree stands. When the tests cannot run because something outside the project is not there (a server they connect to refuses the connection or cannot be found; a tool or credential the command needs is missing), that is not a failed check: the code was never tested. Stop with the missing-service line, naming what is missing and the error that shows it. The user makes it available, never you: never start, stop, install, or configure a service, container, or tool (no `docker run`, `systemctl`, package install, or stand-in server of your own), never point the tests at another one, and never skip the tests that need it. This stop keeps the phase branch and any spec commit. When the service goes away only after you changed files, give the same line and leave the changes uncommitted and Status `Todo`.

## Git

- **Uncommitted changes.** `pick_task.py` stops on any but two: changes inside the feature's folder (the one holding `tasks.md`), which are spec files not yet committed (see Spec commit), and `.agent-skills-config.yaml` in the project root, the user's settings, which you never stage.
- **Branch.** One branch per phase, named `<branch_prefix><feature>/phase-<n>`: `<feature>` is the name of the `tasks.md` folder, `<n>` the task's phase, and the prefix is empty when not set.
  - The default branch is `base_branch` when set, else the branch `origin/HEAD` names, which `git symbolic-ref --short refs/remotes/origin/HEAD` prints as `origin/<name>`, else `main`, else `master`. A local `main` or `master` that is not the default branch is only another branch: never cut a phase branch from it, and never delete it.
  - After the task is picked, when the current branch is the default branch or any `<branch_prefix><feature>/phase-*` branch, switch to the task's phase branch. On any other branch, stay on it.
  - If the phase branch does not exist, create it from the previous phase's branch when that branch exists and is not merged into the default branch, else from the default branch.
- **Spec commit.** If the feature's folder had uncommitted changes, stage that folder by path and commit it before implementing, once, with the subject `Add <feature-name> spec` and no body, on the branch the Branch rule chose.
- **Stage by path.** Stage only the files you changed and `tasks.md`. Never `git add -A`, `git add .`, or `git commit -a`.
- **One commit per task**, after any spec commit, made only after every check passes and Status is `Done`. Subject `T-<p>.<n>: <task title>` (` (rework)` appended for a rework); body `Covers: <IDs>` and `Tasks: <path to tasks.md>`. Keep any commit trailer the environment requires.
- **Leave no new files behind.** After the task's commit, run `git status --porcelain`. Each untracked path (`??`) is one this run's commands created, such as a lock file or cache the test command wrote, and the next task would stop on it: remove each by path with `git clean -fd -- <path>`, except `.agent-skills-config.yaml` and the task's own Files. Never run `git clean` without a path, and never remove a tracked file. A stop line removes nothing, except the missing-service line, which removes the files the test command created the same way.
- **Never** push, pull, merge, amend, rebase, reset, stash, or change another branch.
- **Not a git repository:** implement, set Status, and end the done report with `Commit: none (not a git repository)`.

## Stop lines

Reply with exactly one line, and nothing else: no text before it, and no backticks around it (they only mark the line here).

Wrong, because a sentence comes first:

```
The change also needs `reset/mailer.py`, which T-1.2 does not list, so the rules say stop.

T-1.2 needs reset/mailer.py, which its Files do not list. Fix the task with write-tasks, then run implement-task again.
```

Right: the second of those lines alone, as your last message.

`pick_task.py` prints the stop lines it decides, whole: copy the line after `stop`. These four are yours to write:

- Task mismatch: `<id> <what does not fit>. Fix the task with write-tasks, then run implement-task again.`
- Rework with nothing to fix: `<id> is a rework but its check passes and no gap was given. Pass the failing verify rows, then run implement-task again.`
- Failed check: `<id> check failed: <command>: <one-line failure>. Status stays Todo; the changes are left uncommitted.`
- Missing service: `<id> cannot run its tests: <what is missing> is not available (<command>: <one-line error>). Make it available, then run implement-task again.`

## Validation checklist

Run every item before setting Status and committing.

1. Every changed file is in the task's Files (or is the path chosen for one of its `new:` files), plus `tasks.md`.
2. The test Done when names exists and passed (a `manual:` check names none and was not made); the full suite passed, with no test skipped, deleted, or weakened.
3. `requirements.md`, `plan.md`, and every other task are unchanged; only this task's Status line changed in `tasks.md`. No blocked requirement was implemented and no open question answered.
4. The commit holds only this task's changes, on the task's phase branch, and nothing was pushed. The only other commit this run made is the spec commit of the feature's folder.
5. Nothing was started, stopped, installed, or configured to make the tests run.
