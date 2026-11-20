# Without commands

Read this only when you cannot run commands. You then do by hand what the three scripts do. Every other rule in [build-rules.md](build-rules.md) holds unchanged.

## In place of find_tasks.py

- **`tasks.md`:** a path the user names in this request, else `<spec_output_dir>/<feature-name>/tasks.md` and no other, with `spec_output_dir` from `.agent-skills-config.yaml` in the project root, else from `~/.agent-skills-config.yaml`. With no feature named and one `tasks.md` under `spec_output_dir`, use it; with several, ask which. With no `spec_output_dir`, as [build-rules.md](build-rules.md#finding-the-files-and-the-phase) says.
- **Stops before a phase is picked:**
  - The file does not exist: `Stopped: No tasks file found at <path>. Run write-tasks first, then run build-phase again.`
  - No `requirements.md` beside it: `Stopped: No requirements file found at <path>. Run write-spec first, then run build-phase again.`
  - No phase is named and no task is `Todo`: `Stopped: Every task in <path> is Done.`

  The summary's other lines are then `Phase ? of <feature>: stopped`, `Branch:` the branch from the start, `Tasks: 0 implemented, 0 reworked`, and `Verify: not run`.
- **Round limit:** `build_max_rework_rounds` from the same config files, 2 when it is not set.

## In place of parse_reply.py

Read each reply by the same shapes and act on the kind as the rules say.

- **implement-task:** `done` is five lines, the first `T-<p>.<n> done: <title>`, then a `Covers:`, a `Changed:`, a `Check:`, and a `Commit:` line, none empty. `stop` is one of `implement-task`'s stop lines; pass it on with `then run implement-task again.` made `then run build-phase again.` Anything else is `invalid`.
- **verify-spec:** `stop` is one of `verify-spec`'s stop lines. A `report` is the table, then one `Tests:`, one `Tally:`, and one `Drift:` line. It needs one row for every ID of `requirements.md`, in file order: the phase's rows and a `skipped` row for each other ID. It is `invalid` when it leaves out an ID, repeats one, or names one the file does not have, or when a `met` row has no path:line and passed test. Count the tally from the rows yourself, in the order `met`, `partial`, `unmet`, `untested`, `cannot tell`, `skipped`, leaving out a verdict with no rows.

## In place of summary.py

Write the lines of the reply contract yourself, with the values [build-rules.md](build-rules.md#the-summary) gives, and nothing else.
