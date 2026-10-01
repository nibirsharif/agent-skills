# Plan Rules

These rules are authoritative for `write-plan`. A plan is checked against the [checklist](#validation-checklist) before it is returned.

## Reading the requirements file

`requirements.md` has three ID sequences that are never renumbered: `FR-nnn` (functional, section 3), `NFR-nnn` (non-functional, section 4), and `Q-nnn` (open questions, section 5).

- **Written requirement:** an `FR` or `NFR` line with text. These, and only these, are planned.
- **Withdrawn:** a line whose text is `Withdrawn.` is skipped. `Withdrawn. Moved to <ID>.` is skipped too; plan the new ID instead.
- **Open question:** a `Q-` line that is not `Closed.` A closed question is history; ignore it.
- **Blocked requirement:** a requirement that is not written yet because it waits on open questions. A section's `Pending:` line names only those questions (`Pending: Q-001, Q-002.`), so take the topic from each question's text and its `Source` comment. Questions on one topic block one requirement: list them together as `Blocked by Q-001, Q-002: <topic>`, with no approach, no phase, and no guess at what it will say.

The plan covers every written requirement exactly once, and plans nothing else.

## Stop and ask

- The file is missing or has no written requirement: reply with one line that names the path and suggests `write-spec`, and stop. Do not plan from the feature name, and do not ask what the feature should do.
- An open question changes the core approach: ask it in chat before planning, say the answer belongs in the requirements through `write-spec`, and write no plan. A question changes the core approach when different answers lead to a different architecture, data model, or system boundary, not merely a different value or message.
- The requirements contradict each other, or two requirements cannot both be met by one design: ask which wins. Do not pick.

Answering open questions is `write-spec`'s job. Never close, answer, or assume one.

## Exploring the code

Explore before choosing anything. Look for:

- the files and modules the requirements' systems live in, by the names the requirements use;
- existing patterns to follow (how similar features are structured, tested, and configured);
- utilities, components, and tests to reuse, instead of new ones.

Name a file or function only after you have seen it. When there is no codebase, or none of it relates to the feature, say so in the approach and plan from the requirements alone: write `None found.` for reuse. Never list a plausible-sounding file.

## Phases

A phase is one PR that can merge with every test green and leaves the product working, with a smaller feature.

1. **Group** requirements into coherent slices: the same system, flow, or data. A phase holds at most `plan_max_requirements_per_phase` requirements (default 8), counting `FR` and `NFR` IDs together. A feature that fits the limits is one phase; do not merge unrelated flows to fill a phase, and do not split a flow to shrink one below the limits.
2. **Order** phases so each depends only on earlier ones: foundations (data, interfaces) first, then behaviour, then failure handling.
3. **Split** a phase estimated at more than `plan_max_files_per_phase` files (default 10), however few requirements it has. Estimate from the code you explored: files to add or change, tests included.
4. **Place each `NFR`** in the phase of the `FR` it constrains, because the phase that builds the behaviour must meet its threshold. Give an `NFR` its own later phase only when it can be met afterwards without changing behaviour: performance tuning, availability, or an accessibility level. Say why in that phase's scope.
5. **Cover each written requirement in exactly one phase**, by ID. An `FR`/`NFR` pair for one response stays together unless step 4 separates them.

A phase is not a layer. Do not split "database", "API", "UI" into phases unless each one leaves the product working and is reviewable alone.

## What each phase holds

- **Scope:** what the phase delivers, in one or two sentences, and what it leaves for later phases.
- **Requirements:** the `FR` and `NFR` IDs it covers.
- **Size:** the estimated number of files to add or change, tests included, as `about <n> files`.
- **Reuse:** existing files, patterns, and utilities, with their paths, or `None found.` on the same line. Only code that exists before the plan counts: what an earlier phase adds is not reuse; name it in Scope or Interface and data changes.
- **Interface and data changes:** new or changed endpoints, function signatures, events, schemas, config. Name them; do not write the code.
- **Verify:** how a reviewer checks each requirement ID: the test to add, the command to run, or the behaviour to observe. A verification cites the ID it checks.
- **Open questions:** the open `Q-` IDs that touch this phase, or `None.`

## Validation checklist

Run every item on the plan before returning it.

1. Every written `FR` and `NFR` appears in exactly one phase; none is missing, none is repeated.
2. No withdrawn line and no blocked requirement appears in a phase; each blocked one has one `Blocked by` entry naming all the questions it waits on.
3. No open question is answered, closed, or assumed, and no closed question is listed as open.
4. Every phase is mergeable on its own: it depends only on earlier phases, and nothing it needs is left to a later one.
5. No phase exceeds the requirement or file limit, and each phase states its size.
6. Each `NFR` sits with the `FR` it constrains, or has a stated reason for a later phase.
7. Every file or utility named in Reuse was seen in the code. Nothing an earlier phase builds is listed as Reuse; with no codebase, every Reuse is `None found.`
8. Every requirement ID in Verify names a check a reviewer can run or observe.
9. No code, no task breakdown, and no new requirement.
