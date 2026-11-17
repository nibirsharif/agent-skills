Set: dev. Twelve written requirements, one blocked, limit 8 per phase. The file lists the table setup (FR-010) last, and everything else needs it.

Written IDs (12): FR-001 to FR-010, NFR-001, NFR-002.

Phase count: 2 to 4.

Before (the first is in the same phase as the second, or an earlier one):
- D1: FR-010 before FR-002. A booking needs tables with seat counts.
- D2: FR-010 before FR-001. Free time slots are computed from the tables.
- D3: FR-002 before FR-004. The confirmation follows a created booking.
- D4: FR-002 before FR-005. A cancellation needs a booking.
- D5: FR-002 before FR-006. The day view shows bookings.
- D6: FR-002 before FR-007.
- D7: FR-008 before FR-009. The release follows the no-show mark.

Together (same phase):
- T1: NFR-001 with FR-004, the response it limits.
- T2: FR-002 with FR-003: one request, accepted or rejected.
- T3: FR-008 with FR-009.
- T4: NFR-002 with FR-001, or in a later phase whose scope says why.

Blocked: one entry, `Blocked by Q-001`, about the deposit for large parties. No phase, scope, or verification plans a deposit, and no amount is stated.

One sensible cut: tables, free slots, and booking (FR-010, FR-001, FR-002, FR-003, NFR-002); confirmation and cancellation (FR-004, NFR-001, FR-005); the day view, arrivals, and no-shows (FR-006, FR-007, FR-008, FR-009).
