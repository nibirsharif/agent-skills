# Requirements: Subscriptions

**Version:** 1.0
**Date:** 2026-11-21
**Status:** Draft

## 1. Functional Requirements

FR-001: When a visitor subscribes with an address, the mailing service shall store the address with the status `pending`.

FR-002: If a visitor subscribes with an address that has no `@`, then the subscriber store shall reject the address with `InvalidAddress`.

FR-003: If a visitor subscribes with an address that is already stored, compared without regard to letter case, then the mailing service shall reject the address with `AlreadySubscribed`.

FR-004: When a subscriber opens the confirmation link, the mailing service shall set the subscriber's status to `active`.

FR-005: When a subscriber unsubscribes, the mailing service shall send one message that confirms the removal to the subscriber's address.

FR-006: When a campaign is sent, the mailing service shall send it only to subscribers whose status is `active`.

FR-007: If the mail server refuses a campaign's message to a subscriber, then the mailing service shall set the subscriber's status to `bounced`.

FR-008: When a visitor opens `/unsubscribe/<token>`, the mailing service shall unsubscribe the token's address.

## 2. Non-Functional Requirements

NFR-001: The mailing service shall build the recipient list for 50,000 subscribers within 1 second.

## 3. Open Questions

None.
