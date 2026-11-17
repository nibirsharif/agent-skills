Plan the implementation of the parking-permits feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/parking-permits/requirements.md:

```markdown
# Requirements Specification: Parking Permits

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Residents apply for parking permits, council officers decide on them, and wardens check number plates.

## 2. Scope

### In Scope

- Applications, decisions, plate checks, renewals, and plate changes

### Out of Scope

None given.

**Systems:** permit service, notification service

## 3. Functional Requirements

FR-001: When a warden scans a number plate in a zone, the permit service shall return whether a valid permit covers the number plate in the zone. <!-- Source: "wardens check plates" -->

FR-002: When a resident applies for a permit with a number plate and a proof of address, the permit service shall create a permit application. <!-- Source: "residents apply online" -->

FR-003: If a resident applies for a permit with a number plate that already has a valid permit, then the permit service shall reject the permit application. <!-- Source: "one permit per plate" -->

FR-004: When a council officer approves a permit application, the permit service shall issue a permit that is valid for 12 months in the zone of the address. <!-- Source: "officers approve; permits last a year" -->

FR-005: When a council officer rejects a permit application, the permit service shall record the reason the council officer gave. <!-- Source: "rejections have a reason" -->

FR-006: When the permit service issues a permit, the notification service shall email the permit to the resident. <!-- Source: "the permit is emailed" -->

FR-007: When a permit is 30 days from the end date of the permit, the notification service shall email a renewal reminder to the resident. <!-- Source: "remind people a month before" -->

FR-008: When a resident renews a permit, the permit service shall extend the end date of the permit by 12 months. <!-- Source: "renewal adds a year" -->

FR-009: When a resident changes the number plate of a permit, the permit service shall replace the number plate of the permit. <!-- Source: "people change cars" -->

Pending: Q-001, Q-002.

## 4. Non-Functional Requirements

NFR-001: When a warden scans a number plate, the permit service shall return the result within 2 seconds of the scan for 99% of scans. <!-- Source: "wardens cannot wait" -->

NFR-002: The permit service shall keep each permit application for 6 years. <!-- Source: "records are kept six years" -->

## 5. Open Questions

Q-001: What does a permit cost in each zone? <!-- Source: "permits are paid for" -->

Q-002: How many visitor permits may one household hold at once? <!-- Source: "visitor permits" -->

Q-003: Closed. Can one resident hold permits for two number plates? Answer: yes, one permit application per number plate. <!-- Source: "coverage gap in FR-003" -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
