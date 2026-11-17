## 1. Approach

There is no codebase in this folder and `docs/specs/expense-approval/requirements.md` is not on disk, so this plan comes from the pasted requirements alone (version 1.0). It builds the flow in order. First the expense service creates and validates expense records. Then the approval service decides on them, with the two-manager rule for large amounts. Then payment and the employee confirmation. Last, the reporting service. Manager notification stays with the expense creation it follows, so the 1-minute threshold is met in the phase that builds that behaviour. Nothing exists to build on, so the plan lists no reuse.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Expense submission and manager notification | FR-006, FR-007, FR-008, NFR-001 |
| 2 | Manager approval and rejection | FR-003, FR-004, FR-005 |
| 3 | Reimbursement and payment confirmation | FR-009, FR-010 |
| 4 | Monthly report and export | FR-001, FR-002 |

## 2. Phases

### Phase 1: Expense submission and manager notification

**Scope:** An employee submits an expense with an amount, a category and a receipt, and the manager is notified within the deadline. A submission without a receipt is rejected. Approval, payment and reporting are left for later phases.

**Requirements:** FR-006, FR-007, FR-008, NFR-001

**Size:** about 8 files

**Reuse:** None found.

**Interface and data changes:**

- Expense service: a submit operation taking amount, category and receipt
- Expense record with status `submitted`, amount, category, receipt reference, employee and the employee's manager
- Event `expense.created`, consumed by the notification service
- Notification service: a handler that notifies the manager on `expense.created`

**Verify:**

- FR-006: integration test that a submission with an amount, a category and a receipt creates a record with status `submitted`
- FR-007: integration test that a submission without a receipt is rejected and no record is created
- FR-008: integration test that creating a record notifies the employee's manager
- NFR-001: load test that at least 99% of managers are notified within 1 minute of record creation

**Open questions:** None.

### Phase 2: Manager approval and rejection

**Scope:** A manager approves or rejects a submitted expense, and a rejection stores the reason. An expense of more than 1,000 EUR is held after the first approval until a second manager approves it. Payment is left for Phase 3.

**Requirements:** FR-003, FR-004, FR-005

**Size:** about 7 files

**Reuse:** None found.

**Interface and data changes:**

- Approval service: approve and reject operations on an expense record
- Expense record: statuses `approved`, `rejected` and a held state, a rejection reason, and the approvals recorded so far
- Event `expense.approved`, published when a record becomes approved

**Verify:**

- FR-003: integration test that a manager's approval of an expense of 1,000 EUR or less sets the status to `approved`
- FR-004: integration test that a rejection sets the status to `rejected` and stores the reason given
- FR-005: integration test that a first approval of an expense above 1,000 EUR leaves it held, and a second manager's approval marks it approved

**Open questions:** None.

### Phase 3: Reimbursement and payment confirmation

**Scope:** An approved expense joins the next payment run, and the employee gets an emailed confirmation once it is paid. The monthly report is left for Phase 4.

**Requirements:** FR-009, FR-010

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- Payment service: a handler for `expense.approved` that adds the expense to the next payment run
- Payment run record listing its expenses, and an event `expense.paid`
- Notification service: a handler that emails a payment confirmation on `expense.paid`

**Verify:**

- FR-009: integration test that approving an expense puts it in the next payment run
- FR-010: integration test that paying an expense sends one confirmation email to the employee

**Open questions:** None.

### Phase 4: Monthly report and export

**Scope:** A finance officer sees the approved total per department for a month and exports the month's approved expenses as CSV. It only reads data from earlier phases.

**Requirements:** FR-001, FR-002

**Size:** about 5 files

**Reuse:** None found.

**Interface and data changes:**

- Reporting service: a monthly report operation returning the approved total per department
- Reporting service: a monthly export operation returning a CSV file of the month's approved expenses

**Verify:**

- FR-001: test with approved expenses in two departments that the report shows the correct total for each department
- FR-002: test that the exported CSV holds exactly the month's approved expenses

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.
