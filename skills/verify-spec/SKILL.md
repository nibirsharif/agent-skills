---
name: verify-spec
description: Check whether the code meets a saved requirements file (requirements.md from write-spec), with one verdict per FR and NFR ID (met, partial, unmet, untested, cannot tell, or skipped), each backed by file:line and test evidence from running the project's tests. Can be limited to one phase of plan.md or one ID. Also lists changed files that no requirement covers. Read-only, so it never edits code, requirements, plan, or tasks, and never commits. Use when the user asks whether an implementation meets, satisfies, or matches the spec or requirements, whether a requirement or phase is really done, or to verify or audit code against requirements, even when the skill is not named. Load it before looking for requirements.md, because it says what to reply when the file does not exist. Not for writing requirements, the plan, tasks, or code, or for a general code review with no requirements file.
---

# Verify Spec

Check a feature's code against its `requirements.md` and report, requirement by requirement, whether it is met and how you know. One report per run; it changes nothing.

## Reply contract

Your reply is one of two things, and its first character is the first character of that thing:

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
2. **A stop line**, one of those in [references/verify-rules.md](references/verify-rules.md#stop-lines), word for word, and nothing else. When there is no `requirements.md`, which you find out before reading the rules, it is exactly: `No requirements file found at <path>. Run write-spec first, then run verify-spec again.` with `<path>` the `<spec_output_dir>/<feature>/requirements.md` you looked for.

The reply is only that: no preface, no summary or advice after it, no code fence around it, and no text before a stop line. Write no text between tool calls.

Narration is the usual mistake. These all break the contract when they come before the report or a stop line: "Clean working tree on main, so drift is not checked.", "Now I have everything needed for the report.", "The file only has FR-001 to FR-005.". Anything you want to say about scope, branch state, or a stop goes in an Evidence cell or the Drift line, or nowhere. A stop line is the whole reply: do not follow it with what you noticed in the code, and do not name the files you looked at.

The last message you write is the reply. It starts with `| ID` for a report or with the stop line's own first word, never with a sentence about what you found.

## Before starting

- Read [references/verify-rules.md](references/verify-rules.md) in full before checking anything: scope, the verdicts and how to choose between them, evidence, running tests, drift, stop lines, and the validation checklist. This file is authoritative.
- Read [references/examples.md](references/examples.md) before your first reply in a conversation.

## Scope

This skill reports and nothing else. It does not edit code, tests, or any spec file, does not commit, and does not say how to fix a gap; fixing belongs to `implement-task`, and requirements to `write-spec`. Never mark a requirement `met` without the code and a passing test in front of you, and never invent a requirement the file does not state.

## Workflow

Work silently: do not narrate what you found or which rule applies.

1. **Find `requirements.md`**, as [Finding the files](#finding-the-files) says. If it is missing, reply with the stop line and stop.
2. **Pick the scope:** the whole file, one phase from `plan.md`, or one ID, as the rules say. Mark blocked requirements `skipped`.
3. **Explore the code:** for each requirement in scope, find where its behaviour lives and the tests that drive it. Read the test bodies.
4. **Run the project's test command** once, as the rules say, and read the result per test.
5. **Decide each verdict** and write its evidence, taking the weaker verdict when unsure.
6. **Find drift:** run `git status --porcelain`, then take the uncommitted files, and the files changed on the feature branch if on one, that no requirement covers.
7. **Validate** against the rules' checklist, then reply with the report.

## Finding the files

Find the requirements, in this order:

1. Requirements the user pasted into the conversation: verify against exactly those, with no plan and so no phase scoping. Add nothing from a file, and do not compare them with one, even when a file has the same IDs.
2. A path the user named.
3. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. Use `<spec_output_dir>/<feature-name>/requirements.md`. If the user names no feature, list the existing `<spec_output_dir>/*/requirements.md` files; if only one exists, use it, otherwise ask which one.
4. None of these: ask for the path.

When the user names a feature (or a path) whose `requirements.md` does not exist, that is the no-requirements-file stop line for `<spec_output_dir>/<feature>/requirements.md`, even when other features exist. Never suggest or use another feature.

`plan.md` is in the same folder as `requirements.md`. It is optional: it supplies phase scoping and the list of blocked requirements. `tasks.md` is never read.
