Break the password-reset plan into tasks. There is no codebase in this folder, and the plan is not on disk; this is docs/specs/password-reset/plan.md:

```markdown
# Implementation Plan: Password Reset

**Version:** 1.0
**Date:** 2026-03-03
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

There is no codebase in this folder. Phase 1 sends the link; Phase 2 accepts the new password.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Reset link email and expiry | REQ-001, REQ-002, NFR-001 |
| 2 | Set a new password | REQ-003, REQ-004 |

## 2. Phases

### Phase 1: Reset link email and expiry

**Scope:** Send the reset link and reject an expired link.

**Requirements:** REQ-001, REQ-002, NFR-001

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- `POST /auth/password-reset` accepts an email address
- `password_reset_tokens` table with a `sent_at` column

**Verify:**

- REQ-001: integration test that a reset request for a registered user sends one email with a link
- REQ-002: unit test that a link opened 15 minutes and 1 second after `sent_at` is rejected
- NFR-001: load test that 99% of emails are sent within 2 minutes of the request

**Open questions:** None.

### Phase 2: Set a new password

**Scope:** Accept a new password through a valid reset link. Builds on the tokens from Phase 1.

**Requirements:** REQ-003, REQ-004

**Size:** about 4 files

**Reuse:** None found.

**Interface and data changes:**

- `POST /auth/password-reset/confirm` accepts a reset token and a new password

**Verify:**

- REQ-003: integration test that a valid token and a new password update the password and the token cannot be used again
- REQ-004: unit test that a password of 11 characters is rejected and one of 12 is accepted

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial plan from requirements.md 1.0 |
```
