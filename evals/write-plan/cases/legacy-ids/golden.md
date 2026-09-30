## 1. Approach

There is no existing code in this folder, so the feature is planned from the requirements alone: the booking form creates a booking, sends the confirmation email, and rejects double bookings, and cancelling frees the room. The two timing requirements in section 4 of the file are non-functional, so they are built with the behaviour they constrain. One phase delivers everything.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Booking, confirmation, cancellation | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 |

## 2. Phases

### Phase 1: Booking, confirmation, and cancellation

**Scope:** Accept and reject bookings, send the confirmation email, and free the room on cancellation. REQ-004 and REQ-005 are timing limits on REQ-001 and REQ-002, so they are met in the same phase.

**Requirements:** REQ-001, REQ-002, REQ-003, REQ-004, REQ-005

**Size:** about 8 files

**Reuse:** None found.

**Interface and data changes:**

- A booking endpoint for the booking form
- A cancellation endpoint
- A room-availability store keyed by room and dates

**Verify:**

- REQ-001: integration test that a submitted booking form sends one confirmation email to the guest's email address
- REQ-002: integration test that cancelling a booking makes the room available for the booking's dates
- REQ-003: integration test that a booking for an already booked date is rejected
- REQ-004: timing test that the confirmation email is sent within 2 minutes of the submission
- REQ-005: timing test that 99% of cancellations free the room within 1 minute

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.
