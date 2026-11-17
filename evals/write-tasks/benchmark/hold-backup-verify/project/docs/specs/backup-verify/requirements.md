# Requirements Specification: Backup Verify

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

The backup tool proves that an archive is intact, and reports a nightly backup that is not.

## 2. Scope

### In Scope

- Checksums, the verify command, and reporting a failed nightly backup

### Out of Scope

None given.

**Systems:** backup tool

## 3. Functional Requirements

FR-001: When the backup tool writes an archive, the backup tool shall write the SHA-256 checksum of the archive to a file beside the archive. <!-- Source: "every archive gets a checksum" -->

FR-002: When a user runs `backup verify` on an archive whose checksum matches, the backup tool shall print `OK`. <!-- Source: "check an archive" -->

FR-003: If a user runs `backup verify` on an archive whose checksum does not match, then the backup tool shall print `CORRUPT` and exit with status 1. <!-- Source: "a bad archive is reported" -->

FR-004: If the archive of a nightly backup fails verification, then the backup tool shall email the failure to the configured address. <!-- Source: "mail me when a backup is bad" -->

FR-005: If the archive of a nightly backup fails verification, then the backup tool shall set the status light of the NAS to red. <!-- Source: "the light goes red" -->

## 4. Non-Functional Requirements

NFR-001: When a user runs `backup verify` on an archive of 1 GB, the backup tool shall print the result within 60 seconds of the command. <!-- Source: "checking must not take all night" -->

## 5. Open Questions

None.

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
