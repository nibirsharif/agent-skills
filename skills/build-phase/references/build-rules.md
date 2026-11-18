# Build Rules

These rules are authoritative for `build-phase`. A run is checked against the [checklist](#validation-checklist) before the summary is written.

## Finding the files and the phase

- Run [find_tasks.py](../scripts/find_tasks.py) by its full path, with the project as the current directory, before any other search. Give it `--feature <name>` when the user names a feature, `--path <path>` when they name a path, and no argument when they name neither; add `--phase <n>` when they name a phase. Do what it prints:
  - `found <path>`: that is `tasks.md`, with `plan.md` and `requirements.md` beside it. Use it and no other.
  - `rounds <n>`, the line after `found`: the round limit, the most rework rounds this run may make. It is `build_max_rework_rounds` from the config, and `rounds 0` means no task is ever reopened.
  - `stop`, then the lines of a stopped summary: those lines are your whole reply. That includes `Every task in <path> is Done.` when no phase was named. Another feature's task list is not what the user asked for, even when it is the only one in the project.
  - `ask <what>`: ask the user that.
- Only when you cannot run commands, find the files yourself by the same rules. `tasks.md`: a path the user named, else `<spec_output_dir>/<feature-name>/tasks.md` and no other, with `spec_output_dir` from `.agent-skills-config.yaml` in the project root, else from `~/.agent-skills-config.yaml`. With no feature named and one `tasks.md` under `spec_output_dir`, use it; with several, ask which. If the file does not exist, the summary is `stopped` with `Stopped: No tasks file found at <path>. Run write-tasks first, then run build-phase again.` Without `requirements.md` beside it, stop: `Stopped: No requirements file found at <path>. Run write-spec first, then run build-phase again.`
- **Phase:** the one the user named. Otherwise the first phase of `tasks.md`, in file order, that has a `Todo` task. If none has, stop with `Every task in <path> is Done.`; that is also the stop when a named phase has no `Todo` task and no gap to find.
- Settings from the same config files: `build_max_rework_rounds` (default 2), which the script prints as `rounds <n>` and which you read from the files yourself only when you cannot run commands; and `test_command`, `base_branch`, `branch_prefix`, which the build and verify subagents read themselves.
- Run `git branch --show-current` once at the start. Do not change branch yourself: `implement-task` does.

## Running a task

**No subagents.** Before the first task, check that you have a tool that starts a subagent (the Agent tool, or Task under its older name). When you have none, or the first call is refused because the tool is not available, end the run: `Stopped: This agent cannot start subagents, which build-phase needs. Run implement-task for each task of phase <n>, then verify-spec, yourself.` Change nothing, and never do a task's work or the verify in your own context in its place.

Start one subagent per task, with the Agent tool and the general-purpose type, never in the background, and never two at once. Its prompt is exactly:

```
Call the Skill tool with implement-task. Implement task <T-id> of <path to tasks.md>. <rework only: This task was reopened. Gap rows from verify-spec: <the rows for its Covers>.> Reply as the skill says.
```

Name the task, so the subagent never picks one. Tasks run in file order within the phase; a task runs only when its dependencies are `Done` in `tasks.md` (re-read the file after each task).

**The verify task** is the phase's task with `**Files:** None.` (it runs the plan's Verify list and changes no code). It is not a build task: skip it here, and run it only after [Verifying the phase](#verifying-the-phase) reports no gaps, as the last step before the summary. Run before the gaps are fixed, its check fails by design.

**Parse every reply with the script**, the done ones too: it checks what reading cannot, such as a done report missing a line or a tally that does not match its rows. Pass the subagent's reply as it came back, without editing it, and do what the JSON's `kind` says, not what the reply looks like:

```
python3 <this skill folder>/scripts/parse_reply.py implement <<'REPLY'
<the subagent's reply>
REPLY
```

Only when you cannot run commands, parse by the same shapes yourself. The kinds:

- **done** (five lines, the first `T-<p>.<n> done: <title>`): the task is finished. Keep its commit.
- **stop**: one of `implement-task`'s stop lines. End the run: `Stopped: <the line>`. Never work around a stop line.
- **anything else** (invalid, or questions): the reply is not usable. First re-read `tasks.md` and `git log -1 --format=%s`: when the task is `Done` and the last commit subject starts with `<T-id>:`, the work happened and only the reply was wrong, so count it as done. Otherwise start one new subagent with the same prompt. A second unusable reply ends the run: `Stopped: <T-id> gave no usable reply twice`.

## Verifying the phase

When every task of the phase is `Done`, start a separate subagent (a fresh one, never one that implemented a task) with the prompt:

```
Call the Skill tool with verify-spec. Verify phase <n> of <path to requirements.md>. Reply as the skill says.
```

Parse its reply with `parse_reply.py verify` in the same way. When the script says `invalid` (no report, or a report whose own lines disagree, such as a Tally that does not match its rows), start one new verify subagent with the same prompt; a verify run changes nothing, so a retry is always safe. A second `invalid` ends the run: `Verify: no usable report` and `Stopped: verify-spec gave no usable reply twice`. Never fix a report yourself, and never copy a Tally the script rejected.

- **stop**: end the run with the line.
- **report**: the `Verify:` line is the script's `tally`. Gaps are the rows `unmet` and `partial`, and each `untested` row that is not a [manual check](#manual-checks). `cannot tell` is not a gap (it needs `write-spec`) and `skipped` is not either; list them in the summary only through the tally. No gaps: run the verify task as [Running a task](#running-a-task) says; the phase is done when it replies done.

## Manual checks

A task's Done when holds one check per ID, `<ID>: <check>`. A check that starts with the word `manual:` (`FR-007: manual: ...`) is made by a person: no test can turn its row into `met`, so reworking it cannot succeed.

An `untested` row is a manual check, and not a gap, when at least one build task of the phase covers its ID and every build task that covers it has `manual:` at the start of that ID's check. Then:

- its tasks are not reopened for it, and the phase can end as done;
- the summary has a `Check by hand:` line for it, as [The summary](#the-summary) says.

Everything else stays a gap:

- An `untested` row where any covering build task has a check for that ID without the word: a test can close it.
- An `unmet` or `partial` row, whatever its check: the code is wrong or missing.

Decide by the word alone. Never conclude that a check is manual from its wording, the task's Files, or the requirement. In a `tasks.md` that has no `manual:` check, every `untested` row is a gap.

## Reopening and reworking

For each gap row, the tasks to reopen are the build tasks of this phase whose Covers include the row's ID. The verify task is never reopened: it has not run yet. A gap whose ID no build task of the phase covers ends the run: `Stopped: <ID> is <verdict> but no task of phase <n> covers it. Add one with write-tasks, then run build-phase again.`

1. When the rounds already made equal the round limit and gaps are left (at once, with a limit of 0): end the run, `Stopped: <IDs> still not met after <limit> rework rounds`. Reopen nothing.
2. Check that the current branch is `<branch_prefix><feature>/phase-<n>`; otherwise stop with `Stopped: not on the phase branch`.
3. Set `**Status:** Todo` on each task to reopen, and nothing else in the file. Stage `tasks.md` by path and commit it with the subject `Reopen <T-ids>: <gap IDs> <verdicts>`. Nothing else is staged. Never amend, never push.
4. Run each reopened build task in file order as in [Running a task](#running-a-task), with the gap rows for its Covers in the prompt, then [Verifying the phase](#verifying-the-phase) again. That is one round.

## The summary

A stop is still the whole summary. Wrong, because a sentence comes first:

```
There is no tasks file for invoice-export.

Phase ? of invoice-export: stopped
...
```

Right: the `Phase` line is the first line.

`Tasks: <k> implemented, <r> reworked` counts build tasks only. `<k>` is the build tasks this run implemented for the first time; `<r>` is the build tasks it reopened, each once however many rounds it took. A task in `<r>` is not also in `<k>`. The verify task (`**Files:** None.`) is in neither number, even though it ran through `implement-task` and replied done. Count from the task IDs, not from the number of subagents you started.

Wrong, for a phase whose build tasks T-1.2 and T-1.3 were implemented, T-1.1 reopened once, and verify task T-1.4 run last: `Tasks: 3 implemented, 1 reworked` (T-1.4 counted). Right: `Tasks: 2 implemented, 1 reworked`. When the run stops before a phase is picked (no `tasks.md`, no `requirements.md`, no `Todo` task), write the phase as `?`: `Phase ? of <feature>: stopped`, `Branch:` the branch from the start, and `Tasks: 0 implemented, 0 reworked`.

`Check by hand: <ID>: <check>` is written once for each [manual check](#manual-checks) row of the last report, in the report's order, after the `Verify:` line. `<check>` is the text after `manual: ` in that ID's check, copied as written from the first build task that covers it. The lines are there whether the run is done or stopped, so a `Verify:` tally with `untested` in it is explained; with `Verify: not run` there are none. A row that is `met` or a gap gets no line.

The phase title in the `Next:` line is the text after `### Phase <n>: ` in `tasks.md`, copied as written.

## Never

- Edit code, tests, requirements, the plan, or any task text; only the `Status` line of a task you reopen.
- Push, pull, merge, rebase, reset, stash, amend, or switch branches.
- Implement or verify in your own context: always a subagent, and always a different one for verify. An agent with no subagents [stops](#running-a-task).
- Retry a stop line, or retry more than once.
- Answer an open question or mark a blocked requirement as a gap.

## Validation checklist

1. Every task you ran was named, and ran only with its dependencies `Done`.
2. Every subagent reply went through `parse_reply.py` (unless you cannot run commands); no stop line was retried; no task or verify had more than two attempts.
3. Verify ran only after every task of the phase was `Done`, in a subagent that implemented nothing.
4. The only commits you made are `Reopen` commits that change only Status lines of `tasks.md`.
5. Nothing was pushed, and the branch is the one `implement-task` chose.
6. The summary lines match what happened: counts of implemented and reworked tasks, the last report's tally, one `Check by hand:` line per manual check row, and a `Stopped:` line exactly when the run stopped.
7. No task was reopened for a manual check row, and no row was treated as a manual check without the word `manual:` in every covering task.
