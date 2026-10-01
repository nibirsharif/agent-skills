## 1. Approach

There is no existing code in this folder, so the feature is planned from the requirements alone. It is built along the return flow: requests and records first, then the label and warehouse intake, then refunds, then the status pages. Each phase merges on its own and leaves returns working for the flow it covers.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Return requests and records | FR-001, FR-002, FR-003, FR-004, FR-014 |
| 2 | Label email, cancellation, and warehouse intake | FR-005, NFR-001, FR-006, FR-007, FR-008, FR-009 |
| 3 | Refunds | FR-010, FR-011, FR-012, FR-013 |
| 4 | Return status pages | FR-015, FR-016, NFR-002 |
| 5 | Availability target | NFR-003 |

## 2. Phases

### Phase 1: Return requests and records

**Scope:** Create a return record for a delivered order, reject ineligible requests, generate the label, and keep the status history.

**Requirements:** FR-001, FR-002, FR-003, FR-004, FR-014

**Size:** about 9 files

**Reuse:** None found.

**Interface and data changes:**

- New or changed interfaces for return requests and records

**Verify:**

- FR-001: integration test that a request for a delivered order creates one return record
- FR-002: test that a request 31 days after delivery is rejected and one at 30 days is accepted
- FR-003: test that a request for an undelivered order is rejected
- FR-004: test that creating a return record generates one label
- FR-014: test that every status change is stored with its time

**Open questions:** None.

### Phase 2: Label email, cancellation, and warehouse intake

**Scope:** Email the label (with its 5-minute limit), let a customer cancel before the label is scanned, and record receipt and inspection at the warehouse.

**Requirements:** FR-005, NFR-001, FR-006, FR-007, FR-008, FR-009

**Size:** about 9 files

**Reuse:** None found.

**Interface and data changes:**

- New or changed interfaces for label email, cancellation, and warehouse intake

**Verify:**

- FR-005: integration test that the notification service emails the generated label to the customer
- NFR-001: timing test that 99% of label emails are sent within 5 minutes of generation
- FR-006: test that cancelling before the label is scanned marks the record cancelled
- FR-007: test that scanning a label marks the record received
- FR-008: test that receipt prompts staff for the condition of each returned item
- FR-009: test that recording every item's condition marks the record inspected

**Open questions:** None.

### Phase 3: Refunds

**Scope:** Calculate and pay the refund, mark a rejected refund, and email the confirmation.

**Requirements:** FR-010, FR-011, FR-012, FR-013

**Size:** about 8 files

**Reuse:** None found.

**Interface and data changes:**

- New or changed interfaces for refunds

**Verify:**

- FR-010: unit test of the refund amount for each recorded condition
- FR-011: test against the payment gateway's test mode that the refund goes to the original payment method
- FR-012: test that a gateway rejection marks the record refund failed
- FR-013: test that a completed refund emails the confirmation

**Open questions:** None.

### Phase 4: Return status pages

**Scope:** Show return status to customers and its history to support agents. The accessibility level is met in the page that FR-015 builds.

**Requirements:** FR-015, FR-016, NFR-002

**Size:** about 7 files

**Reuse:** None found.

**Interface and data changes:**

- New or changed interfaces for return status pages

**Verify:**

- FR-015: browser test that the status page lists each of the customer's returns
- FR-016: test that the support console shows the status history
- NFR-002: automated WCAG 2.2 level AA audit of the status page

**Open questions:** None.

### Phase 5: Availability target

**Scope:** Meet the monthly availability target. It needs monitoring and failover, which change no behaviour, so it follows the phases that build the behaviour.

**Requirements:** NFR-003

**Size:** about 4 files

**Reuse:** None found.

**Interface and data changes:**

- New or changed interfaces for availability target

**Verify:**

- NFR-003: availability measured per calendar month against 99.9%

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.
