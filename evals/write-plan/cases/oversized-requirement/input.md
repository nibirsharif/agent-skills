Plan the implementation of the legacy-import feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/legacy-import/requirements.md:

```markdown
# Requirements Specification: Legacy Import

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

An administrator copies the records of the legacy system into the new database.

## 2. Scope

### In Scope

- Copying legacy records, the error report, and the summary email

### Out of Scope

None given.

**Systems:** import service, notification service

## 3. Functional Requirements

FR-001: When an administrator starts the legacy import, the import service shall copy the records of each of the 14 legacy modules (customers, contacts, quotes, orders, invoices, payments, products, price lists, suppliers, purchase orders, stock, shipments, returns, and tickets) to the new database in the record format of that module. <!-- Source: "everything in the old system moves over, module by module, and each module has its own format" -->

FR-002: If a legacy record fails validation, then the import service shall write the record and the reason to the import error report. <!-- Source: "bad records are reported, not dropped silently" -->

FR-003: When the legacy import finishes, the notification service shall email the administrator the number of copied records and failed records of each module. <!-- Source: "the admin gets a summary" -->

## 4. Non-Functional Requirements

None given.

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
