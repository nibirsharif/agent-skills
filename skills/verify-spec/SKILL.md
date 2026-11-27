---
name: verify-spec
description: Check whether the code meets a saved requirements file (requirements.md from write-spec), with one verdict per FR and NFR ID (met, partial, unmet, untested, cannot tell, or skipped), each backed by file:line and test evidence from running the project's tests. Can be limited to one phase of plan.md or one ID. Also lists changed files that no requirement covers. Read-only, so it never edits code, requirements, plan, or tasks, and never commits. Use when the user asks whether an implementation meets, satisfies, or matches the spec or requirements, whether a requirement or phase is really done, or to verify or audit code against requirements, even when the skill is not named. Load it before looking for requirements.md, because it says what to reply when the file does not exist. Not for writing requirements, the plan, tasks, or code, or for a general code review with no requirements file.
---

# Verify Spec

Check a feature's code against its `requirements.md` and report, requirement by requirement, whether it is met and how you know. One report per run; it changes nothing.

## Reply contract

Your reply is one of three things, and its first character is the first character of that thing:

1. **The report**, exactly this shape, as plain text. The header and separator lines are written exactly as shown, there are no blank lines, and the first character of the reply is the `|` of the header:

   ```
   | ID | Verdict | Evidence |
   |----|---------|----------|
   | FR-001 | met | textstats/counts.py:17; tests/test_counts.py::test_x passed |
   | FR-002 | untested | <evidence> |
   Tests: <command>: <result>
   Tally: 1 met, 1 untested
   Drift: <path>, <path>
   ```

   - One row per requirement in scope, in file order.
   - The tests line is `Tests: <command>: <result>`, or `Tests: not run: <reason>`.
   - The tally lists only the verdicts that occur, in this order: met, partial, unmet, untested, cannot tell, skipped.
   - The drift line is `Drift: <paths>`, `Drift: none`, or `Drift: not checked (no feature branch)`.
2. **A stop line**, word for word, and nothing else: the line [scripts/check_scope.py](scripts/check_scope.py) prints after `stop`.
3. **The lookup's one question**, when it cannot tell which `requirements.md` to use, as [Finding the files](#finding-the-files) says, and nothing else.

The reply is only that: no preface, no summary or advice after it, and no code fence or backticks around it. Write no text between tool calls.

Narration is the usual mistake. These all break the contract when they come before the report or a stop line: "Clean working tree on main, so drift is not checked.", "Now I have everything needed for the report.", "The file only has FR-001 to FR-005.". Anything you want to say about scope or branch state goes in an Evidence cell or the Drift line, or nowhere. A stop line is the whole reply: nothing before it, and nothing after it about the code or the files you looked at.

The last message you write is the reply. It starts with `| ID` for a report or with the stop line's own first word, never with a sentence about what you found.

## Before starting

- Read [references/verify-rules.md](references/verify-rules.md) in full before checking anything: scope, the verdicts and how to choose between them, evidence, running tests, drift, and the validation checklist. This file is authoritative.
- Read [references/examples.md](references/examples.md) before your first reply in a conversation.
- Only when you cannot run commands, also read [references/without-commands.md](references/without-commands.md): how to do by hand what `check_scope.py` does.

## Scope

This skill reports and nothing else. It does not edit code, tests, or any spec file, does not commit, and does not say how to fix a gap; fixing belongs to `implement-task`, and requirements to `write-spec`. Never invent a requirement the file does not state.

## Workflow

Work silently: do not narrate what you found or which rule applies.

1. **Find `requirements.md` and the scope**, as [Finding the files](#finding-the-files) says: one script does both, and prints the stop line when there is one. Blocked requirements are `skipped`, as the rules say.
2. **Explore the code:** for each requirement in scope, find where its behaviour lives, every caller that reaches it, and the tests that drive it. Read the test bodies.
3. **Run the project's test command** once, as the rules say, and read the result per test.
4. **Decide each verdict** and write its evidence, taking the weaker verdict when unsure.
5. **Find drift**, as the rules say: run `git status --porcelain` every time.
6. **Validate** against the rules' checklist, then reply with the report.

## Finding the files

Requirements the user pasted into the conversation need no file: verify against exactly those, with no plan and so no phase scoping. Add nothing from a file, and do not compare them with one, even when a file has the same IDs.

Otherwise run [scripts/check_scope.py](scripts/check_scope.py) by its full path, with the project as the current directory, before any other command. It finds `requirements.md` and checks the scope, which is step 1 of the workflow. Give it:

- `--feature <name>` when the user names a feature, or `--path <path>` when they name a path to `requirements.md`; neither when they name neither.
- `--id <ID>` when the user names one requirement, or `--phase <n>` when they name a phase; neither for the whole file.

Do what it prints:

- `found <path>` and, on the next line, `scope <what>`: that is `requirements.md` and the scope, `all`, one ID, or `phase <n>:` with the IDs of that phase. Use them and no other.
- `stop <line>`: `<line>` is your whole reply. Run nothing more.
- `ask <question>`: `<question>` is your whole reply, as written. The one exception is `ask Where is requirements.md?`: when a path from earlier in this conversation gives the feature's folder, as the next paragraph says, run the script once more with `--path` to the `requirements.md` in that folder, and do what it prints. Never answer a question yourself in any other way.

**Without `spec_output_dir`:** A path to the feature's `requirements.md`, `plan.md`, or `tasks.md` that appears earlier in this conversation, named by the user or reported saved by a skill of this chain, gives the feature's folder, since the three files live together: use it when the file you need is in that folder and the user names no other feature. Otherwise ask for the path, and the question is your whole reply. Never search the project for the file or use a path you chose yourself.

`plan.md`, when the feature has one, is in the same folder as `requirements.md`.
