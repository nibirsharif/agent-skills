# Plan Rules

## Reading the requirements file

`requirements.md` has three ID sequences that are never renumbered: `FR-nnn` (functional, section 3), `NFR-nnn` (non-functional, section 4), and `Q-nnn` (open questions, section 5).

- **Written requirement:** an `FR` or `NFR` line with text. These, and only these, are planned, each in exactly one phase.
- **Withdrawn:** a line whose text is `Withdrawn.` is skipped. `Withdrawn. Moved to <ID>.` is skipped too; plan the new ID instead.
- **Open question:** a `Q-` line that is not `Closed.` A closed question is history; ignore it.
- **Blocked requirement:** a requirement that is not written yet because it waits on open questions. A section's `Pending:` line names only those questions (`Pending: Q-001, Q-002.`), so take the topic from each question's text and its `Source` comment. Questions on one topic block one requirement: list them together as `Blocked by Q-001, Q-002: <topic>`, with no approach, no phase, and no guess at what it will say.

## Stop and ask

Each stop is its line or its question from the reply contract and nothing else: no plan.

- **No requirements file, or no written requirement in it.** Do not plan from the feature name, ask what the feature should do, offer options, or draft requirements.
- **An open question changes the core approach:** different answers lead to a different architecture, data model, or system boundary, not merely a different value or message. Ask it in chat and say the answer belongs in the requirements through `write-spec`. Do not plan around a guess.
- **The requirements contradict each other,** or one design cannot meet two of them. Ask which wins. Do not pick.
- **One requirement alone needs more than `plan_max_files_per_phase` files.** Reply with exactly `<ID> needs more than <n> files on its own. Split it with write-spec, then run write-plan again.` and stop, with `<n>` the limit. Do not spread the requirement over several phases, write a phase that lists no requirement ID, or plan it as one phase over the limit. Count only what the requirement needs by its own words (14 modules, each in its own format, is at least 14 files); when the count is unsure or near the limit, plan it as one phase.

## Exploring the code

Look for:

- the files and modules the requirements' systems live in, by the names the requirements use;
- existing patterns to follow;
- utilities, components, and tests to reuse, instead of new ones.

Name a file or function only after you have seen it, never a plausible-sounding one. When there is no codebase, or none of it relates to the feature, say so in the Approach and plan from the requirements alone.

## Phases

A phase is one PR, read in one sitting, that merges with every test green and leaves the product working, with a smaller feature. It holds at most `plan_max_requirements_per_phase` requirements, `FR` and `NFR` together, and `plan_max_files_per_phase` files, tests included. Cut the fewest phases that fit: that a slice could merge alone is no reason to make it a phase, and a layer ("database", "API", "UI") is never one.

1. **Start with one phase.** A feature that fits both limits is one, however many flows it has.
2. **Cut** only what is over a limit, between two slices (a system, flow, or set of data), or inside a flow over a limit alone, where one part works without the other. A phase of one requirement cannot be cut: that is a [stop](#stop-and-ask).
3. **Count files** from the code you explored, each once per phase, so slices that share files are smaller as one phase. With no code for the feature, Size is a guess that neither cuts a phase nor keeps two apart: the requirement limit alone sizes the phases.
4. **Place each `NFR`** in the phase of the `FR` it constrains, which must meet its threshold. It gets its own later phase only when it can be met afterwards without changing behaviour: performance tuning, availability, or an accessibility level. Say why in that phase's scope.
5. **Order** phases so each depends only on earlier ones: foundations (data, interfaces) first, then behaviour, then failure handling.
6. **Merge neighbours.** In order, merge a phase and the next whenever they fit the limits together, until no pair does. A later `NFR` phase stays on its own.

## What each phase holds

- **Scope:** what the phase delivers, in one or two sentences, and what it leaves for later phases.
- **Requirements:** the `FR` and `NFR` IDs it covers.
- **Size:** the file estimate, as `about <n> files` and nothing more.
- **Reuse:** existing files, patterns, and utilities, with their paths, or `None found.` on the same line. Only code that exists before the plan counts: what an earlier phase adds is not reuse; name it in Scope or Interface and data changes.
- **Interface and data changes:** new or changed endpoints, function signatures, events, schemas, config.
- **Verify:** how a reviewer checks each requirement ID: the test to add, the command to run, or the behaviour to observe.
- **Open questions:** the open `Q-` IDs that touch this phase, or `None.`

## Validation checklist

Run every item on the plan before returning it.

1. Every written `FR` and `NFR` appears in exactly one phase.
2. No withdrawn line and no blocked requirement appears in a phase; each blocked one has one `Blocked by` entry naming all the questions it waits on.
3. No open question is answered, closed, or assumed, and no closed question is listed as open.
4. Every phase depends only on earlier phases: nothing it needs is left to a later one.
5. No phase exceeds a limit that applies, each states its size and lists at least one requirement ID, and no two neighbours fit the limits as one, except a later `NFR` phase.
6. Each `NFR` sits with the `FR` it constrains, or has a stated reason for a later phase.
7. Every file or utility named in Reuse was seen in the code, and none is built by an earlier phase; with no codebase, every Reuse is `None found.`
8. Every requirement ID in Verify names a check a reviewer can run or observe.
9. No code, no task breakdown, and no new requirement.
