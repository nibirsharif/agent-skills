# Requirements: Sentence Count

**Version:** 1.0
**Date:** 2026-11-14
**Status:** Draft

## 1. Functional Requirements

FR-001: When a caller passes text to `sentence_count`, the textstats library shall return the number of sentences in it, where a sentence ends at `.`, `!`, or `?`.

FR-002: When a caller passes a list of abbreviations to `sentence_count`, the textstats library shall not end a sentence at the full stop of an abbreviation in that list.

## 2. Open Questions

None.
