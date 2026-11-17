Set: dev. A pasted plan and no codebase: the plan write-plan 0.14.0 gave for its own benchmark input of the same name. Five phases, twelve IDs, one blocked entry.

IDs (12): Phase 1: FR-010, FR-002, FR-003, FR-005. Phase 2: FR-001, NFR-002. Phase 3: FR-004, NFR-001. Phase 4: FR-006, FR-007. Phase 5: FR-008, FR-009.

Order (the first task is earlier in the phase than the second):
- O1: Phase 1: the task that stores tables comes before the task that creates a booking.
- O2: Phase 1: creating a booking comes before rejecting one for lack of a table, and before cancelling one.
- O3: Phase 2: the availability endpoint comes before the booking page that reads it.
- O4: Phase 3: publishing `booking.created` comes before the consumer that sends the text.
- O5: Phase 4: the endpoint that lists a day's bookings comes before the day view page.
- O6: Phase 5: marking a no-show comes before releasing its table.

Manual:
- M1: NFR-002 has a `manual:` check. The plan verifies it with "a keyboard-only and screen-reader pass", which a person makes. An automated scan beside it is fine; a scan alone drops half of the plan's check.
- M2: no other ID is `manual:`. The plan gives each a test (API, UI, integration, load, or a controllable clock).

Files: every file is `new:`. A path is invented.

Blocked: `Blocked by Q-001: deposit for a party of more than 8 guests`, copied once, word for word. No task builds a deposit.
