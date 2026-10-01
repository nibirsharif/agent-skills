## 1. Approach

There is no existing code in this folder, so the feature is planned from the requirements alone: a reset endpoint that creates a token and emails a reset link, and an expiry check when the link is opened. One phase delivers everything that is written. Rate limiting waits on open questions and is not planned.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Reset link email and expiry | FR-001, FR-002, NFR-001 |

## 2. Phases

### Phase 1: Reset link email and expiry

**Scope:** Send the reset link to a registered user and reject a link that is older than 15 minutes. Rate limiting is not part of this phase.

**Requirements:** FR-001, FR-002, NFR-001

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- A reset-request endpoint that accepts an email address
- A reset-token store with the time each reset link was sent

**Verify:**

- FR-001: integration test that a reset request for a registered user sends one email with a reset link to the registered address
- FR-002: unit test that a link opened 15 minutes and 1 second after it was sent is rejected, and one opened at 14 minutes is accepted
- NFR-001: load test that 99% of reset emails are sent within 2 minutes of receiving the request

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001, Q-002: rate limiting of password-reset requests

## 4. Open Questions

Q-001: What does the reset rate limit count per: account, IP address, or both? (touches the blocked rate-limit requirement)

Q-002: How many reset requests are allowed in how long a period? (touches the blocked rate-limit requirement)
