# Implementation Plan: Sentence Count

**Version:** 1.0
**Date:** 2026-11-14
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

Add `sentence_count` to `textstats/counts.py` next to `word_count`. One phase.

## 2. Phases

### Phase 1: Sentence count

**Scope:** Counting sentences, and leaving out the full stops of abbreviations the caller lists.

**Requirements:** FR-001, FR-002

**Size:** about 2 files

**Reuse:** None.

**Interface and data changes:**

- `sentence_count(text, abbreviations=())` in `textstats/counts.py`

**Verify:**

- FR-001: unit test that `sentence_count("One. Two! Three?")` returns 3 and `sentence_count("")` returns 0
- FR-002: unit test that `sentence_count("See Dr. Lee. Then go.", abbreviations=["Dr."])` returns 2

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.
