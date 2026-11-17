# Requirements: Cart Totals

**Version:** 1.0
**Date:** 2026-10-12
**Status:** Draft

## 1. Functional Requirements

FR-001: When a shopper adds an item, the cart shall include the item's price multiplied by its quantity in the subtotal.

FR-002: When a shopper applies the coupon code `SAVE10`, the cart shall reduce the subtotal by 10 percent.

FR-003: If a shopper adds an item with a quantity below 1, then the cart shall raise `ValueError`.

FR-004: While the cart has no items, the cart shall report a subtotal of 0.00.

FR-005: When the subtotal is 50.00 or more, the cart shall set the shipping charge to 0.00.

FR-006: When a shopper asks for the tax, the cart shall apply the tax rate of the shopper's country to the subtotal. Blocked by Q-001.

## 2. Non-Functional Requirements

None.

## 3. Open Questions

Q-001: Which tax rate applies to each country, and where does the cart read it from?
