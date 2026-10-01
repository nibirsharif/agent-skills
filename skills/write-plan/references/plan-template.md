# Plan File Template

Use the template below the line for every new `plan.md`. Everything above the line is instructions and is never copied into the file. Planning rules are in [plan-rules.md](plan-rules.md); a filled-in file is in [examples.md](examples.md#a-saved-file).

- Replace every `[...]` and `<...>`, and `YYYY-MM-DD` with today's date.
- `plan.md` sits next to the `requirements.md` it plans. **Requirements** names that file's version, so a reader can tell when the plan is stale.
- Fill Approach only with what the requirements and the code you read support. Where there is nothing to reuse, write `**Reuse:** None found.` on one line.
- One section per phase, numbered from 1 in build order. Every phase has all seven fields; write `None.` for one that is empty.
- Section 3 lists each requirement that waits on open questions, once, as `Blocked by <every Q- ID it waits on>: <topic>`, as [plan-rules.md](plan-rules.md#reading-the-requirements-file) says. It holds `None.` when nothing is blocked.
- Section 4 lists every open `Q-` ID from the requirements file, copied without rewording, each followed by `(touches Phase <n>)` or `(touches the blocked <topic> requirement)`, in chat replies too. Closed questions are not listed.
- A new file is version 1.0. Each update raises the minor version and adds one Revision History row naming the phases and IDs added, changed, or moved.

## Updating an existing plan

- Keep every phase number. Never renumber.
- A requirement that was blocked and is now written goes into a phase: an existing phase whose scope it fits and that the user says is not yet merged, else a new phase at the end. Ask which phases have merged before choosing; never assume. Remove its blocked entry.
- A changed requirement stays in its phase; update that phase's Verify and changes.
- A withdrawn requirement is removed from its phase; note it in the Revision History.
- Update Requirements with the new `requirements.md` version.

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
