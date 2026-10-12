# build-phase evals

Cases that run build-phase on the made-up `textstats` project in [fixture/](fixture/): a `reading-time` feature whose `tasks.md` has T-1.1 `Done`, T-1.2 and T-1.3 `Todo`, and T-1.4 as the verify task. A gap is planted on purpose: T-1.1 is marked `Done`, but `reading_time` rounds down and its only test passes at exactly 200 words, so FR-001 is unmet once verify-spec runs. FR-004 is blocked by Q-001.

[config.json](config.json) allows the Agent tool, file edits, and git (never needed for pushing), since the subagents do the work under the same permissions. The prompt is the slash command, because build-phase is user-only.

| Case | Tests |
|------|-------|
| `rework-recovers` | The whole loop: T-1.2 and T-1.3 are implemented in subagents, verify-spec finds the FR-001 gap, a `Reopen T-1.1` commit changes only Status, T-1.1 is reworked, verify-spec runs again with FR-001, FR-002, FR-003 met, and the verify task runs last. The reply is `done` with the `Next:` line. |
| `missing-tasks` | No `tasks.md` for the feature: `Phase ? ... stopped` with the no-tasks-file reason, no subagent, no change. |
| `routing-implement-one` | Routing: a request to implement one named task. build-phase must not fire. |

[hooks.py](hooks.py) checks that the reply is only the summary, in the contract's line order. Trace checks cannot tell a subagent's edit from build-phase's own, so "build-phase edits nothing itself" is on the manual list.

Known, at 3 runs each (Sonnet): `missing-tasks` puts a sentence before the summary in about two runs in three, and one `rework-recovers` run had its implement-task subagent use `git stash`, which implement-task's rules forbid.

Case folders, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

```bash
make eval SKILL=build-phase
```
