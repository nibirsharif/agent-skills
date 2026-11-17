Plan the implementation of the feature-flags feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/feature-flags/requirements.md:

```markdown
# Requirements Specification: Feature Flags

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Developers turn features on for a share of users, and applications ask whether a feature is on.

## 2. Scope

### In Scope

- Creating flags, turning them on for a percentage of users, and answering applications

### Out of Scope

None given.

**Systems:** flag service

## 3. Functional Requirements

FR-001: When a developer creates a flag with a name, the flag service shall store the flag as off. <!-- Source: "new flags start off" -->

FR-002: When a developer turns a flag on for a percentage of users, the flag service shall report the flag as on for that percentage of users. <!-- Source: "roll out by percentage" -->

FR-003: When an application asks for a flag by name for a user, the flag service shall return whether the flag is on for the user. <!-- Source: "apps ask per user" -->

FR-004: If an application asks for a flag that does not exist, then the flag service shall return off. <!-- Source: "unknown flags are off" -->

## 4. Non-Functional Requirements

NFR-001: When an application asks for a flag, the flag service shall answer within 20 milliseconds of the request for 99% of requests. <!-- Source: "flag checks must be fast" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
