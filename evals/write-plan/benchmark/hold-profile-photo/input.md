Plan the implementation of the profile-photo feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/profile-photo/requirements.md:

```markdown
# Requirements Specification: Profile Photo

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Users upload a profile photo, which the product shows beside their name.

## 2. Scope

### In Scope

- Uploading, replacing, removing, and showing a profile photo

### Out of Scope

None given.

**Systems:** profile service, web app

## 3. Functional Requirements

FR-001: When a user uploads an image file as a profile photo, the profile service shall store the image file as the profile photo of the user. <!-- Source: "upload a photo" -->

FR-002: If a user uploads a file larger than 5 MB, then the profile service shall reject the file. <!-- Source: "5 MB at most" -->

FR-003: If a user uploads a file of a type other than JPEG and PNG, then the profile service shall reject the file. <!-- Source: "JPEG or PNG only" -->

FR-004: When the profile service stores a profile photo, the profile service shall create a 128 by 128 pixel thumbnail of the profile photo. <!-- Source: "small version for lists" -->

FR-005: When a user removes the profile photo, the profile service shall delete the profile photo and the thumbnail of the user. <!-- Source: "remove my photo" -->

FR-006: While a user has no profile photo, the web app shall display the initials of the user in place of the profile photo. <!-- Source: "initials when there is no photo" -->

## 4. Non-Functional Requirements

NFR-001: When the profile service stores a profile photo, the profile service shall create the thumbnail within 3 seconds of the upload for 99% of uploads. <!-- Source: "thumbnails appear quickly" -->

## 5. Open Questions

Q-001: Closed. Are animated images accepted? Answer: no, JPEG and PNG only. <!-- Source: "coverage gap in FR-003" -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
