---
name: implement-task
description: Implement one task from a saved task list (tasks.md from write-tasks), the one the user names (T-1.2) or the next Todo task whose dependencies are Done. Reads the task's plan phase, its requirements, and the code first; changes only the task's files; runs its Done when check, the test suite, and the project's lint and format checks; then sets its Status to Done and commits it on the feature branch. Never pushes, never changes the requirements, the plan, or other tasks, and stops with one line when the task cannot be done as written. Use when the user asks to implement, build, do, start, or continue a task, the next task, or a T- ID, even when the skill is not named. Load it before looking for tasks.md, because it says what to reply when the file does not exist. Not for writing requirements, the plan, or the task list, or for code changes that have no tasks.md.
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
2. **A stop line**, word for word, and nothing else: the line [scripts/pick_task.py](scripts/pick_task.py) prints after `stop`, or one of those in [references/implement-rules.md](references/implement-rules.md#stop-lines).
3. **The questions**, when the task leaves a choice that the code, the task, the plan, and the requirements do not decide, or the lookup's one question when it cannot tell which `tasks.md` to use.

The reply is only that: no preface, no reason before a stop line, no summary or next steps after it, and no code fence or backticks around it. Write no text between tool calls.

The last message you write is the reply. It starts with `T-` for a done report or with the stop line's own first word, never with a sentence about what you found ("FR-004 is blocked by Q-001. Per the rules, this is a stop.").

## Before starting

- Read [references/implement-rules.md](references/implement-rules.md) in full before changing anything: picking the task, scope, tests, git, stop lines, and the validation checklist. This file is authoritative.
- Read [references/examples.md](references/examples.md) before your first reply in a conversation.
- Only when you cannot run `pick_task.py` (you cannot run commands, or the user pasted the task list), also read [references/without-commands.md](references/without-commands.md): how to do by hand what the script does.

## Scope

This skill implements the task it picked and nothing else. It does not write or change requirements, the plan, or other tasks, and it never answers an open question; those belong to `write-spec`, `write-plan`, and `write-tasks`. Never invent a requirement or a behaviour the task, plan, and requirements do not state.

## Workflow

Work silently: do not say what you found, which rule applies, or why you stop. A stop line is the whole reply, even when the reason is obvious from the file.

1. **Find `tasks.md`, check the working tree, and pick the task**, as [Finding the files](#finding-the-files) says: one script does all three, and prints the stop line when there is one.
2. **Read the context:** the task's phase in `plan.md` (scope, interface and data changes, Verify) and each requirement in its Covers in `requirements.md`.
3. **Explore the code:** the task's Files, the tests beside them, how tests are run, and the patterns nearby. Then run the test command and the check commands once, before editing anything: tests or checks that cannot run because a service or tool they need is not available are the missing-service stop line, as the rules' test section says. Never start one yourself.
4. **Implement** within the task's Files, test included, as the rules' scope and test sections say.
5. **Run the check** in Done when, then the full test suite, then the check commands (the project's lint, format, and type checks), as the rules' test section says.
6. **Validate** against the rules' checklist.
7. **Set Status to `Done`** in `tasks.md`, **commit** as the rules' git section says (the spec files first, if they were not committed yet), remove the untracked files your commands left behind, as that section says, and reply with the done report.

## Finding the files

A task list the user pasted into the conversation needs no file: pick the task from it by hand and implement it, but there is no Status to set; the done report's last line still names the commit.

Otherwise run [scripts/pick_task.py](scripts/pick_task.py) by its full path, with the project as the current directory, before any other command. It finds `tasks.md`, checks the working tree, and picks the task, which is step 1 of the workflow. Give it:

- `--feature <name>` when the user names a feature, or `--path <path>` when they name a path to `tasks.md`; neither when they name neither.
- `--task <T-id>` when the user names a task, or `--requirement <ID>` when they ask for an FR or NFR in place of a task; neither for the next task.

Do what it prints:

- `found <path>` and, on the next line, `task <T-id>`: that is `tasks.md` and the task to implement. Use them and no other. `task <T-id> rework` means the task is a rework, as the rules say.
- `stop <line>`: `<line>` is your whole reply. Run nothing more and change nothing.
- `ask <question>`: `<question>` is your whole reply, as written. The one exception is `ask Where is tasks.md?`: when a path from earlier in this conversation gives the feature's folder, as the next paragraph says, run the script once more with `--path` to the `tasks.md` in that folder, and do what it prints. Never answer a question yourself in any other way.

**Without `spec_output_dir`:** A path to the feature's `requirements.md`, `plan.md`, or `tasks.md` that appears earlier in this conversation, named by the user or reported saved by a skill of this chain, gives the feature's folder, since the three files live together: use it when the file you need is in that folder and the user names no other feature. Otherwise ask for the path, and the question is your whole reply. Never search the project for the file or use a path you chose yourself.

`plan.md` and `requirements.md` are in the same folder as `tasks.md`. When one is missing, work from the task alone.
