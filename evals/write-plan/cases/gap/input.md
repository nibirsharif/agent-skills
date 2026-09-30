Plan the implementation of the audit-log feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/audit-log/requirements.md:

```markdown
# Requirements Specification: Audit Log

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Administrators can view and export a log of the actions users take in the product.

## 2. Scope

### In Scope

- Recording user actions and letting administrators view them

### Out of Scope

None given.

**Systems:** audit log service

## 3. Functional Requirements

REQ-001: When a user changes a record, the audit log service shall record the user, the record, and the time of the change. <!-- Source: "Every change to a record is logged with who, what, and when." -->

REQ-002: When an administrator opens the audit log, the audit log service shall display the recorded changes of the administrator's own tenant. <!-- Source: "Admins see their own tenant's log." -->

Pending: Q-001.

## 4. Non-Functional Requirements

None given.

## 5. Open Questions

Q-001: Is each tenant's audit log stored in a separate database or in one shared database? <!-- Source: "Admins see their own tenant's log." -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
