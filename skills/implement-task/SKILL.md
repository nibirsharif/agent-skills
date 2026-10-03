---
name: implement-task
description: Implement one task from a saved task list (tasks.md from write-tasks), the one the user names (T-1.2) or the next Todo task whose dependencies are Done. Reads the task's plan phase, its requirements, and the code first; changes only the task's files; runs its Done when check and the test suite; then sets its Status to Done and commits it on the feature branch. Never pushes, never changes the requirements, the plan, or other tasks, and stops with one line when the task cannot be done as written. Use when the user asks to implement, build, do, start, or continue a task, the next task, or a T- ID, even when the skill is not named. Load it before looking for tasks.md, because it says what to reply when the file does not exist. Not for writing requirements, the plan, or the task list, or for code changes that have no tasks.md.
---

# Implement Task

Implement one task of a feature's `tasks.md`, prove it with its check, mark it `Done`, and commit it. One task per run; the next run picks the next task.

## Reply contract

Your reply is one of three things, and its first character is the first character of that thing:

1. **The done report**, exactly these five lines and nothing else, as plain text:
   - `T-<p>.<n> done: <task title>`
   - `Covers: <IDs>`
   - `Changed: <path>, <path>`
   - `Check: <command>: <result>`
   - `Commit: <short hash> on <branch>`
2. **A stop line**, one of those in [references/implement-rules.md](references/implement-rules.md#stop-lines), word for word, and nothing else. When there is no `tasks.md`, which you find out before reading the rules, it is exactly: `No tasks file found at <path>. Run write-tasks first, then run implement-task again.` with `<path>` the `<spec_output_dir>/<feature>/tasks.md` you looked for.
3. **The questions**, when the task leaves a choice that the code, the task, the plan, and the requirements do not decide.

The reply is only that: no preface, no reason before a stop line, no summary or next steps after it, and no code fence or backticks around it. Write no text between tool calls.

The last message you write is the reply. It starts with `T-` for a done report or with the stop line's own first word, never with a sentence about what you found ("FR-004 is blocked by Q-001. Per the rules, this is a stop.").

## Before starting

- Read [references/implement-rules.md](references/implement-rules.md) in full before changing anything: picking the task, scope, tests, git, stop lines, and the validation checklist. This file is authoritative.
- Read [references/examples.md](references/examples.md) before your first reply in a conversation.

## Scope

This skill implements the task it picked and nothing else. It does not write or change requirements, the plan, or other tasks, and it never answers an open question; those belong to `write-spec`, `write-plan`, and `write-tasks`. Never invent a requirement or a behaviour the task, plan, and requirements do not state.

## Workflow

Work silently: do not say what you found, which rule applies, or why you stop. A stop line is the whole reply, even when the reason is obvious from the file.

1. **Find `tasks.md`**, as [Finding the files](#finding-the-files) says. If it is missing, reply with the stop line and stop.
2. **Check the working tree**: only the feature's own spec files may be uncommitted, as the rules' git section says.
3. **Pick the task** as the rules say, and check its dependencies are `Done`.
4. **Read the context:** the task's phase in `plan.md` (scope, interface and data changes, Verify) and each requirement in its Covers in `requirements.md`.
5. **Explore the code:** the task's Files, the tests beside them, how tests are run, and the patterns nearby.
6. **Implement** within the task's Files, test included, as the rules' scope and test sections say.
7. **Run the check** in Done when, then the full test suite. A failure you cannot fix within the task is the failed-check stop line.
8. **Validate** against the rules' checklist.
9. **Set Status to `Done`** in `tasks.md`, **commit** as the rules' git section says (the spec files first, if they were not committed yet), and reply with the done report.

## Finding the files

Find `tasks.md`, in this order:

1. A path the user named.
2. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. Use `<spec_output_dir>/<feature-name>/tasks.md`. If the user names no feature, list the existing `<spec_output_dir>/*/tasks.md` files; if only one exists, use it, otherwise ask which one.
3. A task list the user pasted into the conversation: implement from it, but there is no Status to set; the done report's last line still names the commit.
4. None of these: ask for the path.

When the user names a feature (or a path) whose `tasks.md` does not exist, that is the no-tasks-file stop line for `<spec_output_dir>/<feature>/tasks.md`, even when other features exist. Never suggest or use another feature.

`plan.md` and `requirements.md` are in the same folder as `tasks.md`. When one is missing, work from the task alone.
