Set: hold. Domain: stock depot, about 30 modules. Harder kinds: an implementation the requirement's words do not find, a fault across two modules, a second way in that skips a rule, tests through mocks. Drift: a feature branch with two files no requirement covers.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | The hook `replenish` in `depot/hooks/after_move.py` follows `stock.moved` and calls `drafts.open_for`; the code says floor, batch, and draft, never reorder or purchase order, and `depot/stock/reorder.py` only suggests numbers. `test_stock_falling_below_the_floor_drafts_an_order` and `test_stock_at_the_floor_drafts_nothing` pass. `unmet` here is a search that stopped at the file with the obvious name. |
| FR-002 | partial | Two modules. `packs.whole_packs` returns a number of packs and is right; `drafts.open_for` stores that number as `Order.qty`, which is units everywhere else, so 50 units in packs of 12 is ordered as 5. `test_order_is_for_the_batch` passes because its supplier's pack size is 1, and `test_packs.py` tests `whole_packs` alone. |
| FR-003 | met | `open_for` returns None while an order for the item is `draft` or `sent`; `test_item_with_an_order_waiting_gets_no_second_one` checks both statuses and passes. |
| FR-004 | unmet | Nothing sets `Order.overdue`, and `settings.OVERDUE_DAYS` is used nowhere. `test_overdue_orders_are_listed` passes because the test sets the flag itself. |
| FR-005 | untested | `dock.receive` adds the received quantity through `move`. Its tests check the order's status and date, never the stock. |
| FR-006 | partial | `replenish` returns early for a discontinued item, and `test_discontinued_item_is_not_ordered` passes. `handlers.post_order`, routed at `POST /orders`, calls `drafts.open_for` with no check, so the buyer can order a discontinued item. |
| FR-007 | met | `send.send` posts the payload to the supplier's endpoint. `test_order_is_posted_to_the_suppliers_endpoint` checks the call on a mock transport, which is the boundary: the sending code runs. |
| FR-008 | partial | On `TransportError` the reason goes into `Order.note`, but the status set before the post stays `sent`. `test_rejected_order_keeps_the_suppliers_reason` checks the note and `sent_at`, never the status. |
| FR-009 | skipped | `Blocked by Q-001`. |
| NFR-001 | met | `test_one_movement_among_10000_items_takes_under_20_ms` measures the stated size against the stated limit and passes. |

Expected tally: `4 met, 3 partial, 1 unmet, 1 untested, 1 skipped`.

Expected drift: `depot/reports/turnover.py, tests/reports/test_turnover.py` (both added on the branch, covered by no requirement). `tests/procurement/test_send.py` was also added on the branch and tests FR-007 and FR-008, so it is not drift.

Faults a `met` would miss: FR-002, FR-004, FR-005, FR-006, FR-008. Anything but `met` on FR-001, FR-003, FR-007, or NFR-001 is a false alarm. A verdict other than `skipped` on FR-009 is a wrong verdict.
