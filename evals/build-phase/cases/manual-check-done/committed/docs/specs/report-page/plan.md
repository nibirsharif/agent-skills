# Implementation Plan: Report Page

**Version:** 1.0
**Date:** 2026-11-11
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

Add `render_report` in a new module beside `textstats/counts.py`. It returns one self-contained HTML page; the Copy button is a script inside that page. The project has Python unit tests and no browser test runner, and this plan adds none. One phase.

## 2. Phases

### Phase 1: Report page

**Scope:** An HTML report page with the word count, and a Copy button on it.

**Requirements:** FR-001, FR-002

**Size:** about 2 files

**Reuse:** `word_count` in `textstats/counts.py`.

**Interface and data changes:**

- `render_report(text)` in a new module `textstats/report.py`, returning the page as a string
- the word count is in `<span id="word-count">`; the button is `<button id="copy">Copy</button>`

**Verify:**

- FR-001: unit test that `render_report("one two three")` returns HTML containing `<span id="word-count">3</span>`
- FR-002: in a browser, open a page saved from `render_report("one two three")`, click Copy, and paste into a text field: `3` is pasted

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.
