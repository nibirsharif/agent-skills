# Updating an existing plan.md

Read this only when a `plan.md` already exists beside the requirements. The file keeps the [template](plan-template.md)'s layout.

- Keep every phase number. Never renumber.
- A requirement that was blocked and is now written goes into a phase: an existing phase whose scope it fits and that the user says is not yet merged, else a new phase at the end. Ask which phases have merged before choosing; never assume. Remove its blocked entry.
- A changed requirement stays in its phase; update that phase's Verify and changes.
- A withdrawn requirement is removed from its phase; note it in the Revision History.
- Update **Requirements** with the new `requirements.md` version.
- Each update raises the minor version and adds one Revision History row naming the phases and IDs added, changed, or moved.

Example: the plan in [examples.md](examples.md#a-saved-file) has Phase 1 and one blocked entry. After the user answers with write-spec and `FR-005` is written, the skill asks whether Phase 1 has merged; told that it has, it adds `Phase 2: Rate limiting` with `FR-005`, removes the blocked entry, raises the version to 1.1, and adds a Revision History row.
