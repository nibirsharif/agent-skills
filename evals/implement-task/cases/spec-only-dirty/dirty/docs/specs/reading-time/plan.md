# Implementation Plan: Reading Time

**Version:** 1.0
**Date:** 2026-09-02
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

Add `reading_time` to `textstats/counts.py` next to `word_count`, which it builds on. One phase.

## 2. Phases

### Phase 1: Reading time

**Scope:** Reading time at the default or a given speed, and rejecting non-string input.

**Requirements:** FR-001, FR-002, FR-003

**Size:** about 2 files

**Reuse:** `word_count` in `textstats/counts.py`.

**Interface and data changes:**

- `reading_time(text, words_per_minute=200)` in `textstats/counts.py`

**Verify:**

- FR-001: unit test that 200 words take 1 minute and 201 words take 2
- FR-002: unit test that `reading_time(None)` and `reading_time(42)` raise `TypeError`
- FR-003: unit test that 300 words at 100 words per minute take 3 minutes

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001: reading speed per language

## 4. Open Questions

Q-001: Which reading speed applies to each language, and who maintains the table?

Q-001 owner: product, to answer before Phase 2 is planned.
