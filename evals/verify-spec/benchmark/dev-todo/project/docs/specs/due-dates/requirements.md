# Requirements: Due Dates

**Version:** 1.0
**Date:** 2026-10-19
**Status:** Draft

## 1. Functional Requirements

FR-001: When a user adds a task with `--due` and a date in the form YYYY-MM-DD, the todo tool shall store that date as the task's due date.

FR-002: If a user gives `--due` a value that is not a date in the form YYYY-MM-DD, then the todo tool shall print `Invalid date: <value>` and exit with status 2.

FR-003: When a user lists overdue tasks, the todo tool shall show each task that is not done and whose due date is before today.

FR-004: When a user lists tasks, the todo tool shall show them by due date, earliest first, with tasks that have no due date last.

FR-005: When a user marks a task done, the todo tool shall record the date the task was completed.

## 2. Non-Functional Requirements

NFR-001: The todo tool shall be easy to use.

## 3. Open Questions

None.
