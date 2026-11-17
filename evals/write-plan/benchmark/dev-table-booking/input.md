Plan the implementation of the table-booking feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/table-booking/requirements.md:

```markdown
# Requirements Specification: Table Booking

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Guests book a table at the restaurant, and staff see the bookings of the day and record arrivals.

## 2. Scope

### In Scope

- Tables, time slots, bookings, confirmations, the day view, arrivals, and no-shows

### Out of Scope

None given.

**Systems:** booking service, notification service, booking web app, staff console

## 3. Functional Requirements

FR-001: When a guest opens the booking page for a day, the booking web app shall display the free time slots of the day. <!-- Source: "guests see what is free" -->

FR-002: When a guest books a free time slot with a party size and a phone number, the booking service shall create a booking for the time slot. <!-- Source: "guests book a slot for their party" -->

FR-003: If a guest books a time slot that has no free table for the party size, then the booking service shall reject the booking. <!-- Source: "no table, no booking" -->

FR-004: When the booking service creates a booking, the notification service shall send a confirmation text message to the guest. <!-- Source: "guests get a text" -->

FR-005: When a guest cancels a booking, the booking service shall release the table of the booking. <!-- Source: "a cancelled table is free again" -->

FR-006: When a staff member opens the day view, the staff console shall display the bookings of the day by time slot. <!-- Source: "staff see the day" -->

FR-007: When a staff member marks a booking as arrived, the booking service shall record the arrival time of the booking. <!-- Source: "staff tick guests off" -->

FR-008: If a guest has not arrived 15 minutes after the start of the time slot, then the booking service shall mark the booking as a no-show. <!-- Source: "15 minutes late is a no-show" -->

FR-009: When the booking service marks a booking as a no-show, the booking service shall release the table of the booking. <!-- Source: "no-show tables go back on sale" -->

FR-010: When a staff member defines a table with a seat count, the booking service shall store the table. <!-- Source: "staff set up the tables and their seats" -->

Pending: Q-001.

## 4. Non-Functional Requirements

NFR-001: When the booking service creates a booking, the notification service shall send the confirmation text message to the guest within 30 seconds of the creation for 95% of bookings. <!-- Source: "the text arrives quickly" -->

NFR-002: The booking web app shall comply with WCAG 2.2 level AA. <!-- Source: "accessibility" -->

## 5. Open Questions

Q-001: How much is the deposit for a party of more than 8 guests? <!-- Source: "large parties pay a deposit" -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
