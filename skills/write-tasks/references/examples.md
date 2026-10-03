# Examples

The code in these examples is made up. In your work, name only files you have read.

## Missing plan

User: `Break the invoice-export plan into tasks.` No `plan.md` exists for it.

```
No plan file found at docs/specs/invoice-export/plan.md. Run write-plan first to write the plan, then run write-tasks again.
```

Nothing else: no tasks from the feature name.

## One phase (chat only)

The password-reset plan has one phase with `FR-001`, `FR-002`, `NFR-001`, and there is no codebase.

```
## 1. Overview

There is no codebase in this folder, so every file is new. The token store comes first, then expiry, then the email and its deadline, then the phase check.

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.5 | FR-001, FR-002, NFR-001 |

## 2. Tasks

### Phase 1: Reset link email and expiry

#### T-1.1: Add the reset token store

**Covers:** FR-001

**Files:** new: migration for the `password_reset_tokens` table with `sent_at`, new: token module that creates a token, new: its unit test

**Depends on:** None.

**Done when:** FR-001: unit test that creating a token for a registered user stores a row with `sent_at` set

**Status:** Todo

#### T-1.2: Reject an expired reset link

**Covers:** FR-002

**Files:** new: token validation in the token module, new: its unit test

**Depends on:** T-1.1

**Done when:** FR-002: unit test that a token checked 15 minutes and 1 second after `sent_at` is rejected, and one checked at 14 minutes 59 seconds is accepted

**Status:** Todo

#### T-1.3: Email the reset link

**Covers:** FR-001

**Files:** new: `POST /auth/password-reset` handler, new: mail call, new: integration test

**Depends on:** T-1.1

**Done when:** FR-001: integration test that a reset request for a registered user sends one email containing a link

**Status:** Todo

#### T-1.4: Measure the email deadline

**Covers:** NFR-001

**Files:** new: load test script

**Depends on:** T-1.3

**Done when:** NFR-001: load test run shows 99% of reset emails sent within 2 minutes of the request

**Status:** Todo

#### T-1.5: Verify the phase

**Covers:** FR-001, FR-002, NFR-001

**Files:** None.

**Depends on:** T-1.2, T-1.4

**Done when:** FR-001: T-1.1 and T-1.3 tests pass; FR-002: T-1.2 test passes; NFR-001: T-1.4 load test passes; the full test suite is green

**Status:** Todo

## 3. Blocked Requirements

None.
```

## Splitting a task

- Too big: `T-1.3: Build password reset` with six files. Split by behaviour: token store, expiry, email, deadline.
- No check: `Done when: FR-002: it works`. Name the test and the inputs.
- Tests left to the end: tasks 1 to 4 add code, task 5 "add tests". Each task carries its own check.
- Out of order: `T-1.2` depends on `T-1.4`. Reorder so the dependency comes first.
- Layers: `T-1.1 Add database`, `T-1.2 Add API`, `T-1.3 Add UI`. Each task should leave the product working; split by behaviour.

## A plan that cannot be tasked

The plan lists `FR-003`, and `requirements.md` has `FR-003: Withdrawn.`. Reply with the stop line only:

```
plan.md plans FR-003, which requirements.md withdraws. Fix it with write-plan or write-spec, then run write-tasks again.
```

A phase that needs 14 tasks when the limit is 12:

```
Phase 2 needs more than 12 tasks. Split it in plan.md with write-plan, then run write-tasks again.
```

## A saved file

With `spec_output_dir: docs/specs`, the file is `docs/specs/password-reset/tasks.md` and the reply is:

```
Saved docs/specs/password-reset/tasks.md.
Phase 1: 5 tasks (FR-001, FR-002, NFR-001)
Blocked: Q-001, Q-002 (rate limiting)
```

The file is the template filled in, with the Overview, phases, and Blocked section above, `**Plan:** plan.md, version 1.0`, and one Revision History row: `1.0 | 2026-03-03 | Initial tasks from plan.md 1.0`.

After `write-plan` adds Phase 2 for rate limiting, run the skill again: it reads which phases have started from their Status lines, appends `Phase 2`, removes the blocked entry, raises the version to 1.1, and adds a Revision History row.
