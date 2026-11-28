Break the file-upload plan into tasks. There is no codebase in this folder, and the plan is not on disk; this is docs/specs/file-upload/plan.md:

```markdown
# Implementation Plan: File Upload

**Version:** 1.0
**Date:** 2026-03-03
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

There is no codebase in this folder. One phase delivers everything that is written.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Upload and delete a file | FR-001, FR-002, FR-003, FR-004, NFR-001 |

## 2. Phases

### Phase 1: Upload and delete a file

**Scope:** Store an uploaded file and refuse one over the size limit; delete a file and refuse a delete by a user who does not own it.

**Requirements:** FR-001, FR-002, FR-003, FR-004, NFR-001

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- `POST /files` accepts one file
- `DELETE /files/<id>` deletes one file

**Verify:**

- FR-001: API test that an upload of a 1 MB file stores the file and returns its ID
- FR-002: API test that an upload of a 26 MB file is rejected with status 413 and stores nothing
- FR-003: API test that a delete by the file's owner removes the file
- FR-004: API test that a delete by a user who does not own the file is rejected with status 403 and removes nothing
- NFR-001: load test that 95% of uploads of a 1 MB file are stored within 5 seconds of the request

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial plan from requirements.md 1.0 |
```
