# build-phase

Instructions the agent follows: [skills/build-phase/SKILL.md](../skills/build-phase/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Builds one phase of a saved `tasks.md` from its first `Todo` task to a verified phase branch. It does no implementing or verifying itself. Each build task runs in a fresh subagent that calls [implement-task](implement-task.md), one at a time. When the build tasks are `Done`, a separate subagent calls [verify-spec](verify-spec.md) for the phase. Every requirement that is `unmet` or `partial`, or `untested` where a test can close it, reopens the build tasks behind it, which run again with the gap rows as context, and the phase is verified again. This repeats up to `build_max_rework_rounds` times (default 2). With no gaps left, the phase's verify task runs last.

A requirement that only a person can check is not reworked: it stays `untested`, the phase can still end as done, and the summary tells you what to check by hand. The rule is in [build-rules.md](../skills/build-phase/references/build-rules.md#manual-checks).

It never pushes, never opens a PR, and never changes requirements, the plan, or task text. The only thing it edits is the `Status` line of a task it reopens, in a commit of its own.

You start it by typing its name (`/nibirsharif-skills:build-phase`, or `/build-phase` from a clone), with the feature and optionally the phase: `/nibirsharif-skills:build-phase reading-time, phase 1`. The agent never starts it on its own, since it makes many commits.

## When to use it

- You have a `tasks.md` from [write-tasks](write-tasks.md) and want a whole phase built and checked without running implement-task and verify-spec by hand.
- You want gaps found by a verifier that did not write the code, and fixed before you review.

For one task, use implement-task. For a check without building, use verify-spec.

## Output

Five lines or more:

```
Phase 1 of reading-time: done
Branch: reading-time/phase-1
Tasks: 2 implemented, 1 reworked
Verify: 3 met, 1 skipped
Next: push reading-time/phase-1, open a PR titled "reading-time phase 1: Reading time", and run /code-review
```

When a requirement has a manual check, one line per requirement follows `Verify:`, with the check copied from the task:

```
Verify: 6 met, 2 untested
Check by hand: FR-007: in the browser, open a link older than 24 hours: the page shows "Expired"
Check by hand: FR-008: in the browser, open a revoked link: the page shows "Revoked"
```

The phase is done for the agent, not for you, until you have made those checks.

`Tasks:` counts build tasks only. When the run stops, the first line says `stopped`, a `Stopped:` line gives the reason, and there is no `Next:` line. The phase is `?` when the run stopped before one was picked. Reasons include any stop line from implement-task or verify-spec (never retried), an unusable reply twice, a gap that no task of the phase covers, and gaps left after the round limit.

## FAQ

**Why a separate subagent for verify-spec?** So the check is not made by the context that wrote the code.

**Why does the driver reopen tasks, not verify-spec?** verify-spec stays read-only and never reads `tasks.md`. Reopening is bookkeeping, so it belongs to the driver.

**Why is the verify task last?** It runs the plan's Verify list, which fails by design while a gap is open. It runs once, after verify-spec reports no gaps.

**Why is the phase `done` with an `untested` requirement?** Its tasks mark the check as `manual:`, so no test can make it `met` and a rework would only fail. verify-spec's verdict is unchanged and shown in the tally. `unmet` and `partial` rows are always reworked, manual check or not.

**My `tasks.md` was written before 0.12.0 and a phase stops on an `untested` row. What now?** A check without the word `manual:` is treated as a missing test, as before. If the check really needs a person, add `manual:` after the ID in that task's Done when (and in the verify task's), then run build-phase again. If a test could make it, add the runner through [write-plan](write-plan.md) instead.

**Does it fix a `cannot tell` or `skipped` row?** No. A vague requirement needs [write-spec](write-spec.md), and a blocked one needs its question answered. They show only in the tally.

**Which branch does it use?** The one implement-task picks, `<feature>/phase-<n>`. The reopen commits go there too.

**Can I raise the rework limit?** Yes: set `build_max_rework_rounds` in `.agent-skills-config.yaml`. `test_command`, `base_branch`, and `branch_prefix` there also apply to the subagents.

**What does a run cost?** Each task and each verify is its own agent run. In the eval fixture (two tasks, one rework) a run took about two minutes and under a dollar.

## Verifying results

- `git log` on the phase branch shows one commit per task, any `Reopen T-…: …` commit that changes only Status lines, the rework commits, and the verify task's commit last.
- The last verify report has no `unmet` or `partial` row, and every `untested` row has a `Check by hand:` line.
- You made each `Check by hand:` check yourself.
- Nothing was pushed.
- The `Verify:` line matches the tally of a verify-spec run you start yourself.

## Related skills

Drives [implement-task](implement-task.md) and [verify-spec](verify-spec.md) over the output of [write-tasks](write-tasks.md). Its evals are in [evals/build-phase/](../evals/build-phase/README.md).
