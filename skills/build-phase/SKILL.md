---
name: build-phase
description: Build one phase of a saved tasks.md end to end. Runs implement-task for each task in a fresh subagent, then verify-spec for the phase in a separate subagent, and reopens and reworks the tasks behind any requirement that is not met, up to a round limit. Stops at the phase boundary with the phase branch ready for you to push and review. Never pushes, never opens a PR, never changes requirements, the plan, or the task list's contents. Run it by typing its name, with the feature and optionally the phase.
disable-model-invocation: true
---

# Build Phase

Drive one phase of a feature from its first `Todo` task to a verified phase branch. You do not implement or verify anything yourself: each step is a fresh subagent running `implement-task` or `verify-spec`, and you read their replies.

## Reply contract

Your last message is the summary, exactly these lines as plain text, and nothing else:

- `Phase <n> of <feature>: done` or `Phase <n> of <feature>: stopped`
- `Branch: <branch>`
- `Tasks: <k> implemented, <r> reworked`
- `Verify: <the Tally line of the last report>`, or `Verify: not run`
- `Stopped: <the stop line or reason>`, only when stopped
- `Next: push <branch>, open a PR titled "<feature> phase <n>: <phase title>", and run /code-review`, only when done

Write no text between tool calls.

## Before starting

- Read [references/build-rules.md](references/build-rules.md) in full: picking the phase, the subagent prompts, parsing replies, reopening, limits, stop reasons, and the validation checklist. This file is authoritative.

## Scope

This skill only schedules work and reopens tasks. It never edits code, tests, or spec files, except the `Status` lines of the tasks it reopens. It never pushes, merges, or opens a PR, and never answers an open question. A step that needs a decision (a stop line, a malformed reply twice, a gap no task covers, the round limit) ends the run with the reason.

## Workflow

1. **Find the files and the phase**, as the rules say. No `tasks.md`: stop.
2. **Implement:** for each task of the phase in order, start a subagent that calls the Skill tool with `implement-task` for that task. Parse its reply with [scripts/parse_reply.py](scripts/parse_reply.py) (or by the same shapes when you cannot run commands). A done report goes on; anything else is handled as the rules say.
3. **Verify:** when every task of the phase is `Done`, start a separate subagent that calls the Skill tool with `verify-spec` limited to the phase. Parse its report.
4. **Rework:** a row that is `unmet`, `partial`, or `untested` reopens its tasks and sends them through step 2 again, then step 3, up to `build_max_rework_rounds` rounds (default 2).
5. **Finish** with the summary.
