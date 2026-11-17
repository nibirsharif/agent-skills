Set: dev. Domain: web shop. Drift: a feature branch with one file no requirement covers.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | `Cart.subtotal` sums price times quantity; `test_subtotal_sums_price_times_quantity` passes. |
| FR-002 | partial | `SAVE10` takes 15 percent, not 10. `test_save10_reduces_the_subtotal` passes because it computes the expected value from the same constant. |
| FR-003 | partial | `add` rejects a quantity below 0, so 0 is accepted. `test_negative_quantity_is_rejected` tries only -1. |
| FR-004 | met | An empty cart's subtotal is 0.00; `test_empty_cart_is_zero` passes. |
| FR-005 | untested | `shipping` is right, but its only test is skipped, so it did not run. |
| FR-006 | skipped | `Blocked by Q-001`. The code has a flat-rate `tax` with a passing test; a blocked requirement is still never checked. |

Expected tally: `2 met, 2 partial, 1 untested, 1 skipped`.

Expected drift: `shop/currency.py` (added on the branch, covered by no requirement). `shop/cart.py` and `tests/test_cart.py` also changed on the branch and are not drift.

Faults a `met` would miss: FR-002, FR-003, FR-005. A verdict other than `skipped` on FR-006 is a wrong verdict.
