# build-phase evals

Cases that run build-phase on the made-up `textstats` project in [fixture/](fixture/): a `reading-time` feature whose `tasks.md` has T-1.1 `Done`, T-1.2 and T-1.3 `Todo`, and T-1.4 as the verify task. A gap is planted on purpose: T-1.1 is marked `Done`, but `reading_time` rounds down and its only test passes at exactly 200 words, so FR-001 is unmet once verify-spec runs. FR-004 is blocked by Q-001.

[config.json](config.json) allows the Agent tool, file edits, and git (never needed for pushing), since the subagents do the work under the same permissions. The prompt is the slash command, because build-phase is user-only.

| Case | Tests |
|------|-------|
| `rework-recovers` | The whole loop: T-1.2 and T-1.3 are implemented in subagents, verify-spec finds the FR-001 gap, a `Reopen T-1.1` commit changes only Status, T-1.1 is reworked, verify-spec runs again with FR-001, FR-002, FR-003 met, and the verify task runs last. The reply is `done` with the `Next:` line. |
| `manual-check-done` | Its `committed/` folder adds a `report-page` feature whose FR-002 (a Copy button) has a `manual:` check, because the project has no browser test runner. verify-spec gives FR-002 `untested`; no task is reopened, and the reply is `done` with a `Check by hand: FR-002: ...` line. |
| `round-limit` | Its `committed/` config sets `build_max_rework_rounds: 0`, which `find_tasks.py` prints as `rounds 0`. T-1.2 and T-1.3 are implemented, verify-spec finds the FR-001 gap, and the run stops with `FR-001 still not met after 0 rework rounds`: no Reopen commit, no rework. |
| `subagent-stop-line` | Its `dirty/` folder leaves `notes.txt` uncommitted, so the first implement-task subagent replies with its uncommitted-changes stop line. The run ends with that line word for word: no retry, no later task, no verify. |
| `malformed-reply-twice` | Its `committed/` folder holds a project skill named `implement-task`, a test double that changes nothing and replies with one sentence. T-1.2 is tried twice, then `Stopped: T-1.2 gave no usable reply twice`. |
| `gap-no-task` | Its `committed/` folder adds a `sentence-count` feature whose plan puts FR-001 and FR-002 in phase 1, with a build task for FR-001 only. verify-spec finds FR-002 unmet and the run stops with the no-task reason, before the verify task. |
| `no-subagents` | `"disallowed_tools"` in its `checks.json` takes the Agent tool away. The run stops after picking the phase with the no-subagents reason, and never loads implement-task or verify-spec itself. |
| `missing-tasks` | No `tasks.md` for the feature: `Phase ? ... stopped` with the no-tasks-file reason, no subagent, no change. |
| `routing-implement-one` | Routing: a request to implement one named task. build-phase must not fire. |

The stop reasons the rules name each have a case, except three: no `requirements.md` (printed by `find_tasks.py` as the no-tasks-file stop is, and unit-tested there), `Every task in <path> is Done.`, and `not on the phase branch`. Those two have no case and are unmeasured.

What the four stop cases added on 16 November 2026 do not prove:

- `round-limit` runs with a limit of 0. It proves the stop line and that nothing is reopened past the limit, not a run that used its rounds and still had gaps: no fixture gap survives a rework reliably.
- `malformed-reply-twice` mocks the subagent's skill. It relies on a project skill named `implement-task` being loaded for that bare name in place of the plugin's `nibirsharif-skills:implement-task`; two trace checks fail the run when the real one loads. The retry rule for a malformed verify-spec report has no case.
- `gap-no-task` relies on T-1.1's implementer not building FR-002 on the way, which its manual list checks. FR-001 came back `partial` in 1 of 4 runs (the implementer counted punctuation marks, so `...` was three sentences); the stop is the same, and the check accepts both tallies.
- `no-subagents` is Claude Code with the tool denied, not another agent.

First runs of the five, 16 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.322):

| Case | Passed | Notes |
|---|---|---|
| `round-limit` | 0 of 1, then 1 of 1 | The first run never read `.agent-skills-config.yaml`: it reopened T-1.1, reworked it, and ended `done`, so `build_max_rework_rounds` had no effect at any value. `find_tasks.py` now prints the limit as `rounds <n>` and the rules say to stop at it; the run after that passed. |
| `subagent-stop-line` | 1 of 1 | |
| `malformed-reply-twice` | 1 of 1 | The test double loaded for the bare name `implement-task` in both subagents. |
| `gap-no-task` | 3 of 4 | The miss was a sentence before a correct summary. One pass is by the widened tally check (FR-001 `partial`). |
| `no-subagents` | 1 of 1 | |

`rework-recovers` passed 1 of 1 with the script's new `rounds` line. The other three older cases were not run again after that change, and none of the five has had 3 runs. In the failed `round-limit` run the summary also said `Tasks: 3 implemented, 1 reworked` where the rules give 2 and 1; `rework-recovers` accepts 2 to 9, so that miscount is not caught.

[hooks.py](hooks.py) grades two things apart, so a run shows which one failed: `summary: ...` when the summary lines themselves are wrong, and `outside the summary: ...` when the reply has other text, such as a sentence before a correct summary. Trace checks cannot tell a subagent's edit from build-phase's own, so "build-phase edits nothing itself" is on the manual list.

Known, at 3 runs each on 15 November 2026: 12 of 12 on `claude-sonnet-5-5` (Claude Code 2.1.322). On `claude-sonnet-5` (Claude Code 2.1.267) the same day: 7 of 12, every miss a sentence before a correct summary (`manual-check-done` 1 of 3, `rework-recovers` 1 of 3, `missing-tasks` 3 of 3). `missing-tasks` does this in most runs, on 0.11.0 as well: 16 of 20 runs that day across both versions. The rate depends on the model, not the skill version: those runs were on `claude-sonnet-5` (Claude Code 2.1.267, where `sonnet` is that model), and on `claude-sonnet-5-5` (Claude Code 2.1.322) `missing-tasks` passed 14 of 15 the same day. Three wordings were tried against `claude-sonnet-5` that day and none was kept:

| Wording | `missing-tasks` passes on `claude-sonnet-5` |
|---|---|
| 0.12.0 as released | 0 of 20, and 1 of 3 on a second machine |
| Workflow steps 1 and 6: a stop goes straight to the finish step, whose whole reply is the summary lines | 1 of 20 |
| Reply contract gives the reason: a script may read the reply line by line | 0 of 15 |
| Reply contract: the last message is the command's output, check its first word is `Phase` and delete the rest | 4 of 15, with 3 of the misses now bolding the summary lines |

To reproduce the miss on a newer Claude Code, pass `--model claude-sonnet-5`. Earlier, one `rework-recovers` run had its implement-task subagent use `git stash`, which implement-task's rules forbid.

With `scripts/find_tasks.py` doing the lookup and printing the whole stopped summary (16 November 2026, Claude Code 2.1.322), `missing-tasks` passed 12 of 20 on `claude-sonnet-5`, against 0 of 20 before and at most 4 of 15 with any wording; the 8 misses were still a sentence before a correct summary. On `claude-sonnet-5-5` it passed 10 of 10, and the whole suite 4 of 4 at one run each.

With implement-task and verify-spec starting from their own scripts (`pick_task.py`, `check_scope.py`), the whole suite passed 4 of 4 at one run each on 16 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.322).

Case folders, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

```bash
make eval SKILL=build-phase
```
