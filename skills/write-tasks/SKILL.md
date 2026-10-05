---
name: write-tasks
description: Break each phase of a saved implementation plan (plan.md from write-plan) into small, ordered, verifiable tasks and save them as tasks.md next to the plan. Explores the codebase first; every task names the requirement IDs it covers, the files it touches, the tasks it depends on, and a check that shows it is done. Blocked requirements and open questions are never tasked. Not for writing requirements, the plan itself, or code.
disable-model-invocation: true
---

# Write Tasks

Turn a feature's `plan.md` into `tasks.md`: each phase split into small tasks, in build order, each with a check that says when it is done. Read the code first; task only what the plan covers.

## Reply contract

Your reply is one of three things, and its first character is the first character of that thing:

1. **The tasks:** they start with `## 1. Overview`. Nothing comes before it. Say that there is no codebase or no file on disk inside the Overview.
2. **A stop line**, when the plan cannot be tasked, and nothing else. Use exactly:
   - plan file missing or without a phase: `No plan file found at <path>. Run write-plan first to write the plan, then run write-tasks again.`
   - plan and requirements disagree: one line naming the ID and the conflict, then `Fix it with write-plan or write-spec, then run write-tasks again.`
   - a phase needs more tasks than the limit: `Phase <n> needs more than <limit> tasks. Split it in plan.md with write-plan, then run write-tasks again.`
3. **The questions**, when a phase is too vague to break into tasks without a guess.

Write no text between tool calls. Details are in [Output](#output).

## Before writing

- Read [references/task-rules.md](references/task-rules.md) in full before producing anything: how to read the plan, what to explore, task shape and size, ordering, coverage, and the validation checklist. This file is authoritative.
- Before writing or updating a file, read [references/tasks-template.md](references/tasks-template.md).
- Read [references/examples.md](references/examples.md) before your first reply in a conversation, and again when unsure of a task split or a saved file.

## Scope

This skill writes the task list only. It does not write requirements, change the plan, or write code. Never invent a requirement, a file, or a utility. A task names only what the plan states and what you found in the code. Never answer, close, or assume an open question; answering belongs to `write-spec`.

## Workflow

Work silently. Write no text between tool calls and none before the reply.

1. **Find and read the plan**, as [Saving to a file](#saving-to-a-file) says, and the `requirements.md` beside it when it exists. If the plan is missing or has no phase, reply with the stop line and stop. If a `tasks.md` already exists beside the plan, read it: you are updating it.
2. **Check the plan against the requirements.** Every ID in a phase must be a written requirement. A withdrawn or unknown ID is a stop line.
3. **Explore the codebase** as the rules' "Exploring the code" section says.
4. **Split each phase into tasks** as the rules say: shape, size, order, coverage. List the tasks and count them against the limit before writing any; a count over the limit is the stop line, not a reason to merge tasks.
5. **Validate** against the rules' checklist. Fix what fails; a check you cannot pass is a question, not a task.
6. **Return** the tasks as [Output](#output) says, and **save** if a path is set.

## Output

- Saved: state the path in one line, then one line per phase: `Phase <n>: <count> tasks (<IDs>)`, then the blocked requirements' `Blocked by` IDs. Never paste the whole file.
- Chat only: the tasks themselves, in the file template's order, without the title block and without Revision History. The reply's first line is `## 1. Overview` and it ends with the last task or blocked entry. No preamble, no closing note, no account of how you worked.
- Stopped, or asking: only the stop line or the questions.

## Saving to a file

Find the plan, in this order:

1. A plan the user pasted into the conversation. Task from it even when it names a path that does not exist on disk.
2. A path the user named.
3. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. Use `<spec_output_dir>/<feature-name>/plan.md`. If the user names no feature, list the existing `<spec_output_dir>/*/plan.md` files and ask which one; if only one exists, use it.
4. None of these: ask for the path.

Write `tasks.md` in the same folder as `plan.md`, and only when that `plan.md` exists on disk and was found through a path the user named or through `spec_output_dir`. Otherwise, or when the user asks for chat only, reply in chat only.

Limits come from the same config files, or from a limit the user states: `tasks_max_files_per_task` (default 3) and `tasks_max_per_phase` (default 12).

If `tasks.md` already exists, update it as the template says. If it exists but does not follow the template, change nothing yet: say so and ask before rewriting it.

After writing, state the path in one line.
