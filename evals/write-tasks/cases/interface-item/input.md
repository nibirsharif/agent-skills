Break the report-export plan into tasks. There is no codebase in this folder, and the plan is not on disk; this is docs/specs/report-export/plan.md:

```markdown
# Implementation Plan: Report Export

**Version:** 1.0
**Date:** 2026-03-10
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

There is no codebase in this folder. One phase delivers everything that is written.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Export and download a report | FR-001, FR-002, FR-003 |

## 2. Phases

### Phase 1: Export and download a report

**Scope:** Write a report to a CSV file, read it back, and refuse an export when the export folder is not set.

**Requirements:** FR-001, FR-002, FR-003

**Size:** about 6 files

**Reuse:** None found.

**Interface and data changes:**

- `report export <id>` command writes the report as CSV
- `report download <id>` command prints the exported CSV
- `EXPORT_DIR` and `EXPORT_PREFIX` environment variables, read at start-up
- CSV header row taken from the report's column names
- `export_path(report_id)` helper that builds a report's file path from `EXPORT_DIR` and `EXPORT_PREFIX`

**Verify:**

- FR-001: integration test that `report export 7` with `EXPORT_DIR=/tmp/out` and `EXPORT_PREFIX=acme` writes `/tmp/out/acme-7.csv` with the report's rows
- FR-002: integration test that `report download 7` after an export prints the same CSV
- FR-003: integration test that `report export 7` with `EXPORT_DIR` unset exits 1 with "EXPORT_DIR is not set" and writes no file

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-10 | Initial plan from requirements.md 1.0 |
```
