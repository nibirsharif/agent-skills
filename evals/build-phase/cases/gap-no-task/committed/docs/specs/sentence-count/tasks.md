# Implementation Tasks: Sentence Count

**Version:** 1.0
**Date:** 2026-11-14
**Plan:** plan.md, version 1.0

## 1. Overview

`sentence_count` is added beside `word_count` in `textstats/counts.py`.

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.2 | FR-001 |

## 2. Tasks

### Phase 1: Sentence count

#### T-1.1: Count sentences

**Covers:** FR-001

**Files:** `textstats/counts.py`, `tests/test_counts.py`

**Depends on:** None.

**Done when:** FR-001: unit test that `sentence_count("One. Two! Three?")` returns 3 and `sentence_count("")` returns 0

**Status:** Todo

#### T-1.2: Verify the phase

**Covers:** FR-001

**Files:** None.

**Depends on:** T-1.1

**Done when:** FR-001: the phase's Verify list passes and `python3 -m unittest` is green

**Status:** Todo

## 3. Blocked Requirements

None.

## 4. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-14 | Initial tasks from plan.md 1.0 |
