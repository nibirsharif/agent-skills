# Tasks File Template

Use the template below the line for every new `tasks.md`. Everything above the line is instructions and is never copied into the file. Task rules are in [task-rules.md](task-rules.md); a filled-in file is in [examples.md](examples.md#a-saved-file).

- Replace every `[...]` and `<...>`, and `YYYY-MM-DD` with today's date.
- `tasks.md` sits next to the `plan.md` it breaks down. **Plan** names that file's version, so a reader can tell when the tasks are stale.
- Overview is one to three sentences: how the tasks are ordered and the code they build on. Where there is no codebase, say so in its first sentence.
- One `### Phase <n>: <title>` per phase of the plan, with the plan's number and title. Every task has all five parts; write `None.` for an empty Depends on.
- Section 3 copies each `Blocked by` entry from the plan's section 3 word for word, once, on one line (`Blocked by Q-001, Q-002: <topic>`). It never lists the questions' text. It holds `None.` when nothing is blocked.
- A new file is version 1.0. Each update raises the minor version and adds one Revision History row naming the phases and task IDs added, changed, or removed.

## Updating an existing file

- Ask which phases have been started or merged; never assume. Tasks of those phases stay as they are, with their IDs.
- A phase whose requirements changed and has not started is re-split from the plan; its task IDs may change. Say so in the Revision History.
- A phase already started that gains a requirement gets new tasks after the existing ones, with the next numbers and a new last verify task. Earlier tasks keep their IDs.
- A new phase in the plan is appended. A requirement that left the plan is removed from its tasks; a task left with no ID is removed.
- Update Plan with the new `plan.md` version.

---

# Implementation Tasks: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Plan:** plan.md, version [x.y]
**Status:** Draft

## 1. Overview

[How the tasks are ordered and the existing code they build on, in one to three sentences.]

| Phase | Tasks | Requirements |
|-------|-------|--------------|
| 1 | T-1.1 to T-1.4 | REQ-001, REQ-002, NFR-001 |

## 2. Tasks

### Phase 1: [Title]

#### T-1.1: [Imperative title]

**Covers:** REQ-001

**Files:** `[path]`, new: [what it is]

**Depends on:** None.

**Done when:** REQ-001: [the test to add, command to run, or behaviour to observe]

## 3. Blocked Requirements

Blocked by Q-001: [topic, copied from plan.md]

## 4. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial tasks from plan.md [x.y] |
