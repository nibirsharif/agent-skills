## 1. Approach

There is no existing code in this folder, so the feature is planned from the requirements alone: the booking form creates a booking and sends the confirmation email within its deadline, and a booking for an already booked date is rejected. One phase delivers everything that is written.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Booking and confirmation | FR-001, FR-004, NFR-001 |

## 2. Phases

### Phase 1: Booking and confirmation

**Scope:** Accept a booking and send its confirmation email within 2 minutes, and reject a double booking. NFR-001 is the deadline on FR-001, so it is met in the same phase.

**Requirements:** FR-001, FR-004, NFR-001

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- A booking endpoint for the booking form
- A room-availability store keyed by room and dates

**Verify:**

- FR-001: integration test that a submitted booking form sends one confirmation email to the guest's email address
- FR-004: integration test that a booking for an already booked date is rejected
- NFR-001: timing test that the confirmation email is sent within 2 minutes of the submission

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.
