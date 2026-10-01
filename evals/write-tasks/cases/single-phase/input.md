Break the password-reset plan into tasks. There is no codebase in this folder, and the plan is not on disk; this is docs/specs/password-reset/plan.md:

```markdown
# Implementation Plan: Password Reset

**Version:** 1.0
**Date:** 2026-03-03
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

There is no codebase in this folder. One phase delivers everything that is written.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Reset link email and expiry | FR-001, FR-002, NFR-001 |

## 2. Phases

### Phase 1: Reset link email and expiry

**Scope:** Send the reset link and reject an expired link.

**Requirements:** FR-001, FR-002, NFR-001

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- `POST /auth/password-reset` accepts an email address
- `password_reset_tokens` table with a `sent_at` column

**Verify:**

- FR-001: integration test that a reset request for a registered user sends one email with a link
- FR-002: unit test that a link opened 15 minutes and 1 second after `sent_at` is rejected
- NFR-001: load test that 99% of emails are sent within 2 minutes of the request

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
