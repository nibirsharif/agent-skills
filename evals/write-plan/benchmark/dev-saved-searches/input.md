Plan the implementation of the saved-searches feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/saved-searches/requirements.md:

```markdown
# Requirements Specification: Saved Searches

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Users save a search under a name and come back to it later.

## 2. Scope

### In Scope

- Saving, renaming, deleting, listing, and running a saved search

### Out of Scope

None given.

**Systems:** search service, search page

## 3. Functional Requirements

FR-001: While a user has no saved search, the search page shall display a hint in place of the list of saved searches. <!-- Source: "a hint when nothing is saved yet" -->

FR-002: When a user deletes a saved search, the search service shall delete the saved search. <!-- Source: "delete a saved search" -->

FR-003: When a user saves a search with a name, the search service shall store the query of the search under the name. <!-- Source: "save a search" -->

FR-004: If a user saves a search with a name longer than 40 characters, then the search service shall reject the saved search. <!-- Source: "40 characters at most" -->

FR-005: If a user saves a search with a name that another saved search of the user has, then the search service shall reject the saved search. <!-- Source: "names are unique per user" -->

## 4. Non-Functional Requirements

NFR-001: When a user saves a search, the search service shall store the saved search within 1 second of the request for 99% of requests. <!-- Source: "saving is quick" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
