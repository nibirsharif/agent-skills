# Without pick_task.py

Read this only when you cannot run [pick_task.py](../scripts/pick_task.py): you cannot run commands, or the user pasted the task list, so there is no file for it to read. You then do by hand what the script does, in the order below. Every stop here is given before any branch switch or spec commit. Every other rule in [implement-rules.md](implement-rules.md) holds unchanged.

## Find tasks.md

A pasted task list skips this step.

1. A path the user names in this request. If no file is there, reply with the no-tasks-file stop line for that path.
2. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root.
   - **The user names a feature:** the file is `<spec_output_dir>/<feature-name>/tasks.md` and no other. Check that one path and do not look for other `tasks.md` files. If it does not exist, reply with the no-tasks-file stop line for that path.
   - **The user names no feature:** list the existing `<spec_output_dir>/*/tasks.md` files; if only one exists, use it, otherwise ask which one.
3. None of these: a path from earlier in this conversation, as [SKILL.md](../SKILL.md#finding-the-files) says, else ask for the path.

## Check the working tree

Before changing anything, look at `git status --porcelain`. Changes inside the feature's folder and `.agent-skills-config.yaml` in the project root are allowed, as the rules' git section says. A change to any other path: stop with the uncommitted-changes line, naming only those paths. With a pasted task list there is no feature folder, so any change stops.

## Pick the task

- A file with no Status lines was written before Status existed: stop with the no-Status line. Do not guess which tasks are done.
- **Named:** the task ID the user gave. If it is not in the file, stop. If it is `Done`, stop. If its Depends on lists a task that is not `Done`, stop with the dependency line.
- **A requirement in place of a task:** the first task not yet `Done` that builds it (the verify task does not), else the first that builds it, then as for a named task. If it is blocked, or no task covers it, stop with the blocked-or-untasked line.
- **Not named:** the first `Todo` task in file order whose Depends on are all `Done`. If every task is `Done`, stop. If tasks are `Todo` but none has its dependencies `Done`, stop with the dependency line for the first `Todo` task.
- **Rework:** the picked task is a rework when it already has a commit (`git log --grep "^T-<p>.<n>:"` finds one).

## The stop lines the script prints

Reply with the line alone, as [the rules](implement-rules.md#stop-lines) say of every stop line.

- No tasks file: `No tasks file found at <path>. Run write-tasks first, then run implement-task again.`
- Uncommitted changes: `Uncommitted changes in <files outside the feature's folder>. Commit or stash them, then run implement-task again.`
- No Status lines: `<path> has no task Status lines. Re-run write-tasks to add them, then run implement-task again.`
- No such task: `No task <id> in <path>.`
- Already done: `<id> is already Done.`
- Dependency not done: `<id> depends on <ids>, not yet Done. Implement those first.`
- Blocked or untasked work: `<ID> has no task in <path>. Add it with write-tasks, then run implement-task again.`
- Nothing left: `Every task in <path> is Done.`
