Plan the implementation of the expense-approval feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/expense-approval/requirements.md:

```markdown
# Requirements Specification: Expense Approval

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Employees submit expenses, managers approve them, approved expenses are reimbursed, and finance reports on them.

## 2. Scope

### In Scope

- Expense submission, approval, reimbursement, and the monthly report

### Out of Scope

None given.

**Systems:** expense service, approval service, payment service, notification service, reporting service

## 3. Functional Requirements

FR-001: When a finance officer opens the monthly report, the reporting service shall display the total of the approved expenses of each department. <!-- Source: "finance sees approved spend per department each month" -->

FR-002: When a finance officer exports the monthly report, the reporting service shall produce a CSV file of the approved expenses of the month. <!-- Source: "finance can export the month" -->

FR-003: When a manager approves an expense, the approval service shall mark the expense record as approved. <!-- Source: "managers approve expenses" -->

FR-004: When a manager rejects an expense, the approval service shall mark the expense record as rejected with the reason the manager gave. <!-- Source: "a rejection has a reason" -->

FR-005: If a manager approves an expense of more than 1,000 EUR, then the approval service shall hold the expense record until a second manager approves the expense. <!-- Source: "over 1,000 EUR needs two managers" -->

FR-006: When an employee submits an expense with an amount, a category, and a receipt, the expense service shall create an expense record with the status submitted. <!-- Source: "employees submit expenses with a receipt" -->

FR-007: If an employee submits an expense without a receipt, then the expense service shall reject the submission. <!-- Source: "no receipt, no expense" -->

FR-008: When the expense service creates an expense record, the notification service shall notify the manager of the employee. <!-- Source: "the manager is told about a new expense" -->

FR-009: When the approval service marks an expense record as approved, the payment service shall add the expense to the next payment run. <!-- Source: "approved expenses are paid in the next run" -->

FR-010: When the payment service pays an expense, the notification service shall email a payment confirmation to the employee. <!-- Source: "the employee is told when paid" -->

## 4. Non-Functional Requirements

NFR-001: When the expense service creates an expense record, the notification service shall notify the manager of the employee within 1 minute of the creation for 99% of expense records. <!-- Source: "managers hear about it quickly" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
