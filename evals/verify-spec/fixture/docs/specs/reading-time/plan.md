# Implementation Plan: Reading Time

**Version:** 1.0
**Date:** 2026-09-02
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

Add `reading_time` to `textstats/counts.py` next to `word_count`, which it builds on. Two phases: the default behaviour first, then the speed argument and the non-functional requirements.

## 2. Phases

### Phase 1: Reading time

**Scope:** Reading time at the default speed, rejecting non-string input, and empty text.

**Requirements:** FR-001, FR-002, FR-005

**Size:** about 2 files

**Reuse:** `word_count` in `textstats/counts.py`.

**Interface and data changes:**

- `reading_time(text)` in `textstats/counts.py`

**Verify:**

- FR-001: unit test that 200 words take 1 minute and 201 words take 2
- FR-002: unit test that `reading_time(None)` and `reading_time(42)` raise `TypeError`
- FR-005: unit test that `reading_time("")` is 0

**Open questions:** None.

### Phase 2: Speed argument and limits

**Scope:** A words-per-minute argument, and the speed limits.

**Requirements:** FR-003, NFR-001, NFR-002

**Size:** about 2 files

**Reuse:** `reading_time` from phase 1.

**Interface and data changes:**

- `reading_time(text, words_per_minute=200)` in `textstats/counts.py`

**Verify:**

- FR-003: unit test that 300 words at 100 words per minute take 3 minutes

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001: reading speed per language (FR-004)

## 4. Open Questions

Q-001: Which reading speed applies to each language, and who maintains the table?
