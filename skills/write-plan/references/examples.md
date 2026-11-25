# Examples

The repository in these examples is made up. In your work, name only files you have read.

## Blocked requirements (chat only)

The password-reset requirements have `FR-001`, `FR-002`, `NFR-001`, and open questions `Q-001` and `Q-002` about rate limiting. Section 3 ends with `Pending: Q-001, Q-002.` The rate-limit requirement is not written yet, so it gets no phase.

```
## 1. Approach

Extend the existing authentication module: the reset-link email reuses the mailer, and the link expiry check sits beside the token validation. One phase delivers everything that is written.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Reset link email and expiry | FR-001, FR-002, NFR-001 |

## 2. Phases

### Phase 1: Reset link email and expiry

**Scope:** Send the reset link and reject an expired link. Rate limiting waits on open questions.

**Requirements:** FR-001, FR-002, NFR-001

**Size:** about 6 files

**Reuse:**

- `src/auth/tokens.ts`: create and validate the reset token
- `src/mail/mailer.ts`: send the reset email

**Interface and data changes:**

- `POST /auth/password-reset` accepts an email address
- `password_reset_tokens` table with a `sent_at` column

**Verify:**

- FR-001: integration test that a reset request for a registered user sends one email with a link
- FR-002: unit test that a link opened 15 minutes and 1 second after `sent_at` is rejected
- NFR-001: load test that 99% of emails are sent within 2 minutes of the request

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001, Q-002: rate limiting of password-reset requests

## 4. Open Questions

Q-001: What does the reset rate limit count per: account, IP address, or both? (touches the blocked rate-limit requirement)

Q-002: How many reset requests are allowed in how long a period? (touches the blocked rate-limit requirement)
```

Both questions are about one requirement, so they share one `Blocked by` entry.

## An open question changes the core approach

A requirements file for an audit log ends its functional section with `Pending: Q-001.`, and `Q-001` asks whether each tenant's audit log is stored in a separate database or in one shared database. The answer changes the data model, so ask and plan nothing:

```
Q-001 decides the data model, so no plan can be written yet: Is each tenant's audit log stored in a separate database or in one shared database? Record the answer with write-spec, then run write-plan again.
```

## A requirement too large for one phase

`FR-001` copies the records of 14 legacy modules, each in its own record format. That is at least 14 files, over the limit of 10, and a requirement cannot be spread over phases:

```
FR-001 needs more than 10 files on its own. Split it with write-spec, then run write-plan again.
```

Wrong: phases that list `**Requirements:** None (part of FR-001)`, or one phase of `about 28 files`.

## Splitting into phases

The password-reset plan above is right as one phase of 3 requirements, and wrong as a phase per requirement.

Nineteen requirements, limit 8 per phase: cut by flow, not by layer.

- Wrong: Phase 1 database, Phase 2 API, Phase 3 UI. No phase leaves the product working.
- Right: Phase 1 return requests and their rejection rules; Phase 2 labels and warehouse intake; Phase 3 refunds and status pages; each merges on its own.

The 5-minute email deadline sits in the phase of the requirement that sends the email. A monthly availability target can move to a last phase, and says why:

```
**Scope:** Meet the availability target. It needs monitoring and failover, which change no behaviour, so it follows the phases that build the behaviour.
```

## A saved file

The blocked-requirements plan above, saved with `spec_output_dir: docs/specs`. The file is `docs/specs/password-reset/plan.md`, and the reply is:

```
Saved docs/specs/password-reset/plan.md.
Phase 1: Reset link email and expiry (FR-001, FR-002, NFR-001)
Blocked: Q-001, Q-002 (rate limiting)
```

The file is the template filled in: the title block (`# Implementation Plan: Password Reset`, `**Version:** 1.0`, the date, `**Requirements:** requirements.md, version 1.1`, `**Status:** Draft`), the four sections above, and `## 5. Revision History` with one row: `1.0 | 2026-03-03 | Initial plan from requirements.md 1.1`.
