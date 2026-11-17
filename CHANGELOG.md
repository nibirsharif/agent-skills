# Changelog

Versions follow `.claude-plugin/plugin.json`. Claude Code uses that version to decide when installed users get an update, so every release bumps it.

## Unreleased

On `master`, not yet in a release: installed plugins get these with the next version bump.

- implement-task: a new script, `scripts/pick_task.py`, does the first three workflow steps: it finds `tasks.md`, checks the working tree, and picks the task. It prints `found <path>` and `task <T-id>` (with ` rework` for a task that already has a commit), or `stop <the stop line>`, or `ask <what>`. It decides these stop lines: no tasks file, uncommitted changes, no Status lines, no such task, already Done, a dependency not Done, a requirement no task covers, and every task Done. Task mismatch, a failed check, and a rework with nothing to fix are still the agent's. The five stop-line eval cases passed 30 of 30 with it, against about half before, when most misses were a sentence before a correct stop line.
- implement-task: asked for a requirement in place of a task (`--requirement FR-003`), the script takes the first task not yet `Done` that builds it, never the phase's verify task. Before, the rules did not say which task that was.
- verify-spec: a new script, `scripts/check_scope.py`, does the first two workflow steps: it finds `requirements.md` and checks the named ID or phase. It prints `found <path>` and `scope <all, an ID, or a phase with its IDs>`, or `stop <the stop line>`, or `ask <what>`. Every stop line of the skill now comes from it. `unknown-id` and `missing-requirements` passed 12 of 12.
- Evals: benchmarks for verify-spec, write-plan, and write-tasks, in the format of write-spec's: inputs with hidden references, a `dev-*` and a `hold-*` set, scored by hand, each with a baseline on `claude-sonnet-5-5`. verify-spec got every verdict right on six projects with planted faults (36 of 36 rows, no gap called `met`). write-plan covered every ID and kept every dependency, and cut more and smaller phases than the references in 3 of 5 plans. write-tasks covered every ID with checks that can be run; 4 of 44 tasks hold two changes. `evals/bench.py` now runs an input in a copy of its `project/` folder and records the model ID.
- write-plan: a new stop line. When one requirement alone needs more files than `plan_max_files_per_phase`, the reply is exactly `<ID> needs more than <n> files on its own. Split it with write-spec, then run write-plan again.` and no plan is written. Before, the skill spread such a requirement over several phases and wrote phases that listed no requirement ID (3 of 3 eval runs); with the rule the case passed 4 of 4. A new reply line, so the next release is a MINOR one.
- Evals: two more write-plan cases, `phase-dependency` (phases follow what each step needs, not the order of the IDs) and `oversized-requirement` (the stop above).
- Evals: a case or benchmark input can have a `branch/` folder, committed on the branch `feature-work`, so drift on a feature branch can be tested.
- No file format or ID changes, and one new reply line (write-plan's stop above). Where the agent cannot run commands, each skill's written rules still apply.

## 0.14.0

- verify-spec: a new script, `scripts/find_requirements.py`, finds `requirements.md` the way implement-task's script finds `tasks.md`: run first, it prints `found <path>`, `stop <the no-requirements-file stop line>`, or `ask <what>`, and a named feature is looked up at one path only. `missing-requirements` passed 20 of 20 eval runs with it, against about 1 in 3 before, when most runs opened with a sentence.
- build-phase: a new script, `scripts/find_tasks.py`, finds `tasks.md` and checks that `requirements.md` is beside it. For a stop it prints the whole stopped summary, so the reply is copied rather than composed. `missing-tasks` passed 10 of 10 on `claude-sonnet-5-5`, and 12 of 20 on `claude-sonnet-5`, where it passed 0 of 20 before.
- build-phase: when git names no current branch (a detached HEAD, or not a repository), the summary's `Branch:` line is `Branch: none`.
- The three lookup scripts share one core. A skill cannot load code from another skill's folder, so each has its own copy, and a unit test fails when the copies differ.
- No file format, ID, or reply line changes. Where the agent cannot run commands, each skill's written lookup rules still apply.

## 0.13.0

- implement-task: a new script, `scripts/find_tasks.py`, finds `tasks.md`. The skill runs it before any other search and does what it prints: `found <path>`, `stop <the no-tasks-file stop line>`, or `ask <what>`. A feature the user names is looked up at `<spec_output_dir>/<feature>/tasks.md` and nowhere else. Before, asked for a feature that has no task list, the skill sometimes searched the project, found another feature's `tasks.md`, and implemented and committed its next task (4 of 53 eval runs). With the script: 0 of 60, and no sentence before the stop line in those runs.
- implement-task: where the agent cannot run commands, the written lookup rules still apply. They now state the named-feature case first and say not to look for other `tasks.md` files.
- No file format, ID, or reply line changes. The skill needs Python 3 for the lookup, as the other scripts do.
- Evals: `evals/run.py` prints the model ID and the Claude Code version in its Summary line, with a pass count, and saves both in each run's stats. The alias `sonnet` is a different model in different Claude Code versions, and results recorded without the model ID could not be compared.
- build-phase evals: the hook reports a wrong summary (`summary: ...`) and text around a correct one (`outside the summary: ...`) separately. Both still fail a run.
- Eval results: build-phase passes 12 of 12 on `claude-sonnet-5-5`. Its sentence before the summary is specific to `claude-sonnet-5` (0 of 20 on `missing-tasks`), and three wordings did not change that. For the implement-task and verify-spec stop lines the sentence is as frequent on `claude-sonnet-5-5`, and two wordings did not change it. The numbers are in each skill's eval README.

## 0.12.0

- build-phase: a phase with a requirement only a person can check can now finish. An `untested` row is a gap only when a test can close it. When every build task that covers the ID marks its check `manual:`, the tasks are not reopened and the phase can end as done. Before, every `untested` row was reworked, the rework could not succeed, and the run ended in `Stopped`. `unmet` and `partial` rows are reworked as before, and verify-spec's verdicts are unchanged.
- build-phase: the summary has a new line after `Verify:`, `Check by hand: <ID>: <check>`, one per requirement with a manual check, copied from the task's Done when.
- write-tasks: a Done when check is a test or a command whenever a test runner the project has can make it. A check a person must make is written `<ID>: manual: <what to do and what to see>`; "behaviour to observe" without the word is no longer a check. The verify task repeats the phase's manual checks.
- implement-task: for a `manual:` check it builds the behaviour, adds no test, and never makes or reports the check; the verify task leaves those IDs out of the Verify list it runs. The reply format is unchanged.
- Files saved earlier: a `tasks.md` without `manual:` behaves as before. To mark a check that needs a person, add `manual:` after the ID in the task's Done when and in the verify task's.
- build-phase evals: new case `manual-check-done`.

## 0.11.0

- write-spec: every requirement in a follow-up reply carries `(new)` or `(changed)`. Before, a follow-up to a first reply that held only questions often left the marker out. The lint has a `--follow-up` option that fails an unmarked requirement line.
- write-spec: a new "Coverage gaps" section in the rules replaces the one-line failure-case check. Every reply now checks the whole set, not only the requirements it writes: a trigger failing, the other side of a condition, and what a requester receives when a `shall not` refuses the request. A follow-up reply can therefore ask new questions about earlier requirements.
- write-spec: an `If ... then` requirement is an exception to the `When` requirement with the same trigger, and the `When` requirement no longer repeats the opposite of its condition (`for a report of at most 100,000 rows`).
- write-spec: when a statement names no system, the skill now looks in the project (the Systems lines of saved requirements files, the root README, and the top-level folder names) and, if they name exactly one candidate, asks with `Proposed: the <name>`. The name is written into a requirement only after you accept it. Before, the question came with no proposal. Only the name is taken from the project: what the project already does (its requests, paths, fields, status codes) is not input, so it causes no question and no requirement.
- write-spec evals: new cases `followup-answers`, `followup-first-requirements`, and `propose-system`, and a benchmark in `evals/write-spec/benchmark/` with a recorded 0.10.0 baseline.

## 0.10.0

- write-spec: a closed question keeps its question: `Q-NNN: Closed. <question> Answer: <answer>`, not `Closed. Answer: <answer>`, which read as `Answer: Yes.` with nothing to say what was asked. The lint fails a closed line without the question. Files saved earlier: re-add the question to each closed line, or the lint flags it when write-spec next updates the file.
- AGENTS.md: when to bump MINOR or PATCH.

## 0.9.0

- README: a Prerequisites section (Claude Code, git, Python 3; `build-phase` needs Claude Code), the four config keys the table was missing, an Eval results table from the latest recorded runs, a link to EARS, and a CI badge.
- New config keys `test_command`, `base_branch`, `branch_prefix`, read by implement-task, verify-spec, and build-phase. All default to the old behaviour.
- Evals: a case's `committed/` folder is copied over the fixture before it is committed; the new implement-task case `test-command` uses it to set `test_command` and checks that the configured command runs and is named in the Check line (3 of 3 runs).
- CI also runs `claude plugin validate`.
- Removed `examples/example-skill/`: it had not changed since the first commit and no longer matched the skills. AGENTS.md now says to model a new skill on an existing one.
- write-spec eval `prd-solar-monitoring`: the daylight/offline check accepts `daylight` as well as `sunrise` and any wording of the `if ... then` clause.

## 0.8.0

- write-tasks: `tasks.md` no longer has a file-level `**Status:** Draft` line that never changed; each task's Status is the only status. Plugin keywords now include "tasks" and "verify".
- write-spec, write-plan, write-tasks: `disable-model-invocation: true`. They run only when the user types the skill's name, so a phrase like "break this down" no longer starts an authoring step that asks questions and saves files. Descriptions no longer carry "Use when" trigger phrases.
- implement-task: one branch per phase, `<feature>/phase-<n>`, created from the default branch for phase 1 and from the previous phase's unmerged branch after that. A `Todo` task that already has a commit is a rework: it takes the verify rows as context and commits `T-<p>.<n>: <title> (rework)`. New stop line when a rework has nothing to fix.
- New `skills/build-phase/scripts/parse_reply.py`: parses a verify-spec report or an implement-task reply (tolerant by default, `--strict` for evals); `evals/verify-spec/hooks.py` and the new `evals/implement-task/hooks.py` use it.
- New skill `build-phase` (user-only): drives a phase through implement-task and verify-spec subagents, with a rework loop. New config key `build_max_rework_rounds`. The phase's verify task now runs last, after verify-spec reports no gaps: run earlier, its check fails by design and the first eval run stopped there. When the run stops before a phase is picked, the first line is `Phase ? of <feature>: stopped`. Evals in `evals/build-phase/`: the rework loop recovers a planted gap (3 runs: 9 of 9 pass after the two fixes below); bare `implement-task` and `verify-spec` resolve in subagents when only the plugin is installed.
- write-spec: with no path in the request and no `spec_output_dir`, it asks where to save before writing anything, instead of silently writing no file. "Chat only" is an accepted answer.
- Evals: the three skills' prompts are slash commands, and their `fires: true` routing cases are removed, since the agent cannot call them. Re-run at 3 runs each (Sonnet): write-plan 18/18, write-tasks 21/21, implement-task 26/30, write-spec 17/21 or better. The implement-task misses are all a sentence before a stop line (the rules file now shows that case as wrong); write-spec's `prd-solar-monitoring` still misses on brittle keyword checks in about half the runs.
- implement-task evals: trace checks accept `git checkout -q -b` and a code edit made through a Python script, not only `Edit`/`Write`. write-spec's `clean-feature` input now names the instant to log (the time of the click), so it has no real ambiguity left.
- build-phase: the last message starts with `Phase`, never with a sentence about what was found (it did in 2 of 3 `missing-tasks` runs).
- implement-task: the test that must fail without the change is shown failing by running it before the code edit, never by `git stash` or reverting files (a rework subagent stashed in 1 of 3 runs).

## 0.7.0

- New skill `verify-spec`: checks the code against a saved `requirements.md` and replies with one table: a verdict per `FR` and `NFR` (`met`, `partial`, `unmet`, `untested`, `cannot tell`, `skipped`) with `file:line` and test evidence, then `Tests:`, `Tally:`, and `Drift:` lines. `met` needs the code and a test that ran and passed in this run, and the weaker verdict wins when two fit. Can be limited to one phase of `plan.md` or one ID, or run on pasted requirements. Blocked requirements are `skipped`, and `tasks.md` is never read. Read-only: runs the project's test command once, edits nothing, commits nothing. A missing requirements file, an unknown ID or phase stops with one line.
- Evals: `evals/verify-spec/` has a fixture with planted gaps (a missing implementation, a missing test, a vague NFR, a blocked requirement, an uncommitted stray file) and nine cases; `hooks.py` checks the reply's shape, the tally against the rows, and the evidence a `met` row needs.
- Known: in eval runs (Sonnet, 27 runs) about 85% passed. About one reply in ten opens with a sentence before the table or the stop line, and the drift line is occasionally wrong when the only changed file is an uncommitted one.

## 0.6.0

- New skill `implement-task`: implements one task from a saved `tasks.md`, the named `T-` ID or the next `Todo` task whose dependencies are `Done`. Changes only the task's files, adds the test its Done when names, runs the full suite, sets the task's Status to `Done`, and commits it on the feature branch (created from the default branch when needed), staging by path. Never pushes. On its first run it first commits the feature's own spec files (requirements, plan, tasks) as `Add <feature-name> spec`, so the chain can run straight after write-tasks. A missing tasks file, an unfinished dependency, blocked work, a task that does not fit the code, changes outside the feature's folder, or a failing check stops with one line.
- write-tasks: every task has a sixth part, `**Status:** Todo` or `Done`. A phase with a `Done` task counts as started when `tasks.md` is updated, so write-tasks no longer has to ask. Files saved by 0.5.0 have no Status lines; re-run write-tasks to add them.
- Evals: a skill's `config.json` can name a `"fixture"` folder that every case starts in, committed as a git repository on `main`; a case's `dirty/` folder is copied over it uncommitted.

## 0.5.0

- write-spec: functional requirement IDs are now `FR-001`, `FR-002`, … instead of `REQ-001`, so they pair with `NFR-` (the three sequences are `FR-`, `NFR-`, `Q-`). A behaviour with a threshold is split into an `FR` and an `NFR`.
- write-plan and write-tasks: read `FR-` and `NFR-` IDs. The `REQ-` legacy handling is removed: files saved by earlier versions are not supported.
- Evals, examples, and templates use `FR-`; the `legacy-ids` plan case is removed.

## 0.4.0

- New skill `write-tasks`: reads a saved `plan.md`, explores the codebase, and writes `tasks.md`: each phase split into small tasks numbered `T-<phase>.<n>`, with the `REQ` and `NFR` IDs each covers, its files (`new:` when the file does not exist), the earlier tasks it depends on, and a one-line check that cites each ID. Each phase ends with a verify task.
- write-tasks: blocked requirements are copied from the plan's `Blocked by` entries and never tasked; open questions are never answered. A missing plan, a plan that lists a withdrawn ID, or a phase that needs more tasks than the limit stops with one line pointing to write-plan or write-spec.
- New config keys `tasks_max_files_per_task` (default 3) and `tasks_max_per_phase` (default 12).
- Known: on Haiku 4.5, write-tasks often did not fire, either on a request that did not name it or when the plan file was missing (it read the path and asked for it instead). Sonnet passed every eval case in 2 runs each.

## 0.3.0

- New skill `write-plan`: reads a saved `requirements.md`, explores the codebase, and writes `plan.md`: the approach split into phases that each merge as one reviewable PR, with the `REQ` and `NFR` IDs each covers, code to reuse, interface and data changes, and how to verify.
- write-plan: requirements that wait on open questions are listed as `Blocked by Q-nnn` and not planned; a question that decides the core approach stops the plan and is asked in chat. A missing requirements file stops with one line pointing to write-spec.
- write-plan: each `NFR` is placed with the `REQ` it constrains. Withdrawn IDs are skipped, and files saved by write-spec 0.1.0 keep their `REQ` IDs in section 4.
- New config keys `plan_max_requirements_per_phase` (default 8) and `plan_max_files_per_phase` (default 10).
- Known: in eval runs the agent sometimes writes a line before `## 1. Approach` in a chat reply. On Haiku 4.5, write-plan did not fire on a request that did not name it (Sonnet 5 did), and large specs were sometimes split with a phase depending on a later one.

## 0.2.0

- write-spec: non-functional requirements get their own ID sequence, `NFR-001`, `NFR-002`, …, next to `REQ-` (functional) and `Q-` (questions). Each sequence continues from its own highest ID.
- write-spec: a behaviour with a deadline or other quality threshold is split into a `REQ` for the behaviour and an `NFR` for the threshold. A timeout in a condition stays functional.
- write-spec: a requirement that moves to the other class is withdrawn with `Withdrawn. Moved to <ID>.` and written under the next ID of the other sequence.
- write-spec: files saved by 0.1.0 keep their `REQ` IDs in the Non-Functional section; new non-functional requirements start at `NFR-001`.
- write-spec lint: checks `NFR` lines, flags an `NFR` in the Functional section, and flags a deadline in a `REQ` response.

## 0.1.0

- First release as a Claude Code plugin (`nibirsharif-skills`), with one skill: `write-spec`.
