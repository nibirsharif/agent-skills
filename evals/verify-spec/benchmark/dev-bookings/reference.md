Set: dev. Domain: booking service. Harder kinds: a fault across two modules, tests through mocks, a rule kept outside the system the requirement names. Drift: one uncommitted file on `main`.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | `BookingService.book` stores the booking through `BookingStore.add`; `test_free_room_is_booked_active` passes. |
| FR-002 | partial | The named system. The overlap check is in `BookingService.book`, the only caller of `BookingStore.add`; the store the requirement names stores any booking. `test_overlapping_booking_is_rejected` drives the service and passes. An open row, `met` or `partial`, until the rules decided it. |
| FR-003 | partial | Two modules. `policy.is_late` takes hours and is right; `BookingService.cancel` passes it minutes (`total_seconds() / 60`), so only a cancellation less than 24 minutes before the start pays the fee. `test_late_cancellation_keeps_the_fee` passes because it cancels 10 minutes before, and `test_policy.py` tests `is_late` alone. |
| FR-004 | met | `cancel` calls `gateway.refund` once with the payment reference. `test_refund_request_goes_to_the_gateway` checks the call on a mock gateway, which is the boundary the requirement names: the service code runs. |
| FR-005 | partial | Two modules, behind a mock. `Notifier.cancelled` writes `booking.price`, not the refund, so a late cancellation's email states the full price. `test_user_is_told_the_refund` passes because the notifier is a mock, and `test_message_states_the_refund` because its refund equals the price. |
| FR-006 | untested | `cancel` raises `RefundFailed` before it changes the status, which is right. `test_rejected_refund_leaves_the_booking_active` replaces `BookingService.cancel` with a mock, so it checks only what `cancel_command` prints. No test makes the gateway reject. |
| FR-007 | partial or unmet | Open row, a gap either way. `cancel_command` cancels and prints the refund, and `test_cancel_prints_the_refund` calls it directly; `build_parser` has no `cancel` command, so `bookings cancel 1` is an argument error. The rules do not say whether code the trigger cannot reach is `partial` or `unmet`. |
| NFR-001 | untested | `test_room_lookup_is_fast` measures 100 bookings, not 10,000: a threshold with no test that measures it. |

Expected tally: `2 met, 4 partial, 2 untested`, with FR-007 as `partial`, or `2 met, 3 partial, 1 unmet, 2 untested` with it as `unmet`.

Expected drift: `bookings/export.py` (uncommitted, covered by no requirement).

Faults a `met` would miss: FR-002, FR-003, FR-005, FR-006, FR-007, NFR-001. Anything but `met` on FR-001 or FR-004 is a false alarm.
