# Implementation Tasks: Reading Time

**Version:** 1.0
**Date:** 2026-09-03
**Plan:** plan.md, version 1.0
**Status:** Draft

## 1. Overview

`reading_time` is added beside `word_count` in `textstats/counts.py`, then made strict about its input, then given a speed argument.

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.4 | FR-001, FR-002, FR-003 |

## 2. Tasks

### Phase 1: Reading time

#### T-1.1: Add reading time at the default speed

**Covers:** FR-001

**Files:** `textstats/counts.py`, `tests/test_counts.py`

**Depends on:** None.

**Done when:** FR-001: unit test that 200 words take 1 minute and 201 words take 2

**Status:** Done

#### T-1.2: Reject text that is not a string

**Covers:** FR-002

**Files:** `textstats/counts.py`, `tests/test_counts.py`

**Depends on:** T-1.1

**Done when:** FR-002: unit test that `reading_time(None)` and `reading_time(42)` raise `TypeError`

**Status:** Todo

#### T-1.3: Accept a words-per-minute speed

**Covers:** FR-003

**Files:** `textstats/counts.py`, `tests/test_counts.py`

**Depends on:** T-1.1

**Done when:** FR-003: unit test that 300 words at 100 words per minute take 3 minutes

**Status:** Todo

#### T-1.4: Verify the phase

**Covers:** FR-001, FR-002, FR-003

**Files:** None.

**Depends on:** T-1.2, T-1.3

**Done when:** FR-001, FR-002, FR-003: the phase's Verify list passes and `python3 -m unittest` is green

**Status:** Todo

## 3. Blocked Requirements

Blocked by Q-001: reading speed per language

## 4. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-03 | Initial tasks from plan.md 1.0 |
