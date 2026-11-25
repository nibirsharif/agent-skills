# write-tasks

Instructions the agent follows: [skills/write-tasks/SKILL.md](../skills/write-tasks/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Reads a saved `plan.md` and the `requirements.md` beside it, explores the codebase, and writes `tasks.md`: each phase split into small tasks numbered `T-<phase>.<n>`, in build order. Every task names the `FR` and `NFR` IDs it covers, the files it touches (`new:` for files that do not exist yet), the earlier tasks it depends on, a one-line check that shows it is done (a test or command, or a `manual:` check for a person), and a Status (`Todo` until [implement-task](implement-task.md) finishes it). Each phase ends with a verify task.

Blocked requirements are copied from the plan and never tasked. Open questions are never answered.

## When to use it

Type `/nibirsharif-skills:write-tasks` (or `/write-tasks` when installed from a clone). The agent never starts this skill on its own.

- You are about to implement a phase and want a checklist to work through one step at a time.
- You want each step small enough to review and to prove with a test or command.

It does not write requirements, change the plan, or write code.

## Output

When saved, one line for the path, then one line per phase (`Phase 1: 5 tasks (FR-001, FR-002, NFR-001)`) and the blocked entries. In chat only, the tasks themselves, starting at `## 1. Overview`. When you pasted the plan and did not ask for chat only, their last line says so: `Not saved: the plan was pasted, not read from a file. ...`.

It stops with a single line instead of tasking when:

| Situation | Where to go |
|-----------|-------------|
| Plan file missing or has no phase | write-plan |
| Plan lists a withdrawn or unknown requirement ID | write-plan or write-spec |
| A phase needs more tasks than the limit | split the phase in write-plan |

Limits: `tasks_max_files_per_task` (default 3) and `tasks_max_per_phase` (default 16); see [the config](../README.md#configuration).

## FAQ

**Why does it refuse a big phase instead of using bigger tasks?** A phase over the limit usually means the plan's cut is wrong. Squeezing it into fewer, larger tasks hides that. Split it in plan.md.

**What is the verify task?** The last task of a phase. It ties the earlier checks together and runs the full test suite, citing each requirement ID the phase covers.

**What happens to Status when I re-run it?** A phase with any `Done` task has started: its tasks keep their IDs and Status, and new work is appended as `Todo` tasks. The rules are in [updating.md](../skills/write-tasks/references/updating.md).

**When is a check `manual:`?** Only when no test runner the project has can make it: something a person sees in a browser, on a device, or in a real inbox. The check then reads `FR-007: manual: <what to do and what to see>`. The rule is in [task-rules.md](../skills/write-tasks/references/task-rules.md#manual-checks). [implement-task](implement-task.md) builds the behaviour without making the check, and [build-phase](build-phase.md) lists it for you at the end of the phase.

**Many of my checks came out manual. Can they be automated?** Yes, by giving the project a runner that can make them, for example a browser test runner, and including it in `test_command`. That is a plan decision: add it with [write-plan](write-plan.md), then run write-tasks again. A task never adds a test tool on its own.

**Can I use it on a plan I pasted?** Yes. It tasks from the pasted plan, but writes `tasks.md` only when `plan.md` exists on disk.

## Verifying results

- Each task is one focused change, with at most the file limit.
- Every requirement of a phase is covered by a task other than the verify task.
- Each "done when" check is a test or command you can run, or starts with `manual:` and says what to do and what to see.
- No check is `manual:` where the project's tests could make it.
- No task covers an ID from another phase.
- Every item the plan lists under a phase's Interface and data changes, such as a helper or a table, has a task that builds it, even when no Verify line names it, or the Overview names the file that already has it.

## Related skills

Third step of the chain: [write-spec](write-spec.md) → [write-plan](write-plan.md) → **write-tasks** → [implement-task](implement-task.md). It reads what the first two saved under `spec_output_dir` and writes `tasks.md` beside them; implement-task works through it one task at a time.
