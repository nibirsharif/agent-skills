# Requirements: Room Bookings

**Version:** 1.0
**Date:** 2026-11-20
**Status:** Draft

## 1. Functional Requirements

FR-001: When a user books a room for a time when the room is free, the booking service shall store the booking with the status `active`.

FR-002: If a room already has an active booking that overlaps the requested time, then the booking store shall reject the new booking with `RoomTaken`.

FR-003: If a user cancels a booking less than 24 hours before its start, then the booking service shall keep a late fee of 20 percent of the price and refund the rest.

FR-004: When a user cancels a booking, the booking service shall send one refund request for the booking's payment reference to the payment gateway.

FR-005: When a booking is cancelled, the booking service shall email the user a message that states the amount refunded.

FR-006: If the payment gateway rejects a refund, then the booking service shall leave the booking `active` and raise `RefundFailed`.

FR-007: When a user runs `bookings cancel <id>`, the booking tool shall cancel the booking and print the amount refunded.

## 2. Non-Functional Requirements

NFR-001: The booking store shall return the active bookings of one room among 10,000 stored bookings within 50 milliseconds.

## 3. Open Questions

None.
