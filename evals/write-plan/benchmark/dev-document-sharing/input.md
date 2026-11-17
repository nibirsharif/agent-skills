Plan the implementation of the document-sharing feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/document-sharing/requirements.md:

```markdown
# Requirements Specification: Document Sharing

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Owners share documents with other users or by public link, and see who has access.

## 2. Scope

### In Scope

- Shares with users, public links, the sharing panel, and the access log

### Out of Scope

None given.

**Systems:** sharing service, notification service, documents web app

## 3. Functional Requirements

FR-001: When an owner shares a document with a user by email address, the sharing service shall grant the user view access to the document. <!-- Source: "share with a person" -->

FR-002: Withdrawn. Moved to NFR-002.

FR-003: When an owner sets a share to edit access, the sharing service shall grant the user edit access to the document. <!-- Source: "view or edit" -->

FR-004: When an owner revokes a share, the sharing service shall remove the access of the user to the document. <!-- Source: "owners can take access back" -->

FR-005: When the sharing service grants a user access to a document, the notification service shall email the user a link to the document. <!-- Source: "people are told about a share" -->

FR-006: When an owner creates a public link for a document with an expiry date, the sharing service shall let anyone with the public link view the document. <!-- Source: "share by link" -->

FR-007: If a person opens a public link after the expiry date of the public link, then the sharing service shall refuse the public link. <!-- Source: "links expire" -->

FR-008: Withdrawn.

FR-009: When an owner opens the sharing panel of a document, the documents web app shall display each user with access to the document and the access level of the user. <!-- Source: "owners see who has access" -->

FR-010: When the access to a document changes, the sharing service shall record the change, the owner, and the time of the change in the access log. <!-- Source: "changes are logged" -->

## 4. Non-Functional Requirements

NFR-001: The sharing service shall have an availability of 99.9% per calendar month. <!-- Source: "availability" -->

NFR-002: When an owner revokes a share, the sharing service shall remove the access of the user to the document within 5 seconds of the revocation. <!-- Source: "revoking is immediate" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
