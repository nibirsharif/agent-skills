# Build Rules

These rules are authoritative for `build-phase`. A run is checked against the [checklist](#validation-checklist) before the summary is written.

## Finding the files and the phase

- `tasks.md`: a path the user named, else `<spec_output_dir>/<feature-name>/tasks.md`, with `spec_output_dir` from `.agent-skills-config.yaml` in the project root, else from `~/.agent-skills-config.yaml`. With no feature named and one `tasks.md` under `spec_output_dir`, use it; with several, ask which. If the file does not exist, the summary is `stopped` with `Stopped: No tasks file found at <path>. Run write-tasks first, then run build-phase again.`
- `plan.md` and `requirements.md` are beside it. Without `requirements.md`, stop: `Stopped: No requirements file found at <path>. Run write-spec first, then run build-phase again.`
- **Phase:** the one the user named. Otherwise the first phase of `tasks.md`, in file order, that has a `Todo` task. If none has, stop with `Every task in <path> is Done.`; that is also the stop when a named phase has no `Todo` task and no gap to find.
- Settings from the same config files: `build_max_rework_rounds` (default 2).
- Run `git branch --show-current` once at the start. Do not change branch yourself: `implement-task` does.

## Running a task

Start one subagent per task, with the Agent tool and the general-purpose type, never in the background, and never two at once. Its prompt is exactly:

```
Call the Skill tool with implement-task. Implement task <T-id> of <path to tasks.md>. <rework only: This task was reopened. Gap rows from verify-spec: <the rows for its Covers>.> Reply as the skill says.
```

Name the task, so the subagent never picks one. Tasks run in file order within the phase; a task runs only when its dependencies are `Done` in `tasks.md` (re-read the file after each task).

Parse the reply with `python3 <this skill folder>/scripts/parse_reply.py implement`, or by the same shapes when you cannot run commands:

- **done** (five lines, the first `T-<p>.<n> done: <title>`): the task is finished. Keep its commit.
- **stop**: one of `implement-task`'s stop lines. End the run: `Stopped: <the line>`. Never work around a stop line.
- **anything else** (invalid, or questions): the reply is not usable. First re-read `tasks.md` and `git log -1 --format=%s`: when the task is `Done` and the last commit subject starts with `<T-id>:`, the work happened and only the reply was wrong, so count it as done. Otherwise start one new subagent with the same prompt. A second unusable reply ends the run: `Stopped: <T-id> gave no usable reply twice`.

## Verifying the phase

When every task of the phase is `Done`, start a separate subagent (a fresh one, never one that implemented a task) with the prompt:

```
Call the Skill tool with verify-spec. Verify phase <n> of <path to requirements.md>. Reply as the skill says.
```

Parse its reply with `parse_reply.py verify`, with the same retry rule once for an unusable reply (a verify run changes nothing, so a retry is always safe).

- **stop**: end the run with the line.
- **report**: gaps are the rows `unmet`, `partial`, and `untested`. `cannot tell` is not a gap (it needs `write-spec`) and `skipped` is not either; list them in the summary only through the tally. No gaps: the phase is done.

## Reopening and reworking

For each gap row, the tasks to reopen are the build tasks of this phase whose Covers include the row's ID, plus the phase's verify task. A gap whose ID no build task of the phase covers ends the run: `Stopped: <ID> is <verdict> but no task of phase <n> covers it. Add one with write-tasks, then run build-phase again.`

1. Past the round limit with gaps left: end the run, `Stopped: <IDs> still not met after <limit> rework rounds`.
2. Check that the current branch is `<feature>/phase-<n>`; otherwise stop with `Stopped: not on the phase branch`.
3. Set `**Status:** Todo` on each task to reopen, and nothing else in the file. Stage `tasks.md` by path and commit it with the subject `Reopen <T-ids>: <gap IDs> <verdicts>`. Nothing else is staged. Never amend, never push.
4. Run each reopened build task in file order as in [Running a task](#running-a-task), with the gap rows for its Covers in the prompt, then the verify task, then [Verifying the phase](#verifying-the-phase) again. That is one round.

## The summary

The phase title in the `Next:` line is the text after `### Phase <n>: ` in `tasks.md`, copied as written.

## Never

- Edit code, tests, requirements, the plan, or any task text; only the `Status` line of a task you reopen.
- Push, pull, merge, rebase, reset, stash, amend, or switch branches.
- Implement or verify in your own context: always a subagent, and always a different one for verify.
- Retry a stop line, or retry more than once.
- Answer an open question or mark a blocked requirement as a gap.

## Validation checklist

1. Every task you ran was named, and ran only with its dependencies `Done`.
2. Every subagent reply was parsed; no stop line was retried; no task had more than two attempts.
3. Verify ran only after every task of the phase was `Done`, in a subagent that implemented nothing.
4. The only commits you made are `Reopen` commits that change only Status lines of `tasks.md`.
5. Nothing was pushed, and the branch is the one `implement-task` chose.
6. The summary lines match what happened: counts of implemented and reworked tasks, the last report's tally, and a `Stopped:` line exactly when the run stopped.
