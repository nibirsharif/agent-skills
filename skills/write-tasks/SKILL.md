---
name: write-tasks
description: Break each phase of a saved implementation plan (plan.md from write-plan) into small, ordered, verifiable tasks and save them as tasks.md next to the plan. Explores the codebase first; every task names the requirement IDs it covers, the files it touches, the tasks it depends on, and a check that shows it is done. Blocked requirements and open questions are never tasked. Not for writing requirements, the plan itself, or code.
disable-model-invocation: true
---

# Write Tasks

Turn a feature's `plan.md` into `tasks.md`: each phase split into small tasks, in build order, each with a check that says when it is done. Read the code first; task only what the plan covers.

## Reply contract

Your reply is one of three things, and its first character is the first character of that thing:

1. **The tasks.**
   - Saved: the path in one line, then one line per phase, `Phase <n>: <count> tasks (<IDs>)`, then the blocked requirements' `Blocked by` IDs. Never paste the whole file.
   - Chat only: the tasks themselves, in the file template's order, without the title block and without Revision History. The first line is `## 1. Overview`, which says when there is no codebase or no file on disk, and the last is the last task or blocked entry. When the plan was pasted and the user did not ask for chat only, one more line ends it: exactly `Not saved: the plan was pasted, not read from a file. Name a folder to save tasks.md in.` No preamble, no closing note, no account of how you worked.
2. **A stop line**, when the plan cannot be tasked, and nothing else. Use exactly:
   - plan file missing or without a phase: `No plan file found at <path>. Run write-plan first to write the plan, then run write-tasks again.`
   - plan and requirements disagree: one line naming the ID and the conflict, then `Fix it with write-plan or write-spec, then run write-tasks again.`
   - a phase needs more tasks than the limit: `Phase <n> needs more than <limit> tasks. Split it in plan.md with write-plan, then run write-tasks again.`
3. **The questions**, and nothing else, when a phase is too vague to break into tasks without a guess. When no path to the plan is known, reply exactly: `Where is plan.md? Give its path, set `spec_output_dir` in `.agent-skills-config.yaml`, or paste the plan.`

## Before writing

- Read [references/task-rules.md](references/task-rules.md) in full before producing anything. It is authoritative.
- Before writing a file, read [references/tasks-template.md](references/tasks-template.md).
- Read [references/examples.md](references/examples.md) before your first reply in a conversation, and again when unsure of a task split or a saved file.

## Scope

This skill writes the task list only: no requirements, no change to the plan, no code. Never invent a requirement, a file, or a utility. A task names only what the plan states and what you found in the code. Never answer, close, or assume an open question; answering belongs to `write-spec`.

## Workflow

Work silently. Write no text between tool calls and none before the reply.

1. **Find and read the plan**, as [Saving to a file](#saving-to-a-file) says, and the `requirements.md` beside it when it exists. A path comes only from the request, the conversation, or the two config files: until one of them gives it, run no `ls`, `find`, or Glob over the project, and open no file in it but `.agent-skills-config.yaml`. With no path from them, reply with the location question, even with a `plan.md` in plain sight: the reply's first word is `Where`. A missing plan, or one without a phase, is the stop line. If a `tasks.md` already exists beside the plan, read it: you are updating it, as [references/updating.md](references/updating.md) says.
2. **Check the plan against the requirements.** A phase ID that is withdrawn or not written there is the stop line.
3. **Explore the codebase** as the rules' "Exploring the code" section says.
4. **Split each phase into tasks** as the rules say. List a phase's tasks and count them against the limit before writing any: a count over the limit is the stop line, not a reason to merge tasks.
5. **Validate** against the rules' checklist. Fix what fails; a check you cannot pass is a question, not a task.
6. **Reply** as the [Reply contract](#reply-contract) says, and save as [Saving to a file](#saving-to-a-file) says.

## Saving to a file

Find the plan, in this order:

1. A plan the user pasted into the conversation. Task from it even when it names a path that does not exist on disk.
2. A path the user names in this request.
3. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. Use `<spec_output_dir>/<feature-name>/plan.md`. If the user names no feature, list the existing `<spec_output_dir>/*/plan.md` files and ask which one; if only one exists, use it.
4. None of these: A path to the feature's `requirements.md`, `plan.md`, or `tasks.md` that appears earlier in this conversation, named by the user or reported saved by a skill of this chain, gives the feature's folder, since the three files live together: use it when the file you need is in that folder and the user names no other feature. Otherwise ask for the path, and the question is your whole reply. Never search the project for the file or use a path you chose yourself.

Write `tasks.md` in the same folder as `plan.md` whenever the plan was read from a file, whichever step found it. Reply in chat only when the plan was pasted or the user asks for chat only.

Limits come from the same config files, or from a limit the user states: `tasks_max_files_per_task` (default 3) and `tasks_max_per_phase` (default 12).

If the `tasks.md` that exists does not follow the template, change nothing yet: say so and ask before rewriting it.
