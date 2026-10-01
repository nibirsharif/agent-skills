# Changelog

Versions follow `.claude-plugin/plugin.json`. Claude Code uses that version to decide when installed users get an update, so every release bumps it.

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
