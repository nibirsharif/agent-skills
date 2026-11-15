# Implementation Tasks: Report Page

**Version:** 1.0
**Date:** 2026-11-12
**Plan:** plan.md, version 1.0

## 1. Overview

`render_report` is added in a new module that reuses `word_count`, then the page gets its Copy button. The project has no browser test runner, so the button's behaviour is a manual check.

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.3 | FR-001, FR-002 |

## 2. Tasks

### Phase 1: Report page

#### T-1.1: Render the report page

**Covers:** FR-001

**Files:** new: `textstats/report.py` with `render_report`, new: `tests/test_report.py`

**Depends on:** None.

**Done when:** FR-001: unit test that `render_report("one two three")` returns HTML containing `<span id="word-count">3</span>`

**Status:** Todo

#### T-1.2: Add the Copy button to the report page

**Covers:** FR-002

**Files:** `textstats/report.py`

**Depends on:** T-1.1

**Done when:** FR-002: manual: in a browser, open a page saved from `render_report("one two three")`, click Copy, and paste into a text field: `3` is pasted

**Status:** Todo

#### T-1.3: Verify the phase

**Covers:** FR-001, FR-002

**Files:** None.

**Depends on:** T-1.2

**Done when:** FR-001: the T-1.1 test passes and `python3 -m unittest` is green; FR-002: manual: in a browser, open a page saved from `render_report("one two three")`, click Copy, and paste into a text field: `3` is pasted

**Status:** Todo

## 3. Blocked Requirements

None.

## 4. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-12 | Initial tasks from plan.md 1.0 |
