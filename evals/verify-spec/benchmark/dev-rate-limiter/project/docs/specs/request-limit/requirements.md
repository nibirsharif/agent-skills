# Requirements: Request Limit

**Version:** 1.0
**Date:** 2026-10-05
**Status:** Draft

## 1. Functional Requirements

FR-001: When a client makes a request and has made fewer than 5 requests in the last 60 seconds, the limiter shall accept the request.

FR-002: If a client makes a request and has already made 5 requests in the last 60 seconds, then the limiter shall raise `RateLimited` with the number of seconds until the next request will be accepted in its `retry_after` attribute.

FR-003: When 60 seconds have passed since a request, the limiter shall no longer count that request against the client.

FR-004: Where an allowlist of clients is configured, the limiter shall accept every request from a client on the allowlist.

## 2. Non-Functional Requirements

NFR-001: While 10,000 clients are tracked, the limiter shall answer a call to `check` within 1 millisecond.

## 3. Open Questions

None.
