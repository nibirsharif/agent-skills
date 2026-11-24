# Plan File Template

Use the template below the line for every new `plan.md`. Everything above the line is instructions and is never copied into the file. A filled-in file is in [examples.md](examples.md#a-saved-file). To change a `plan.md` that already exists, read [updating.md](updating.md).

- Replace every `[...]` and `<...>`, and `YYYY-MM-DD` with today's date.
- **Requirements** names the version of the `requirements.md` the file sits beside, so a reader can tell when the plan is stale.
- One section per phase, numbered from 1 in build order. Every phase has all seven fields; write `None.` for one that is empty, and `**Reuse:** None found.` on one line where there is nothing to reuse.
- Section 3 lists each blocked requirement once, as `Blocked by <every Q- ID it waits on>: <topic>`, or holds `None.` when nothing is blocked.
- Section 4 lists every open `Q-` ID from the requirements file, copied without rewording, each followed by `(touches Phase <n>)` or `(touches the blocked <topic> requirement)`, in chat replies too. Closed questions are not listed.
- A new file is version 1.0.

---

# Implementation Plan: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Requirements:** requirements.md, version [x.y]
**Status:** Draft

## 1. Approach

[The overall approach in 2 to 5 sentences: what is built, in what order, and the existing code it builds on.]

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | [title] | FR-001, FR-002, NFR-001 |

## 2. Phases

### Phase 1: [Title]

**Scope:** [What this phase delivers, and what it leaves for later phases.]

**Requirements:** FR-001, FR-002, NFR-001

**Size:** about [n] files

**Reuse:**

- `[path]`: [what to reuse it for]

**Interface and data changes:**

- [new or changed endpoint, signature, event, schema, or config]

**Verify:**

- FR-001: [the test to add, command to run, or behaviour to observe]

**Open questions:** None.

## 3. Blocked Requirements

Blocked by Q-001: [the blocked requirement's topic, from the questions it waits on]

## 4. Open Questions

Q-001: [the open question, as written in requirements.md] (touches Phase 1)

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial plan from requirements.md [x.y] |
