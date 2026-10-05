# build-phase

Instructions the agent follows: [skills/build-phase/SKILL.md](../skills/build-phase/SKILL.md). This page is for you: when to use it and what to expect. A draft: it is not yet listed in `plugin.json` or the README.

## Overview

Builds one phase of a feature from its saved `tasks.md`. For each task it starts a fresh subagent that runs [implement-task](implement-task.md), then, when the phase's tasks are all `Done`, a separate subagent that runs [verify-spec](verify-spec.md) for the phase. When a requirement is `unmet`, `partial`, or `untested`, it sets the tasks behind it back to `Todo`, commits that, and runs them again with the verify rows as context, then verifies again. After `build_max_rework_rounds` rounds (default 2) it stops instead of looping.

It stops at the phase boundary: the phase branch (`<feature>/phase-<n>`) holds the commits, ready for you to push and review as one PR. It never pushes or opens the PR.

## When to use it

- The spec, plan, and tasks are written and you want a phase built without running implement-task by hand for each task.
- You want the check in verify-spec before you review.

Type it by name (`/nibirsharif-skills:build-phase`, or `/build-phase` from a clone), with the feature and optionally the phase. The agent never starts it on its own, since it makes many commits.

## Output

```
Phase 1 of reading-time: done
Branch: reading-time/phase-1
Tasks: 4 implemented, 1 reworked
Verify: 3 met, 1 skipped
Next: push reading-time/phase-1, open a PR titled "reading-time phase 1: Reading time", and run /code-review
```

When it stops, the `Stopped:` line holds the reason: an `implement-task` stop line, a reply that was unusable twice, a gap no task covers, or the round limit.

## FAQ

**Why a separate subagent for verify-spec?** So the check is not made by the context that wrote the code.

**Why does the driver reopen tasks, not verify-spec?** verify-spec stays read-only and never reads `tasks.md`. Reopening is bookkeeping, so it belongs to the driver.

**What does a `cannot tell` row do?** Nothing: the requirement has no checkable criterion, and the fix is in write-spec.

## Verifying results

- `git log` on the phase branch shows one commit per task, plus `Reopen` and `(rework)` commits when a round happened.
- The last verify report has no `unmet`, `partial`, or `untested` row.
- Nothing was pushed.

## Related skills

Drives [implement-task](implement-task.md) and [verify-spec](verify-spec.md) after [write-tasks](write-tasks.md).
