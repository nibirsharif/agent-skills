Break the table-booking plan into tasks. There is no codebase in this folder, and the plan is not on disk; this is docs/specs/table-booking/plan.md:

```markdown
# Implementation Plan: Table Booking

**Version:** 1.0
**Date:** 2026-03-04
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

There is no codebase in this folder and the requirements file is not on disk, so this plan comes from the pasted requirements (version 1.0) alone and every Reuse is `None found.`. The booking service comes first, with tables, bookings and availability. The guest booking page, the confirmation text, the staff day view and arrivals, and the no-show handling follow, each as its own PR. The deposit for large parties waits on Q-001 and is not planned.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Tables and bookings in the booking service | FR-010, FR-002, FR-003, FR-005 |
| 2 | Guest booking page | FR-001, NFR-002 |
| 3 | Confirmation text message | FR-004, NFR-001 |
| 4 | Staff day view and arrivals | FR-006, FR-007 |
| 5 | No-shows | FR-008, FR-009 |

## 2. Phases

### Phase 1: Tables and bookings in the booking service

**Scope:** Staff can define tables, and the booking service can create, reject and cancel bookings against free tables. It has no UI and sends no text yet; those come in later phases.

**Requirements:** FR-010, FR-002, FR-003, FR-005

**Size:** about 8 files

**Reuse:** None found.

**Interface and data changes:**

- `tables` store with a seat count per table
- `time_slots` and `bookings` stores; a booking holds the time slot, party size, phone number, table, and status
- Endpoint to define a table with a seat count
- Endpoint to book a time slot with a party size and a phone number, which rejects the request when no free table fits the party size
- Endpoint to cancel a booking, which releases its table

**Verify:**

- FR-010: API test that defining a table with a seat count stores it and returns it on read.
- FR-002: API test that booking a free time slot with a party size and a phone number creates a booking for that slot.
- FR-003: API test that booking a time slot with no free table for the party size is rejected and creates no booking.
- FR-005: API test that after a booking is cancelled, the same time slot can be booked again with that table.

**Open questions:** None.

### Phase 2: Guest booking page

**Scope:** The booking web app shows a day's free time slots, from an availability endpoint added in this phase. The accessibility level is met here because the page is built here. Booking from the page is left for later.

**Requirements:** FR-001, NFR-002

**Size:** about 7 files

**Reuse:** None found.

**Interface and data changes:**

- Availability endpoint in the booking service that returns the free time slots of a day, built on the Phase 1 stores
- Booking page route in the booking web app, taking a day

**Verify:**

- FR-001: UI test that opening the booking page for a day lists exactly the time slots that have a free table, and omits a fully booked slot.
- NFR-002: automated WCAG 2.2 AA scan, with a keyboard-only and screen-reader pass, of the booking page, with no violations.

**Open questions:** None.

### Phase 3: Confirmation text message

**Scope:** The notification service sends a confirmation text when a booking is created, within the NFR-001 threshold. NFR-001 sits here because it constrains this send.

**Requirements:** FR-004, NFR-001

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- `booking.created` event published by the booking service
- Notification service consumer of that event, which sends a text to the booking's phone number
- SMS provider configuration in the notification service

**Verify:**

- FR-004: integration test that creating a booking sends one confirmation text to the booking's phone number.
- NFR-001: load test that 95% of confirmation texts are sent within 30 seconds of booking creation.

**Open questions:** None.

### Phase 4: Staff day view and arrivals

**Scope:** Staff see a day's bookings by time slot in the staff console and mark a booking as arrived. Automatic no-shows are left for Phase 5.

**Requirements:** FR-006, FR-007

**Size:** about 8 files

**Reuse:** None found.

**Interface and data changes:**

- Endpoint that lists the bookings of a day, grouped by time slot
- Endpoint to mark a booking as arrived, which stores an `arrived_at` time on the booking
- Day view page in the staff console

**Verify:**

- FR-006: UI test that the day view lists the day's bookings under their time slots.
- FR-007: API test that marking a booking as arrived stores its arrival time, and that the day view shows it.

**Open questions:** None.

### Phase 5: No-shows

**Scope:** The booking service marks a booking as a no-show when the guest has not arrived 15 minutes after the slot starts, and releases its table.

**Requirements:** FR-008, FR-009

**Size:** about 5 files

**Reuse:** None found.

**Interface and data changes:**

- Scheduled job in the booking service that finds bookings with no `arrived_at` 15 minutes after the time slot start
- `no_show` booking status

**Verify:**

- FR-008: test with a controllable clock that a booking not arrived at 15 minutes after the slot start becomes a no-show, and that one marked arrived is left unchanged.
- FR-009: API test that after the no-show, the table can be booked again for that time slot.

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001: deposit for a party of more than 8 guests

## 4. Open Questions

Q-001: How much is the deposit for a party of more than 8 guests? (touches the blocked deposit requirement)

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-04 | Initial plan from requirements.md 1.0 |
```
