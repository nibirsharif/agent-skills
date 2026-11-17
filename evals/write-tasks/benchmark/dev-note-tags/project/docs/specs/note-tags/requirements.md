# Requirements Specification: Note Tags

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Users tag notes and find notes by tag.

## 2. Scope

### In Scope

- Tags on notes, the tag filter of the list, and tags on the notes page

### Out of Scope

None given.

**Systems:** notes store, notes tool, notes page

## 3. Functional Requirements

FR-001: When a user adds a tag to a note, the notes store shall save the tag with the note. <!-- Source: "tag a note" -->

FR-002: If a user adds a tag longer than 30 characters, then the notes store shall raise `ValueError`. <!-- Source: "tags are short" -->

FR-003: When a user runs `notes list --tag` with a tag, the notes tool shall print only the notes that have the tag. <!-- Source: "find notes by tag" -->

FR-004: When a user opens the notes page, the notes page shall display the tags of each note as coloured labels. <!-- Source: "see tags on the page" -->

## 4. Non-Functional Requirements

NFR-001: When a user runs `notes list --tag` with 10,000 saved notes, the notes tool shall print the notes within 1 second of the command. <!-- Source: "stays fast with many notes" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
