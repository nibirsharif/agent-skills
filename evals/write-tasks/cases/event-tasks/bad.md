## 1. Overview

There is no codebase in this folder, so every file is new. One task for each requirement, then the phase check.

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.6 | FR-001, FR-002, FR-003, FR-004, NFR-001 |

## 2. Tasks

### Phase 1: Upload and delete a file

#### T-1.1: Store an uploaded file

**Covers:** FR-001

**Files:** new: `POST /files` handler, new: API test

**Depends on:** None.

**Done when:** FR-001: API test that an upload of a 1 MB file stores the file and returns its ID

**Status:** Todo

#### T-1.2: Reject an upload over 25 MB

**Covers:** FR-002

**Files:** new: size check in the `POST /files` handler, new: API test

**Depends on:** T-1.1

**Done when:** FR-002: API test that an upload of a 26 MB file is rejected with status 413 and stores nothing

**Status:** Todo

#### T-1.3: Measure the upload deadline

**Covers:** NFR-001

**Files:** new: load test script

**Depends on:** T-1.1

**Done when:** NFR-001: load test run shows 95% of uploads of a 1 MB file stored within 5 seconds of the request

**Status:** Todo

#### T-1.4: Delete a file

**Covers:** FR-003

**Files:** new: `DELETE /files/<id>` handler, new: API test

**Depends on:** T-1.1

**Done when:** FR-003: API test that a delete by the file's owner removes the file

**Status:** Todo

#### T-1.5: Reject a delete by another user

**Covers:** FR-004

**Files:** new: ownership check in the `DELETE /files/<id>` handler, new: API test

**Depends on:** T-1.4

**Done when:** FR-004: API test that a delete by a user who does not own the file is rejected with status 403 and removes nothing

**Status:** Todo

#### T-1.6: Verify the phase

**Covers:** FR-001, FR-002, FR-003, FR-004, NFR-001

**Files:** None.

**Depends on:** T-1.2, T-1.3, T-1.5

**Done when:** FR-001: T-1.1 test passes; FR-002: T-1.2 test passes; FR-003: T-1.4 test passes; FR-004: T-1.5 test passes; NFR-001: T-1.3 load test passes; the full test suite is green

**Status:** Todo

## 3. Blocked Requirements

None.
