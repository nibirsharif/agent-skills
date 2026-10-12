# Requirements: Reading Time

**Version:** 1.0
**Date:** 2026-09-01
**Status:** Draft

## 1. Functional Requirements

FR-001: When a caller passes text to `reading_time`, the textstats library shall return the whole minutes needed to read it at 200 words per minute, rounded up.

FR-002: If a caller passes a value that is not a string to `reading_time`, then the textstats library shall raise `TypeError`.

FR-003: When a caller passes a words-per-minute value to `reading_time`, the textstats library shall use that value instead of 200.

FR-004: Where a language is given, the textstats library shall use that language's reading speed. Blocked by Q-001.

## 2. Open Questions

Q-001: Which reading speed applies to each language, and who maintains the table?
