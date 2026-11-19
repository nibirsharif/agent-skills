---
name: build-phase
description: Build one phase of a saved tasks.md end to end. Runs implement-task for each task in a fresh subagent, then verify-spec for the phase in a separate subagent, and reopens and reworks the tasks behind any requirement that is not met, up to a round limit. A requirement only a person can check is listed for you instead of reworked. Stops at the phase boundary with the phase branch ready for you to push and review. Never pushes, never opens a PR, never changes requirements, the plan, or the task list's contents. Run it by typing its name, with the feature and optionally the phase.
disable-model-invocation: true
---

# Build Phase

Drive one phase of a feature from its first `Todo` task to a verified phase branch. You do not implement or verify anything yourself: each step is a fresh subagent running `implement-task` or `verify-spec`, and you read their replies.

## Reply contract

Your last message is the summary, exactly these lines as plain text, and nothing else:

- `Phase <n> of <feature>: done` or `Phase <n> of <feature>: stopped`
- `Branch: <branch>`
- `Tasks: <k> implemented, <r> reworked`: `<k>` is the build tasks this run implemented from `Todo` for the first time, `<r>` the build tasks it reopened. The verify task is in neither number, however it ran. Tasks from an earlier run in the same conversation are not counted.
- `Verify: <the tally of the last report, counted from its rows>`, `Verify: not run`, or `Verify: no usable report` when verify-spec's reply was invalid twice
- `Check by hand: <ID>: <check>`, one line for each requirement a person must check, only when there are any
- `Stopped: <the stop line or reason>`, only when stopped
- `Next: push <branch>, open a PR titled "<feature> phase <n>: <phase title>", and run /code-review`, only when done

Write no text between tool calls. [scripts/summary.py](scripts/summary.py) prints the summary from the run's values, and the last message you write is what it printed, copied whole: it starts with `Phase`, never with a sentence about what you found or which rule applies, and nothing follows its last line. The `Stopped:` line is the only explanation a stop gets.

## Before starting

- Read [references/build-rules.md](references/build-rules.md) in full: picking the phase, the subagent prompts, parsing replies, reopening, limits, stop reasons, and the validation checklist. This file is authoritative.

## Scope

This skill only schedules work and reopens tasks. It never edits code, tests, or spec files, except the `Status` lines of the tasks it reopens. It never pushes, merges, or opens a PR, and never answers an open question. A step that needs a decision (a stop line, a malformed reply twice, a gap no task covers, the round limit) ends the run with the reason, and so does an agent that cannot start subagents.

## Workflow

1. **Find the files and the phase**, as the rules say: the lookup script first. When it prints `stop`, the lines after it are your whole reply.
2. **Implement:** for each build task of the phase in order (not the verify task), start a subagent that calls the Skill tool with `implement-task` for that task. Run [scripts/parse_reply.py](scripts/parse_reply.py) on every reply, a done one too, passing the reply whole through a file, never retyped, and act on its `kind`, not on how the reply reads (by the same shapes only when you cannot run commands). A done report goes on; anything else is handled as the rules say.
3. **Verify:** when every build task of the phase is `Done`, start a separate subagent that calls the Skill tool with `verify-spec` limited to the phase. Parse its report with the script: an `invalid` report is retried once and never copied. A Tally that miscounts the rows does not make a report invalid; the script counts it from the rows. A gap in a rejected report that its retry no longer calls a gap is a stop, never dropped.
4. **Rework:** a gap row (`unmet`, `partial`, or an `untested` one that is not a [manual check](references/build-rules.md#manual-checks)) reopens the build tasks behind it and sends them through step 2 again, then step 3, up to the round limit the lookup script printed (`rounds <n>`, from `build_max_rework_rounds`, default 2). At the limit the run stops.
5. **Close:** with no gaps, run the phase's verify task through `implement-task`.
6. **Finish:** as soon as the phase is done or a rule ends the run, run `summary.py` as the rules say, and reply with what it printed.
