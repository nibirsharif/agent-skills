## 1. Overview

There is no codebase in this folder, so every file is new. The export comes first, then its failure when `EXPORT_DIR` is not set, then the download, then the phase check.

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.4 | FR-001, FR-002, FR-003 |

## 2. Tasks

### Phase 1: Export and download a report

#### T-1.1: Export a report as CSV

**Covers:** FR-001

**Files:** new: `report export` command that builds the file path from `EXPORT_DIR` and `EXPORT_PREFIX`, new: CSV writer, new: integration test

**Depends on:** None.

**Done when:** FR-001: integration test that `report export 7` writes a CSV with the report's rows

**Status:** Todo

#### T-1.2: Refuse an export without EXPORT_DIR

**Covers:** FR-003

**Files:** new: the missing-folder check in the `report export` command, new: integration test

**Depends on:** T-1.1

**Done when:** FR-003: integration test that `report export 7` with `EXPORT_DIR` unset exits 1 with "EXPORT_DIR is not set" and writes no file

**Status:** Todo

#### T-1.3: Download an exported report

**Covers:** FR-002

**Files:** new: `report download` command, new: integration test

**Depends on:** T-1.1

**Done when:** FR-002: integration test that `report download 7` after an export prints the same CSV

**Status:** Todo

#### T-1.4: Verify the phase

**Covers:** FR-001, FR-002, FR-003

**Files:** None.

**Depends on:** T-1.2, T-1.3

**Done when:** FR-001: T-1.1 test passes; FR-002: T-1.3 test passes; FR-003: T-1.2 test passes; the full test suite is green

**Status:** Todo

## 3. Blocked Requirements

None.
