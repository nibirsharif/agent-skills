Break the parking-permits plan into tasks. There is no codebase in this folder, and the plan is not on disk; this is docs/specs/parking-permits/plan.md:

```markdown
# Implementation Plan: Parking Permits

**Version:** 1.0
**Date:** 2026-03-04
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

There is no codebase in this folder and the requirements file is not on disk, so this plan comes from the pasted requirements alone and Reuse is `None found.` in every phase. It builds the permit service's data and application flow first, then plate checks, then the notification service's emails, then renewals and plate changes. Each phase merges on its own and leaves a working product. The cost and visitor-permit requirements are not written yet, so they are blocked and get no phase.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Permit applications and officer decisions | FR-002, FR-003, FR-004, FR-005, NFR-002 |
| 2 | Warden plate check | FR-001, NFR-001 |
| 3 | Permit and renewal reminder emails | FR-006, FR-007 |
| 4 | Renewals and plate changes | FR-008, FR-009 |

## 2. Phases

### Phase 1: Permit applications and officer decisions

**Scope:** Residents apply with a number plate and proof of address. Officers approve, which issues a 12-month permit in the address's zone, or reject with a reason. Applications are retained for 6 years. Emails, plate checks, renewals and plate changes are left for later phases.

**Requirements:** FR-002, FR-003, FR-004, FR-005, NFR-002

**Size:** about 9 files

**Reuse:** None found.

**Interface and data changes:**

- Permit service endpoint to submit an application (number plate, proof of address)
- Permit service endpoint for an officer to approve or reject an application, with a reason on rejection
- `permit_application` record: number plate, proof of address, status, rejection reason, resident, zone
- `permit` record: number plate, zone, start date, end date, linked application
- Retention setting for applications: 6 years

**Verify:**

- FR-002: integration test that an application with a number plate and proof of address creates a permit application
- FR-003: integration test that an application for a number plate with a valid permit is rejected
- FR-004: integration test that approval issues a permit whose end date is 12 months after issue, in the zone of the address
- FR-005: integration test that rejection stores the officer's reason on the application
- NFR-002: test that the purge job keeps an application for 6 years and does not delete it before then

**Open questions:** None.

### Phase 2: Warden plate check

**Scope:** A warden scans a number plate in a zone and gets back whether a valid permit covers it. Phase 1's permits are the data source. The phase includes the response-time threshold, because it builds the behaviour that NFR-001 constrains.

**Requirements:** FR-001, NFR-001

**Size:** about 5 files

**Reuse:** None found.

**Interface and data changes:**

- Permit service plate-check endpoint: number plate and zone in, covered or not covered out
- Index on permit number plate, zone and end date

**Verify:**

- FR-001: integration tests for a plate with a valid permit in the zone, for the same plate in another zone, and for a plate whose permit has ended
- NFR-001: load test that 99% of scans return within 2 seconds

**Open questions:** None.

### Phase 3: Permit and renewal reminder emails

**Scope:** The notification service emails the permit to the resident when it is issued, and emails a renewal reminder 30 days before the permit's end date. Renewing and changing plates are left for Phase 4.

**Requirements:** FR-006, FR-007

**Size:** about 7 files

**Reuse:** None found.

**Interface and data changes:**

- Permit-issued event from the permit service, consumed by the notification service
- Notification service email templates for the permit and the renewal reminder
- Daily scheduled job that finds permits 30 days from their end date and records that the reminder was sent

**Verify:**

- FR-006: integration test that issuing a permit sends one email with the permit to the resident
- FR-007: test with a controlled clock that a permit 30 days from its end date triggers one reminder email, and that none is sent a second time

**Open questions:** None.

### Phase 4: Renewals and plate changes

**Scope:** A resident renews a permit, which extends its end date by 12 months. A resident changes the number plate on a permit, which replaces the plate. Cost and visitor permits are not part of this phase.

**Requirements:** FR-008, FR-009

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- Permit service endpoint to renew a permit
- Permit service endpoint to change a permit's number plate

**Verify:**

- FR-008: integration test that renewal moves the end date 12 months later
- FR-009: integration test that a plate change replaces the plate, and that a plate check for the new plate is covered and for the old plate is not

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001: permit cost in each zone

Blocked by Q-002: limit on visitor permits per household

## 4. Open Questions

Q-001: What does a permit cost in each zone? (touches the blocked permit cost requirement)

Q-002: How many visitor permits may one household hold at once? (touches the blocked visitor permit requirement)

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-04 | Initial plan from requirements.md 1.0 |
```
