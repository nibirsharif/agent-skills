# build-phase evals

Cases that run build-phase on the made-up `textstats` project in [fixture/](fixture/): a `reading-time` feature whose `tasks.md` has T-1.1 `Done`, T-1.2 and T-1.3 `Todo`, and T-1.4 as the verify task. A gap is planted on purpose: T-1.1 is marked `Done`, but `reading_time` rounds down and its only test passes at exactly 200 words, so FR-001 is unmet once verify-spec runs. FR-004 is blocked by Q-001.

[config.json](config.json) allows the Agent tool, file edits, and git (never needed for pushing), since the subagents do the work under the same permissions. The prompt is the slash command, because build-phase is user-only.

| Case | Tests |
|------|-------|
| `rework-recovers` | The whole loop: T-1.2 and T-1.3 are implemented in subagents, verify-spec finds the FR-001 gap, a `Reopen T-1.1` commit changes only Status, T-1.1 is reworked, verify-spec runs again with FR-001, FR-002, FR-003 met, and the verify task runs last. The reply is `done` with the `Next:` line. |
| `manual-check-done` | Its `committed/` folder adds a `report-page` feature whose FR-002 (a Copy button) has a `manual:` check, because the project has no browser test runner. verify-spec gives FR-002 `untested`; no task is reopened, and the reply is `done` with a `Check by hand: FR-002: ...` line. |
| `round-limit` | Its `committed/` config sets `build_max_rework_rounds: 0`, which `find_tasks.py` prints as `rounds 0`. T-1.2 and T-1.3 are implemented, verify-spec finds the FR-001 gap, and the run stops with `FR-001 still not met after 0 rework rounds`: no Reopen commit, no rework. |
| `subagent-stop-line` | Its `dirty/` folder leaves `notes.txt` uncommitted, so the first implement-task subagent replies with its uncommitted-changes stop line. The run ends with that line, its rerun command changed from implement-task to build-phase: no retry, no later task, no verify. |
| `malformed-reply-twice` | Its `committed/` folder holds a project skill named `implement-task`, a test double that changes nothing and replies with one sentence. T-1.2 is tried twice, then `Stopped: T-1.2 gave no usable reply twice`. |
| `gap-no-task` | Its `committed/` folder adds a `sentence-count` feature whose plan puts FR-001 and FR-002 in phase 1, with a build task for FR-001 only. verify-spec finds FR-002 unmet and the run stops with the no-task reason, before the verify task. |
| `no-subagents` | `"disallowed_tools"` in its `checks.json` takes the Agent tool away. The run stops after picking the phase with the no-subagents reason, and never loads implement-task or verify-spec itself. |
| `all-done` | Its `committed/` `tasks.md` has every task `Done`, and no phase is named: `find_tasks.py` prints the stopped summary with `Every task in ... is Done.`; no subagent, no change. |
| `off-phase-branch` | Its `branch/` folder leaves the run on `feature-work`, which implement-task stays on. When verify-spec finds the FR-001 gap, the run stops with `not on the phase branch`: no Reopen commit, no branch switch. |
| `bad-verify-report` | Its `committed/` folder holds a project skill named `verify-spec`, a test double whose report has FR-002 `met` with no path:line and no passed test. `parse_reply.py` rejects it; the verify is retried once, then `Verify: no usable report` and `Stopped: verify-spec gave no usable reply twice`. Without the parse step the run would see no gap and end `done`. |
| `miscounted-tally` | The same kind of test double, whose report has every row right but a Tally (2 met) that miscounts its rows (3 met); its `committed/` folder also has FR-001 already fixed, so the verify task's check passes. The report is not rejected: no retry, T-1.4 runs, and the reply is `done` with `Verify: 3 met, 1 skipped`, counted from the rows. |
| `missing-tasks` | No `tasks.md` for the feature: `Phase ? ... stopped` with the no-tasks-file reason, no subagent, no change. |
| `routing-implement-one` | Routing: a request to implement one named task. build-phase must not fire. |

Every stop reason the rules name has a case but one. No `requirements.md` is printed by `find_tasks.py` the same way the no-tasks-file stop is, and is unit-tested there rather than run. A verify-spec retry that calls a gap of its rejected first report `met` has no case: it needs a test double that answers differently the second time. The rows a rejected report keeps are unit-tested in `tests/test_parse_reply.py`.

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

The whole suite at 3 runs, 16 and 17 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.322): 26 of 27. The first attempt hit the account's usage limit, and 12 runs ended early or wrote about the limit in the summary; those four cases were run again and only the complete runs are counted.

| Case | Passed |
|---|---|
| `rework-recovers` | 3 of 3 under the old `Tasks:` check, 1 of 3 under the tighter one below, 3 of 3 after the fix below |
| `manual-check-done` | 3 of 3 |
| `missing-tasks` | 3 of 3 |
| `routing-implement-one` | 3 of 3 |
| `round-limit` | 3 of 3 |
| `subagent-stop-line` | 3 of 3 |
| `malformed-reply-twice` | 3 of 3 |
| `gap-no-task` | 2 of 3, the miss a sentence before a correct summary |
| `no-subagents` | 3 of 3 |

`rework-recovers` reported `Tasks: 3 implemented, 1 reworked` in 2 of 3 runs, counting the verify task T-1.4, which the rules leave out of both numbers. Its check accepted 2 to 9 implemented; it now requires exactly `2 implemented, 1 reworked`, and the reply contract and build-rules.md now say what each number counts, with this case as the wrong-and-right example. After that, 3 of 3 runs reported `Tasks: 2 implemented, 1 reworked` (17 November 2026, `claude-sonnet-5-5`, Claude Code 2.1.322). The other eight cases were not run again after the wording change.

`all-done` and `off-phase-branch`, 3 runs each on 17 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.322): 2 of 3 each.

- `all-done`: the miss was a sentence before a correct summary. `find_tasks.py` prints the no-tasks-file stop as a whole summary, which ended that miss for `missing-tasks`; the every-task-Done stop is still composed by the agent.
- `off-phase-branch`: every run stopped correctly. The miss was the `Verify:` line, `1 met, 1 partial, 1 skipped`: verify-spec's own Tally line was wrong (its rows give 2 met), and build-phase copied it. `parse_reply.py verify` rejects that report as invalid, which would have sent it to the retry rule, but in none of the 3 runs, nor in the `rework-recovers` run checked, did build-phase run `parse_reply.py`: the step is skipped in practice.

Two fixes followed. `find_tasks.py` prints the every-task-Done stop as a whole summary when no phase is named (`--phase` leaves it to the rules). The rules and SKILL.md say to run `parse_reply.py` on every reply, with the command written out, and to act on its `kind`; an invalid verify report twice is `Verify: no usable report` and `Stopped: verify-spec gave no usable reply twice`. `rework-recovers`, `manual-check-done`, `round-limit`, `gap-no-task`, and `off-phase-branch` now fail a run in which no `parse_reply.py verify` call appears.

After them, 17 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.322): the whole suite once, then `all-done`, `bad-verify-report`, and `off-phase-branch` twice more: 14 of 18.

| Case | Passed |
|---|---|
| `all-done` | 3 of 3 |
| `bad-verify-report` | 3 of 3 |
| `off-phase-branch` | 1 of 3 |
| `no-subagents`, `round-limit` | 0 of 1 each |
| the other seven | 1 of 1 each |

Every run that reached verify-spec ran `parse_reply.py verify`. All four misses were text around a correct summary (a sentence before it, or the gap explained after it), on stops the agent composes. `no-subagents` and `round-limit` had passed 3 of 3 before the rule change, so the longer rules may have made this more frequent; it is not yet measured at 3 runs.

From the real run in [../real-runs/2026-11-17.md](../real-runs/2026-11-17.md), implement-task's stop lines are passed on with build-phase as the command to rerun, and `subagent-stop-line` expects `... then run build-phase again.`: 3 of 3 on 17 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327).

After the fix for [#2](https://github.com/nibirsharif/agent-skills/issues/2) (a miscounted Tally is recounted, not rejected; replies reach `parse_reply.py` through a file; `bad-verify-report`'s double changed and `miscounted-tally` added), the whole suite at 3 runs on 18 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327): 33 of 39. A single pass the day before had 12 of 13, the miss `round-limit`.

| Case | Passed |
|---|---|
| `miscounted-tally` | 3 of 3 |
| `bad-verify-report` | 2 of 3, the miss a sentence before a correct summary |
| `off-phase-branch` | 1 of 3: once the gap explained after a correct summary, once verify-spec also gave FR-003 `partial` (rounding down at a custom speed), so the tally, counted right, was `1 met, 2 partial, 1 skipped` |
| `round-limit` | 0 of 3, each a sentence before a correct summary |
| the other nine | 3 of 3 each |

In every run that reached verify-spec, build-phase wrote each subagent reply to a file in its temp directory and passed that file to `parse_reply.py`. `round-limit` is the measurement the paragraph above asked for: at 3 runs, the longer rules from 0.15.0 do make a composed stop open with a sentence.

Why the composed stops got worse, from the saved transcripts: `round-limit` passed 3 of 3 on 17 November in runs that skipped `parse_reply.py verify` (the step 0.15.0 then made mandatory), and missed in every run since in which that script's JSON was the last tool result: 2 on 17 November, and 0 of 3 in the pass after the #2 fix above, in which `bad-verify-report` and `off-phase-branch` each missed once the same way. The stop is then the agent's own inference from the JSON (a gap, with `rounds 0`), and it wrote that inference out before the summary: `FR-001 is a gap, and the round limit is 0, so nothing is reopened.` Stops whose `Stopped:` line already gives the reason (`gap-no-task`) missed far less often, and stops that `find_tasks.py` prints whole not at all.

A wording fix alone (no text after the summary; the `Stopped:` line is a stop's only explanation; a wrong example of a decision written out before the summary) gave `round-limit` 2 of 3, `off-phase-branch` and `bad-verify-report` 3 of 3 each (18 November 2026, `claude-sonnet-5-5`, Claude Code 2.1.327). The miss: `Gap on FR-001 and rounds is 0, so the run stops.`

So every run that `find_tasks.py` does not stop now ends with `scripts/summary.py`, which takes the run's values and prints the summary lines; the reply is its output copied whole, and the decision to stop is made before that tool call rather than after the last one. The reply lines are unchanged. The whole suite at 3 runs on 18 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327): 36 of 36, with `round-limit` 3 of 3. Every run of the nine cases that compose their summary ran `summary.py`; `missing-tasks` and `all-done` took `find_tasks.py`'s lines, and `routing-implement-one` never loaded build-phase. This run was on master before the #2 fix was merged, so without that fix or its `miscounted-tally` case.

With the #2 fix merged in, the whole suite at 3 runs on 18 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327): 39 of 39, `miscounted-tally` and `round-limit` 3 of 3 each. Every run of the ten cases that compose their summary ran `summary.py`.

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
