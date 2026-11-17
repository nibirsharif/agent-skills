# Implementation Plan: Note Tags

**Version:** 1.0
**Date:** 2026-03-04
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

Tags are a list on each note in the existing JSON file, added through the store. The `list` command gains a filter, and the page draws the tags it already receives in `notes.json`. One phase: the three parts share the `tags` list and are small.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Tags on notes, in the store, the command line, and the page | FR-001, FR-002, FR-003, FR-004, NFR-001 |

## 2. Phases

### Phase 1: Tags on notes

**Scope:** Save tags with a note and reject a tag over 30 characters, filter the list by tag within the time limit, and show each note's tags on the page. Removing a tag is not in the requirements.

**Requirements:** FR-001, FR-002, FR-003, FR-004, NFR-001

**Size:** about 6 files

**Reuse:**

- `notes/store.py`: `Store.load` and `Store.save` keep the notes file
- `notes/cli.py`: the `list` command
- `tests/test_store.py` and `tests/test_cli.py`: the `unittest` pattern with a temporary notes file
- `web/app.js`: `render` draws each note

**Interface and data changes:**

- `Store.add_tag(note_id, tag)` in `notes/store.py`; a note gains a `tags` list
- `list --tag <tag>` in `notes/cli.py`
- a label element for each tag in `web/app.js`, with its colours in `web/index.html`

**Verify:**

- FR-001: `add_tag` saves the tag with the note
- FR-002: a 31-character tag raises `ValueError`, and a 30-character tag is saved
- FR-003: `list --tag work` prints only the notes tagged `work`
- FR-004: the page shows each note's tags as coloured labels
- NFR-001: `list --tag` over 10,000 saved notes prints within 1 second of the command

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-04 | Initial plan from requirements.md 1.0 |
