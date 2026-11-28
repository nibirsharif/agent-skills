# Examples

The code in these examples is made up. In your work, name only files you have read.

## One phase (chat only)

The password-reset plan has one phase with `FR-001`, `FR-002`, `NFR-001`, and there is no codebase.

```
## 1. Overview

There is no codebase in this folder, so every file is new. The token store comes first, then expiry, then the email with its deadline, then the phase check.

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.4 | FR-001, FR-002, NFR-001 |

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

#### T-1.3: Email the reset link within its deadline

**Covers:** FR-001, NFR-001

**Files:** new: `POST /auth/password-reset` handler with its mail call, new: integration test, new: load test script

**Depends on:** T-1.1

**Done when:** FR-001: integration test that a reset request for a registered user sends one email containing a link; NFR-001: load test run shows 99% of reset emails sent within 2 minutes of the request

**Status:** Todo

#### T-1.4: Verify the phase

**Covers:** FR-001, FR-002, NFR-001

**Files:** None.

**Depends on:** T-1.2, T-1.3

**Done when:** FR-001: T-1.1 and T-1.3 tests pass; FR-002: T-1.2 test passes; NFR-001: T-1.3 load test passes; the full test suite is green

**Status:** Todo

## 3. Blocked Requirements

None.
```

## Splitting a task

- Too big: `T-1.3: Build password reset` with six files. Split by behaviour: token store, expiry, email.
- Too small: `Email the reset link` and `Measure the email deadline` as two tasks. `NFR-001` is a threshold on `FR-001`'s response, and the files fit: one task, with a check for each ID. `FR-002` stays apart: opening a link is another event.
- Layers: `T-1.1 Add database`, `T-1.2 Add API`, `T-1.3 Add UI`. Each task should leave the product working; split by behaviour.

## An interface item no Verify line names

The plan's phase lists, under Interface and data changes, an `export_path(report_id)` helper that builds a report's file path from `EXPORT_DIR` and `EXPORT_PREFIX`. `FR-001` writes the export and `FR-002` downloads it; their Verify lines test the two commands and never name the helper.

```
#### T-1.1: Add the export path helper

**Covers:** FR-001, FR-002

**Files:** new: `export_path` helper, new: its unit test

**Depends on:** None.

**Done when:** FR-001: unit test that `export_path` joins `EXPORT_DIR`, `EXPORT_PREFIX`, and the report ID; FR-002: unit test that `export_path` gives the same path for the same report ID on every call

**Status:** Todo
```

The export and download tasks then depend on `T-1.1` and call the helper.

- Wrong: no task names the helper, and the export task builds the path inside the export command. The download task then has to copy the rule.

## A manual check

The project has unit tests and no browser test runner. `FR-003` says the reset page shows "This link has expired" for an expired link. The page's handler can be tested; what the browser shows cannot.

```
**Done when:** FR-003: manual: in a browser, open a reset link older than 15 minutes: the page shows "This link has expired"
```

- Wrong: `FR-003: the page shows the expired message`. A person must check it, and the word is missing.
- Wrong: `FR-002: manual: check that an expired token is rejected`. A unit test can do that.
- Wrong: `FR-003: Playwright test that ...` when neither the plan nor the code has Playwright.

## A plan that cannot be tasked

The plan lists `FR-003`, and `requirements.md` has `FR-003: Withdrawn.`. Reply with the stop line only, and task nothing:

```
plan.md plans FR-003, which requirements.md withdraws. Fix it with write-plan or write-spec, then run write-tasks again.
```

## A saved file

With `spec_output_dir: docs/specs`, the file is `docs/specs/password-reset/tasks.md` and the reply is:

```
Saved docs/specs/password-reset/tasks.md.
Phase 1: 4 tasks (FR-001, FR-002, NFR-001)
Blocked: Q-001, Q-002 (rate limiting)
```

The file is the template filled in, with the Overview, phases, and Blocked section above, `**Plan:** plan.md, version 1.0`, and one Revision History row: `1.0 | 2026-03-03 | Initial tasks from plan.md 1.0`.
