Plan the implementation of the order-returns feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/order-returns/requirements.md:

```markdown
# Requirements Specification: Order Returns

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Customers return delivered orders, the warehouse inspects the returned items, and the customer is refunded.

## 2. Scope

### In Scope

- Return requests, return labels, warehouse intake, refunds, and status pages

### Out of Scope

None given.

**Systems:** returns service, notification service, warehouse service, refund service, returns web app, support console

## 3. Functional Requirements

REQ-001: When a customer submits a return request for a delivered order, the returns service shall create a return record for the order. <!-- Source: "a customer can return a delivered order" -->

REQ-002: If a customer submits a return request for an order that was delivered more than 30 days earlier, then the returns service shall reject the return request. <!-- Source: "returns are accepted within 30 days of delivery" -->

REQ-003: If a customer submits a return request for an order that has not been delivered, then the returns service shall reject the return request. <!-- Source: "only delivered orders can be returned" -->

REQ-004: When the returns service creates a return record, the returns service shall generate a return label for the return record. <!-- Source: "a return label is generated for each return" -->

REQ-005: When the returns service generates a return label, the notification service shall email the return label to the customer. <!-- Source: "the customer gets the label by email" -->

REQ-006: When a customer cancels a return request before the return label is scanned, the returns service shall mark the return record as cancelled. <!-- Source: "a customer can cancel a return before sending it" -->

REQ-007: When the warehouse service scans a return label, the warehouse service shall mark the return record as received. <!-- Source: "the warehouse marks returns as received" -->

REQ-008: When the warehouse service marks a return record as received, the warehouse service shall prompt the warehouse staff to record the condition of each returned item. <!-- Source: "staff record item condition on receipt" -->

REQ-009: When warehouse staff record the condition of each returned item, the returns service shall mark the return record as inspected. <!-- Source: "inspected returns are marked" -->

REQ-010: When the returns service marks a return record as inspected, the refund service shall calculate the refund amount from the condition of each returned item. <!-- Source: "the refund depends on item condition" -->

REQ-011: When the refund service calculates the refund amount, the refund service shall refund the amount to the original payment method of the order. <!-- Source: "refunds go to the original payment method" -->

REQ-012: If the payment gateway rejects a refund, then the refund service shall mark the return record as refund failed. <!-- Source: "a rejected refund is visible" -->

REQ-013: When the refund service refunds the amount, the notification service shall email a refund confirmation to the customer. <!-- Source: "the customer is told about the refund" -->

REQ-014: When a return record changes status, the returns service shall record the new status with the time of the change. <!-- Source: "status changes are kept" -->

REQ-015: When a customer opens the return status page, the returns web app shall display the status of each return record of the customer. <!-- Source: "customers can see their returns" -->

REQ-016: When a support agent opens a return record, the support console shall display the status history of the return record. <!-- Source: "support can see the history" -->

## 4. Non-Functional Requirements

NFR-001: When the returns service generates a return label, the notification service shall email the return label to the customer within 5 minutes of the generation for 99% of return labels. <!-- Source: "the label email must be quick" -->

NFR-002: The returns web app shall comply with WCAG 2.2 level AA. <!-- Source: "accessibility" -->

NFR-003: The returns service shall have an availability of 99.9% per calendar month. <!-- Source: "availability" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
