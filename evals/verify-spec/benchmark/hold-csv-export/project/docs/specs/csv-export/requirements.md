# Requirements: CSV Export

**Version:** 1.0
**Date:** 2026-11-02
**Status:** Draft

## 1. Functional Requirements

FR-001: When a user exports a report, the report exporter shall write the column names as the first row.

FR-002: When a value contains a comma, the report exporter shall enclose the value in double quotes.

FR-003: When a value is missing, the report exporter shall write an empty field.

FR-004: When a value is a date, the report exporter shall write it in the form YYYY-MM-DD.

FR-005: If a report has no rows, then the report exporter shall write the column names row and nothing else.

FR-006: If a report has more than 10,000 rows, then the report exporter shall raise `TooManyRows`.

FR-007: Where a column is marked private, the report exporter shall leave the column out. Blocked by Q-001.

## 2. Non-Functional Requirements

None.

## 3. Open Questions

Q-001: Who marks a column private, and where is the mark stored?
