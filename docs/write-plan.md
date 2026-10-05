# write-plan

Instructions the agent follows: [skills/write-plan/SKILL.md](../skills/write-plan/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Reads a saved `requirements.md`, explores the codebase, and writes `plan.md`: the approach, split into phases that each merge on their own as one reviewable PR. Each phase lists the `FR` and `NFR` IDs it covers, the code to reuse, the interface and data changes, and how to verify each ID.

It plans only requirements that are written. A requirement that waits on an open question is listed as blocked, and the question is never answered here.

## When to use it

Type `/nibirsharif-skills:write-plan` (or `/write-plan` when installed from a clone). The agent never starts this skill on its own.

- Requirements exist and you want to know how to build them in reviewable steps.
- A feature is too big for one PR and you want the cut points chosen from the code, not guessed.

It does not write requirements, the per-phase task list, or code. With no `requirements.md` it replies with one line pointing you to write-spec.

## Output

When saved, a short reply: the path, one line per phase (`Phase 2: title (FR-003, NFR-001)`), then the blocked requirements and open question IDs. The full plan is in `plan.md` beside `requirements.md`. In chat only, the plan itself, starting at `## 1. Approach`.

If an open question would change the core approach (an architecture, a data model, a system boundary), it asks that question instead of planning around a guess. The answer belongs in the requirements, through write-spec.

Phase size is limited by `plan_max_requirements_per_phase` (default 8) and `plan_max_files_per_phase` (default 10); see [the config](../README.md#configuration).

## FAQ

**Where does a deadline requirement go?** An `NFR` goes in the phase of the `FR` it constrains, because that phase must meet the threshold. It gets its own later phase only when it can be met afterwards without changing behaviour, such as performance tuning.

**A requirement I added later is not in the plan.** Run it again. It extends `plan.md` and keeps phase numbers. If a new requirement could join a phase, it asks which phases have already merged before placing it.

**There is no codebase yet.** It plans from the requirements alone and says so in the first sentence of the Approach.

## Verifying results

- Every written requirement is in exactly one phase.
- No phase is over the limits, and each phase could merge without the next.
- Reused code and files named in the plan exist in the repository.
- Blocked requirements name the question they wait on.

Each phase is meant to be one PR: [implement-task](implement-task.md) builds it on its own `<feature>/phase-<n>` branch.

## Related skills

Middle of the chain: [write-spec](write-spec.md) → **write-plan** → [write-tasks](write-tasks.md). Fix a plan or a phase that is too big here, not in write-tasks: it stops and sends an oversized phase back.
