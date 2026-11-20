# Verify Rules

These rules are authoritative for `verify-spec`. A report is checked against the [checklist](#validation-checklist) before it is sent.

## Reading requirements.md

Requirements are the lines that start with an ID: `FR-<n>:` for functional and `NFR-<n>:` for non-functional ones. Each is one `shall` sentence in an EARS pattern. A requirement ending `Blocked by Q-<n>.` waits on an open question. Section 2 (Open Questions) lists the questions; they are not requirements and get no row. The `**Status:**` line under the title is not a verdict.

`plan.md`, when it is in the same folder, has phases (`### Phase <n>: <title>`), each with a `**Requirements:**` list, and a Blocked Requirements section. `tasks.md` is never read: a task's Status says what someone intended, not what the code does.

## Choosing the scope

Rows are in file order, whatever the scope: skipped rows stay where their requirement is, never grouped at the end.

- **No phase or ID named:** every requirement in `requirements.md`.
- **A phase named:** the IDs in that phase's `**Requirements:**` list in `plan.md`. Every other ID gets a `skipped` row with the evidence `outside phase <n>`.
- **An ID named** (`FR-003`): only that row.
- **Blocked:** a requirement marked `Blocked by Q-<n>`, or listed in the plan's Blocked Requirements, gets a `skipped` row with the evidence `Blocked by Q-<n>`, even when it is also outside the named phase. It is never checked and never judged `unmet`.

## Verdicts

Every row has exactly one of these:

| Verdict | Means |
|---------|-------|
| `met` | The code does what the statement says, and a test that drives its trigger and checks its response ran and passed. Both are cited. |
| `partial` | The code does part of it: a condition, value, or response in the statement is missing or wrong. The evidence says which part. |
| `unmet` | No implementation found after searching, or the test for it ran and failed. The evidence says which. |
| `untested` | The code does what the statement says, but no test exercises it, or the tests did not run. |
| `cannot tell` | The statement has no checkable criterion (an NFR with no threshold, "quickly", "user-friendly"). The evidence is `no criterion; clarify with write-spec`. |
| `skipped` | Blocked, or outside the named phase. |

Rules that decide between them:

- **`met` needs both halves.** Code alone is `untested`. A test alone is not enough either: cite the code the test exercises.
- **Read the test, not its name.** A test counts only if its body drives the statement's trigger and asserts its response. A test that passes without asserting the behaviour does not count.
- **Failure beats presence.** A test for the requirement that ran and failed makes the row `unmet`, with the failure as evidence.
- **An NFR with a threshold but no benchmark** (a stated limit and no test that measures it) is `untested`, not `cannot tell`.
- **When unsure between two verdicts, take the weaker one** (`partial` over `met`, `untested` over `met`). Never round up.
- **Never mark a row from** a commit message, a task Status, a comment saying "done", or the requirement's own wording.

## What to check in the sentence

Look for each part of the sentence, not only its verb:

- **While** `<state>`: the state is detected, and the behaviour holds only in it.
- **When** `<trigger>`: the trigger is handled and the response follows it.
- **Where** `<feature>`: the behaviour is present when the feature is, and absent when it is not.
- **If** `<condition>`, **then**: the unwanted condition is detected and the stated response happens.
- None of these: the behaviour holds on every call.

A value in the statement (200, 15 minutes, `TypeError`) is checked as written. A different value is `partial`.

## Evidence

- **Implementation:** `path:line`, the line where the behaviour is, from code you read this run.
- **Test:** `path::test_name`, and that it passed or failed in this run. Write them as `path:line; path::test_name passed`.
- **`unmet` with no code:** `no implementation found`, and what you searched (the name and the module). Search by what the code does, not only by the requirement's words.
- Every cited path and line exists. Never cite a file you did not open.

## Running the tests

- Run the project's test command once: `test_command` from `.agent-skills-config.yaml` in the project root, else `~/.agent-skills-config.yaml` when set, else the existing one (from its README, Makefile, package scripts, or CI config; else the language's standard runner). Use the same command in the `Tests:` line.
- Read results per test, not only the total, so each row can cite its own test.
- When the tests cannot run (no command found, the runner fails to start, a missing dependency), say `Tests: not run: <reason>`. No row is then `met`; rows that would have been are `untested`.
- A test that fails for a reason unrelated to the requirements (a broken fixture elsewhere) is not evidence for or against a row; say so in the `Tests:` line.

## Drift

A changed file is drift when it neither implements nor tests any requirement in `requirements.md` (all of them, not only the scoped ones), and is not a spec file. A file that implements or tests a requirement is not drift, whatever that requirement's verdict: a file whose change breaks FR-001 is the evidence for an `unmet` row, not drift.

- Run `git status --porcelain` every time. The branch name alone never decides drift: a change on the default branch still counts.
- The changed files are the uncommitted ones from `git status --porcelain`, plus, on a branch other than the default (`base_branch` from the same config files when set, else the branch `origin/HEAD` names, which `git symbolic-ref --short refs/remotes/origin/HEAD` prints as `origin/<name>`, else `main`, else `master`), `git diff --name-only <default>...HEAD`. Ignore the feature's spec folder.
- On the default branch with nothing uncommitted, or outside a git repository, there is nothing to compare: `Drift: not checked (no feature branch)`.
- Drift is reported, never judged: a file may be a legitimate refactor. List it and let the user decide.

## Never

- Edit, create, or delete any file, or commit, stage, push, stash, switch branches, or change any other state. This skill's tool use is reading, searching, running the tests, and read-only git commands (`status`, `diff`, `log`, `branch`).
- Run anything but the test runner and read-only inspection: no installs, no builds that write outside the project's usual build output, no scripts that change data, no network calls.
- Answer an open question, or say how to fix a gap. A row says what is missing; fixing it is `implement-task` or `write-spec`.

## Validation checklist

Run every item before replying.

1. Every requirement in scope has exactly one row, in file order; every blocked or out-of-phase one is `skipped`.
2. Every `met` row cites an implementation line and a test that ran and passed in this run. Where two verdicts fit, the weaker one is used.
3. Every cited path and line exists, and you opened it.
4. A `Tests:` line names the command and its result, or why the tests did not run.
5. `Tally:` counts match the rows; `Drift:` lists paths or says why it was not checked.
6. Nothing was edited, created, staged, or committed.
