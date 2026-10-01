# Examples

The repository in these examples is made up. In your work, name only files you have read.

## Missing requirements

User: `Plan the invoice-export feature.` No `requirements.md` exists for it.

```
No requirements file found at docs/specs/invoice-export/requirements.md. Run write-spec first to write the requirements.
```

Nothing else: no plan from the feature name.

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

Both questions are about one requirement, so they share one `Blocked by` entry. The topic comes from the questions: the `Pending:` line names only their IDs.

## An open question changes the core approach

A requirements file for an audit log ends its functional section with `Pending: Q-001.`, and `Q-001` asks whether each tenant's audit log is stored in a separate database or in one shared database. The answer changes the data model, so ask and plan nothing:

```
Q-001 decides the data model, so no plan can be written yet: Is each tenant's audit log stored in a separate database or in one shared database? Record the answer with write-spec, then run write-plan again.
```

## Splitting into phases

Nineteen requirements, limit 8 per phase: group by flow, not by layer.

- Wrong: Phase 1 database, Phase 2 API, Phase 3 UI. No phase leaves the product working.
- Right: Phase 1 return requests and their rejection rules; Phase 2 labels and warehouse intake; Phase 3 refunds; Phase 4 status pages; each merges on its own.

An `NFR` goes with the `FR` it constrains: the 5-minute email deadline sits in the same phase as the requirement that sends the email. A monthly availability target can move to a last phase, and says why:

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

The file holds the template filled in:

```markdown
# Implementation Plan: Password Reset

**Version:** 1.0
**Date:** 2026-03-03
**Requirements:** requirements.md, version 1.1
**Status:** Draft

## 1. Approach

Extend the existing authentication module: the reset-link email reuses the mailer, and the link expiry check sits beside the token validation. One phase delivers everything that is written.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Reset link email and expiry | FR-001, FR-002, NFR-001 |

## 2. Phases

### Phase 1: Reset link email and expiry

(as above)

## 3. Blocked Requirements

Blocked by Q-001, Q-002: rate limiting of password-reset requests

## 4. Open Questions

Q-001: What does the reset rate limit count per: account, IP address, or both? (touches the blocked rate-limit requirement)

Q-002: How many reset requests are allowed in how long a period? (touches the blocked rate-limit requirement)

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial plan from requirements.md 1.1 |
```

After the user answers with write-spec and `FR-005` is written, run the skill again: it asks whether Phase 1 has merged; told that it has, it adds `Phase 2: Rate limiting` with `FR-005`, removes the blocked entry, raises the version to 1.1, and adds a Revision History row.
