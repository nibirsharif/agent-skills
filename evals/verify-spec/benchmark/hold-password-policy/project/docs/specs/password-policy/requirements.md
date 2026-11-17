# Requirements: Password Policy

**Version:** 1.0
**Date:** 2026-10-26
**Status:** Draft

## 1. Functional Requirements

FR-001: If a user chooses a password with fewer than 12 characters, then the account service shall reject it with the reason `too short`.

FR-002: If a user chooses a password that contains no digit, then the account service shall reject it with the reason `needs a digit`.

FR-003: If a user chooses a password that matches an entry in the common-password list, compared without regard to letter case, then the account service shall reject it with the reason `too common`.

FR-004: If a user chooses a password equal to one of that user's last 5 passwords, then the account service shall reject it with the reason `used before`.

## 2. Non-Functional Requirements

NFR-001: When a user chooses a password, the account service shall answer within 50 milliseconds.

## 3. Open Questions

None.
