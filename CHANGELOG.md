# Changelog

Versions follow `.claude-plugin/plugin.json`. Claude Code uses that version to decide when installed users get an update, so every release bumps it.

## Unreleased

- write-spec, write-plan, write-tasks: `disable-model-invocation: true`. They run only when the user types the skill's name, so a phrase like "break this down" no longer starts an authoring step that asks questions and saves files. Descriptions no longer carry "Use when" trigger phrases.
- implement-task: one branch per phase, `<feature>/phase-<n>`, created from the default branch for phase 1 and from the previous phase's unmerged branch after that. A `Todo` task that already has a commit is a rework: it takes the verify rows as context and commits `T-<p>.<n>: <title> (rework)`. New stop line when a rework has nothing to fix.
- New `skills/build-phase/scripts/parse_reply.py`: parses a verify-spec report or an implement-task reply (tolerant by default, `--strict` for evals); `evals/verify-spec/hooks.py` and the new `evals/implement-task/hooks.py` use it.
- New draft skill `build-phase` (user-only, not yet in `plugin.json`): drives a phase through implement-task and verify-spec subagents, with a rework loop. New config key `build_max_rework_rounds`.
- write-spec: with no path in the request and no `spec_output_dir`, it asks where to save before writing anything, instead of silently writing no file. "Chat only" is an accepted answer.
- Evals: the three skills' prompts are slash commands, and their `fires: true` routing cases are removed, since the agent cannot call them. Not re-run.

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
