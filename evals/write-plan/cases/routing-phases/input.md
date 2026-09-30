We have the requirements for our password reset feature saved below. How should we build it in reviewable steps, one PR each? There is no codebase yet.

```markdown
# Requirements Specification: Password Reset

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

A registered user can reset a password through a reset link sent by email. Reset requests are rate limited.

## 2. Scope

### In Scope

- Password reset through an emailed reset link

### Out of Scope

None given.

**Systems:** authentication service

## 3. Functional Requirements

REQ-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address. <!-- Source: "When a registered user requests a password reset, the authentication service emails a reset link to their registered address." -->

REQ-002: If a user opens a reset link more than 15 minutes after the reset link was sent, then the authentication service shall reject the reset link. <!-- Source: "The link expires 15 minutes after it is sent." -->

Pending: Q-001, Q-002.

## 4. Non-Functional Requirements

NFR-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address within 2 minutes of receiving the request for 99% of requests. <!-- Source: "the reset email must go out within 2 minutes of the request for 99% of requests" -->

## 5. Open Questions

Q-001: What does the reset rate limit count per: account, IP address, or both? <!-- Source: "Reset requests should be rate limited." -->

Q-002: How many reset requests are allowed in how long a period? <!-- Source: "Reset requests should be rate limited." -->

Q-003: Closed. Answer: send no email for an unregistered address. <!-- Source: coverage gap in REQ-001 -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
