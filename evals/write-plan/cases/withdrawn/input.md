Plan the implementation of the room-booking feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/room-booking/requirements.md:

```markdown
# Requirements Specification: Room Booking

**Version:** 1.2
**Date:** 2026-03-05
**Author:** Not given.
**Status:** Draft

## 1. Summary

Guests book rooms and receive a confirmation email.

## 2. Scope

### In Scope

- Booking rooms and confirming bookings

### Out of Scope

None given.

**Systems:** booking service

## 3. Functional Requirements

FR-001: When a guest submits the booking form, the booking service shall send a confirmation email to the guest's email address. <!-- Source: "a guest submits the booking form, the booking service sends a confirmation email" -->

FR-002: Withdrawn.

FR-003: Withdrawn. Moved to NFR-001.

FR-004: If a guest submits the booking form for a room that is already booked for any of the requested dates, then the booking service shall reject the booking. <!-- Source: "No double bookings." -->

## 4. Non-Functional Requirements

NFR-001: When a guest submits the booking form, the booking service shall send a confirmation email to the guest's email address within 2 minutes of the submission. <!-- Source: "within 2 minutes of the submission" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |
| 1.1 | 2026-03-04 | Not given. | Withdrew FR-002 |
| 1.2 | 2026-03-05 | Not given. | Moved FR-003 to NFR-001 |

## 7. References

None given.
```
