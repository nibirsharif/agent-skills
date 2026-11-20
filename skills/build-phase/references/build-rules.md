# Build Rules

These rules are authoritative for `build-phase`. Check the run against the [checklist](#validation-checklist) before you print the summary.

## Finding the files and the phase

- Run [find_tasks.py](../scripts/find_tasks.py) by its full path, with the project as the current directory, before any other search. Give it `--feature <name>` when the user names a feature, `--path <path>` when they name a path, and no argument when they name neither; add `--phase <n>` when they name a phase. Do what it prints:
  - `found <path>`: that is `tasks.md`, with `plan.md` and `requirements.md` beside it. Use it and no other.
  - `rounds <n>`, the line after `found`: the round limit, the most rework rounds this run may make. `rounds 0` means no task is ever reopened.
  - `stop`, then the lines of a stopped summary: those lines are your whole reply.
  - `ask <question>`: the question is your whole reply, as written, in place of a summary. Never answer it yourself. The one exception is `ask Where is tasks.md?` when the next point gives the feature's folder: run the script once more with `--path` to the `tasks.md` in that folder, and do what it prints.
- **Without `spec_output_dir`:** A path to the feature's `requirements.md`, `plan.md`, or `tasks.md` that appears earlier in this conversation, named by the user or reported saved by a skill of this chain, gives the feature's folder, since the three files live together: use it when the file you need is in that folder and the user names no other feature. Otherwise ask for the path, and the question is your whole reply. Never search the project for the file or use a path you chose yourself.
- **Phase:** the one the user named. Otherwise the first phase of `tasks.md`, in file order, that has a `Todo` task. A named phase with no `Todo` task and no gap to find is a stop: `Every task in <path> is Done.`
- Run `git branch --show-current` once at the start. Do not change branch yourself: `implement-task` does. Read no other setting: the subagents read their own.

## Running a task

**No subagents.** Before the first task, check that you have a tool that starts a subagent (the Agent tool, or Task under its older name). When you have none, or the first call is refused because the tool is not available, end the run: `Stopped: This agent cannot start subagents, which build-phase needs. Run implement-task for each task of phase <n>, then verify-spec, yourself.` Change nothing, and never do a task's work or the verify in your own context in its place.

Start one subagent per task, with the Agent tool and the general-purpose type, never in the background, and never two at once. Its prompt is exactly:

```
Call the Skill tool with implement-task. Implement task <T-id> of <path to tasks.md>. <rework only: This task was reopened. Gap rows from verify-spec: <the rows for its Covers>.> Reply as the skill says.
```

Tasks run in file order within the phase; a task runs only when its dependencies are `Done` in `tasks.md` (re-read the file after each task).

**The verify task** is the phase's task with `**Files:** None.` It is not a build task: run it only after [Verifying the phase](#verifying-the-phase) reports no gaps, as the last step before the summary. Run earlier, its check fails by design.

**Parse every reply with the script**, a done one too: it checks what reading cannot. With your file-writing tool, write the reply exactly as it came back, every line, to a new file in the system temp directory (outside the project, so `implement-task` never sees an uncommitted file), and pass that file:

```
python3 <this skill folder>/scripts/parse_reply.py implement <file>
```

Never retype the reply into a heredoc, `echo`, or the command line, and never shorten or rebuild it: the script can then reject it for something the subagent did not do. Do what the JSON's `kind` says, not what the reply looks like:

- **done**: the task is finished. Keep its commit.
- **stop**: one of `implement-task`'s stop lines. End the run: `Stopped: <the script's relay>`, which is the line with build-phase as the command to rerun. Never retry or work around a stop line.
- **invalid**: first re-read `tasks.md` and `git log -1 --format=%s`. When the task is `Done` and the last commit subject starts with `<T-id>:`, only the reply was wrong, so count the task as done. Otherwise start one new subagent with the same prompt. A second `invalid` ends the run: `Stopped: <T-id> gave no usable reply twice`.

## Verifying the phase

When every build task of the phase is `Done`, start a separate subagent (a fresh one, never one that implemented a task) with the prompt:

```
Call the Skill tool with verify-spec. Verify phase <n> of <path to requirements.md>. Reply as the skill says.
```

Parse its reply through a file in the same way, naming the requirements file, so a report without exactly one row for every ID in it is rejected:

```
python3 <this skill folder>/scripts/parse_reply.py verify --requirements <path to requirements.md> <file>
```

- **stop**: end the run with the line.
- **report**: the summary's tally is the script's `tally`, counted from the rows, never the report's own `Tally:` line; one that miscounts does not make a report invalid. Gaps are the rows `unmet` and `partial`, and each `untested` row that is not a [manual check](#manual-checks). `cannot tell` (it needs `write-spec`) and `skipped` are not gaps. With gaps, go to [Reopening and reworking](#reopening-and-reworking). With none, run the verify task as [Running a task](#running-a-task) says; the phase is done when it replies done.
- **invalid**: no report, or one the script rejects, such as a `met` row without a path:line and a passed test. Never fix a report yourself: start one new verify subagent with the same prompt. A second `invalid` ends the run: `Verify: no usable report` and `Stopped: verify-spec gave no usable reply twice`.

**A gap is never dropped by a retry.** The script's output for a rejected report still has the `rows` it could read. Before the retry, note the gap rows among them. When the retry gives any of those IDs a verdict that is not a gap, neither report is trusted: end the run with `Stopped: verify-spec gave <ID> <first verdict> in a rejected report and <second verdict> on the retry. Check <ID> against the code, then run build-phase again.`, one `<ID> <first verdict> ... <second verdict>` clause per ID, joined by `; `.

## Manual checks

A task's Done when holds one check per ID, `<ID>: <check>`. A check that starts with the word `manual:` (`FR-007: manual: ...`) is made by a person: no test can turn its row into `met`, so reworking it cannot succeed.

An `untested` row is a manual check, and not a gap, when at least one build task of the phase covers its ID and every build task that covers it has `manual:` at the start of that ID's check. Its tasks are not reopened for it, the phase can end as done, and the summary has a `Check by hand:` line for it.

Everything else stays a gap: an `untested` row where any covering build task has a check for that ID without the word (a test can close it), and an `unmet` or `partial` row, whatever its check. Decide by the word alone, never from a check's wording, the task's Files, or the requirement.

## Reopening and reworking

For each gap row, the tasks to reopen are the build tasks of this phase whose Covers include the row's ID; the verify task is never one of them. A gap whose ID no build task of the phase covers ends the run: `Stopped: <ID> is <verdict> but no task of phase <n> covers it. Add one with write-tasks, then run build-phase again.`

1. When the rounds already made equal the round limit and gaps are left (at once, with a limit of 0): end the run, `Stopped: <IDs> still not met after <limit> rework rounds`. Reopen nothing.
2. Check that the current branch is `<branch_prefix><feature>/phase-<n>`; otherwise stop with `Stopped: not on the phase branch`.
3. Set `**Status:** Todo` on each task to reopen, and nothing else in the file. Stage `tasks.md` by path and commit it with the subject `Reopen <T-ids>: <gap IDs> <verdicts>`. Nothing else is staged. Never amend, never push.
4. Run each reopened build task in file order as in [Running a task](#running-a-task), with the gap rows for its Covers in the prompt, then [Verifying the phase](#verifying-the-phase) again. That is one round.

## The summary

Unless `find_tasks.py` printed `stop`, the run ends by printing the summary with [summary.py](../scripts/summary.py), and the reply is what it printed, copied whole:

```
python3 <this skill folder>/scripts/summary.py --feature <feature> --phase <n> --branch <branch> \
  --implemented <k> --reworked <r> --verify '<tally, not run, or no usable report>' \
  [--check-by-hand '<ID>: <check>' ...] (--stopped '<the stop line or reason>' | --title '<phase title>')
```

Give each value without its label (`Stopped:`, `Verify:`):

- `--implemented` and `--reworked` count build tasks as the reply contract says, from the task IDs, not from the number of subagents you started. A reopened task is in `<r>` once, however many rounds it took, and is not also in `<k>`. Wrong, for a phase whose build tasks T-1.2 and T-1.3 were implemented, T-1.1 reopened once, and verify task T-1.4 run last: `Tasks: 3 implemented, 1 reworked` (T-1.4 counted). Right: `Tasks: 2 implemented, 1 reworked`.
- `--check-by-hand`, once for each [manual check](#manual-checks) row of the last report, in the report's order, whether the run is done or stopped. `<check>` is the text after `manual: ` in that ID's check, copied as written from the first build task that covers it.
- `--title`: the text after `### Phase <n>: ` in `tasks.md`, copied as written.

Most stops are yours to decide, from `parse_reply.py`'s JSON or the branch name: decide, run `summary.py` with `--stopped`, and copy its output. The `Stopped:` line is the reason, given once. Wrong, because the decision is written out before the printed lines:

```
FR-003 is still unmet and both rework rounds are used, so nothing more is reopened.

Phase 2 of invoice-export: stopped
...
Stopped: FR-003 still not met after 2 rework rounds
```

Right: the printed lines alone, so the `Phase` line is the first line and nothing follows the last.

## Validation checklist

1. Every task ran by name, with its dependencies `Done`.
2. Every subagent reply went through `parse_reply.py` whole, from a file. No stop line was retried, no task or verify had more than two attempts, and no gap of a rejected verify report was dropped by its retry.
3. Verify ran after every build task of the phase was `Done`, in a subagent that implemented nothing. You implemented and verified nothing in your own context.
4. Your only commits are `Reopen` commits that change only Status lines of `tasks.md`. You edited nothing else and answered no open question.
5. Nothing was pushed, pulled, merged, rebased, reset, stashed, or amended, and you never switched branch.
6. The summary's values match what happened, with a `Stopped:` value exactly when the run stopped.
7. No task was reopened for a manual check row, and no row was treated as a manual check without `manual:` in every covering task.
