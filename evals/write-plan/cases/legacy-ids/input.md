Plan the implementation of the booking feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/booking/requirements.md:

```markdown
# Requirements Specification: Booking

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Guests book rooms and receive a confirmation email. Cancelling frees the room.

## 2. Scope

### In Scope

- Booking, cancelling, and room availability

### Out of Scope

None given.

**Systems:** booking service

## 3. Functional Requirements

REQ-001: When a guest submits the booking form, the booking service shall send a confirmation email to the guest's email address. <!-- Source: "a guest submits the booking form, the booking service sends a confirmation email" -->

REQ-002: When a guest cancels a booking, the booking service shall mark the room of that booking as available for the dates of that booking. <!-- Source: "When a guest cancels a booking, the booking service marks the room as available." -->

REQ-003: If a guest submits the booking form for a room that is already booked for any of the requested dates, then the booking service shall reject the booking. <!-- Source: "No double bookings." -->

## 4. Non-Functional Requirements

REQ-004: When a guest submits the booking form, the booking service shall send a confirmation email to the guest's email address within 2 minutes of the submission. <!-- Source: "within 2 minutes of the submission" -->

REQ-005: When a guest cancels a booking, the booking service shall mark the room of that booking as available for the dates of that booking within 1 minute of the cancellation for 99% of cancellations. <!-- Source: "the room must be free again within a minute for 99% of cancellations" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
