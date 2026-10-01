# write-tasks

Instructions the agent follows: [skills/write-tasks/SKILL.md](../skills/write-tasks/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Reads a saved `plan.md` and the `requirements.md` beside it, explores the codebase, and writes `tasks.md`: each phase split into small tasks numbered `T-<phase>.<n>`, in build order. Every task names the `FR` and `NFR` IDs it covers, the files it touches (`new:` for files that do not exist yet), the earlier tasks it depends on, and a one-line check that shows it is done. Each phase ends with a verify task.

Blocked requirements are copied from the plan and never tasked. Open questions are never answered.

## When to use it

- You are about to implement a phase and want a checklist to work through one step at a time.
- You want each step small enough to review and to prove with a test or command.

It does not write requirements, change the plan, or write code.

## Output

When saved, one line for the path, then one line per phase (`Phase 1: 5 tasks (FR-001, FR-002, NFR-001)`) and the blocked entries. In chat only, the tasks themselves, starting at `## 1. Overview`.

It stops with a single line instead of tasking when:

| Situation | Where to go |
|-----------|-------------|
| Plan file missing or has no phase | write-plan |
| Plan lists a withdrawn or unknown requirement ID | write-plan or write-spec |
| A phase needs more tasks than the limit | split the phase in write-plan |

Limits: `tasks_max_files_per_task` (default 3) and `tasks_max_per_phase` (default 12); see [the config](../README.md#configuration).

## FAQ

**Why does it refuse a big phase instead of using bigger tasks?** A phase over the limit usually means the plan's cut is wrong. Squeezing it into fewer, larger tasks hides that. Split it in plan.md.

**What is the verify task?** The last task of a phase. It ties the earlier checks together and runs the full test suite, citing each requirement ID the phase covers.

**Can I use it on a plan I pasted?** Yes. It tasks from the pasted plan, but writes `tasks.md` only when `plan.md` exists on disk.

## Verifying results

- Each task is one focused change, with at most the file limit.
- Every requirement of a phase is covered by a task other than the verify task.
- Each "done when" check is something you can run or observe.
- No task covers an ID from another phase.

## Related skills

Last step of the chain: [write-spec](write-spec.md) → [write-plan](write-plan.md) → **write-tasks**. It reads what the first two saved under `spec_output_dir` and writes `tasks.md` beside them.
