# Requirements: Temperature Alerts

**Version:** 1.0
**Date:** 2026-11-09
**Status:** Draft

## 1. Functional Requirements

FR-001: When a temperature reading is above 35.0 degrees Celsius, the greenhouse monitor shall raise a `high` alert.

FR-002: While a `high` alert is active, the greenhouse monitor shall not raise another `high` alert.

FR-003: When a temperature reading is 33.0 degrees Celsius or below while a `high` alert is active, the greenhouse monitor shall clear the `high` alert.

FR-004: If no temperature reading arrives for 120 seconds, then the greenhouse monitor shall raise a `sensor-lost` alert.

FR-005: When the greenhouse monitor raises an alert, the greenhouse monitor shall add the alert's kind and time to the alert log.

## 2. Non-Functional Requirements

NFR-001: When a temperature reading arrives, the greenhouse monitor shall process it within 10 milliseconds.

NFR-002: The greenhouse monitor shall be reliable.

## 3. Open Questions

None.
