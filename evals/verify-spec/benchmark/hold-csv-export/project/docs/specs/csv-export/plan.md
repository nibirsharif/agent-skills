# Implementation Plan: CSV Export

**Version:** 1.0
**Date:** 2026-11-03
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

One function, `export`, in `reports/export.py`. Phase 1 writes rows as text; phase 2 handles the values that need care and the size limit.

## 2. Phases

### Phase 1: Rows as text

**Scope:** The header row and quoting.

**Requirements:** FR-001, FR-002

**Size:** about 2 files

**Reuse:** None.

**Interface and data changes:**

- `export(columns, rows)` in `reports/export.py`

**Verify:**

- FR-001: unit test that the first row is the column names
- FR-002: unit test that a value with a comma is quoted

**Open questions:** None.

### Phase 2: Values and limits

**Scope:** Missing values, dates, a report with no rows, and the row limit.

**Requirements:** FR-003, FR-004, FR-005, FR-006

**Size:** about 2 files

**Reuse:** `export` from phase 1.

**Interface and data changes:**

- `TooManyRows` in `reports/export.py`

**Verify:**

- FR-003: unit test that `None` gives an empty field
- FR-004: unit test that a date is written as YYYY-MM-DD
- FR-005: unit test that no rows gives the header row alone
- FR-006: unit test that 10,001 rows raise `TooManyRows`

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001: private columns (FR-007)

## 4. Open Questions

Q-001: Who marks a column private, and where is the mark stored?
