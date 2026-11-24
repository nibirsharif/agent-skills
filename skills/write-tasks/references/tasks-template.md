# Tasks File Template

Use the template below the line for every new `tasks.md`. Everything above the line is instructions and is never copied into the file. A filled-in file is in [examples.md](examples.md#a-saved-file). To change a `tasks.md` that already exists, read [updating.md](updating.md).

- Replace every `[...]` and `<...>`, and `YYYY-MM-DD` with today's date.
- **Plan** names the version of the `plan.md` the file sits beside, so a reader can tell when the tasks are stale.
- Where there is no codebase, the Overview says so in its first sentence.
- One `### Phase <n>: <title>` per phase of the plan, with the plan's number and title.
- The file has no status of its own: only each task's **Status** says where the work stands.
- Section 3 holds the plan's `Blocked by` entries, one on each line, or `None.` when nothing is blocked.
- A new file is version 1.0.

---

# Implementation Tasks: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Plan:** plan.md, version [x.y]

## 1. Overview

[How the tasks are ordered and the existing code they build on, in one to three sentences.]

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.4 | FR-001, FR-002, NFR-001 |

## 2. Tasks

### Phase 1: [Title]

#### T-1.1: [Imperative title]

**Covers:** FR-001

**Files:** `[path]`, new: [what it is]

**Depends on:** None.

**Done when:** FR-001: [the test to add or command to run, or `manual:` and what a person does and sees]

**Status:** Todo

## 3. Blocked Requirements

Blocked by Q-001: [topic, copied from plan.md]

## 4. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial tasks from plan.md [x.y] |
