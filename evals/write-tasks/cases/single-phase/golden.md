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

#### T-1.2: Reject an expired reset link

**Covers:** FR-002

**Files:** new: token validation in the token module, new: its unit test

**Depends on:** T-1.1

**Done when:** FR-002: unit test that a token checked 15 minutes and 1 second after `sent_at` is rejected, and one checked at 14 minutes 59 seconds is accepted

#### T-1.3: Email the reset link

**Covers:** FR-001

**Files:** new: `POST /auth/password-reset` handler, new: mail call, new: integration test

**Depends on:** T-1.1

**Done when:** FR-001: integration test that a reset request for a registered user sends one email containing a link

#### T-1.4: Measure the email deadline

**Covers:** NFR-001

**Files:** new: load test script

**Depends on:** T-1.3

**Done when:** NFR-001: load test run shows 99% of reset emails sent within 2 minutes of the request

#### T-1.5: Verify the phase

**Covers:** FR-001, FR-002, NFR-001

**Files:** None.

**Depends on:** T-1.2, T-1.4

**Done when:** FR-001: T-1.1 and T-1.3 tests pass; FR-002: T-1.2 test passes; NFR-001: T-1.4 load test passes; the full test suite is green

## 3. Blocked Requirements

None.
