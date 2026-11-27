# Requirements: Low-Stock Reordering

**Version:** 1.0
**Date:** 2026-11-22
**Status:** Draft

## 1. Functional Requirements

FR-001: When a stock movement takes an item's stock below its reorder point, the depot system shall create a purchase order for the item.

FR-002: The depot system shall set a purchase order's quantity, in units, to the item's reorder quantity rounded up to a whole number of the supplier's packs.

FR-003: While an item has a purchase order that is not yet received, the depot system shall not create another purchase order for the item.

FR-004: If a purchase order has not been received 14 days after it was sent, then the depot system shall mark the order overdue.

FR-005: When a purchase order is received, the depot system shall add the received quantity to the item's stock.

FR-006: If an item is discontinued, then the depot system shall not create a purchase order for it.

FR-007: When a purchase order is sent, the depot system shall post it to the supplier's endpoint.

FR-008: If the supplier's endpoint rejects a purchase order, then the depot system shall keep the order in the status `draft` and record the supplier's reason on the order.

FR-009: Where an item has a second supplier, the depot system shall order from the second supplier when the first is out of stock. Blocked by Q-001.

## 2. Non-Functional Requirements

NFR-001: The depot system shall handle one stock movement within 20 milliseconds with 10,000 items stored.

## 3. Open Questions

Q-001: How does the depot system learn that a supplier is out of stock?
