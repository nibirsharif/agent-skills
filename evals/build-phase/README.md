# build-phase evals

Cases that run build-phase on the made-up `textstats` project in [fixture/](fixture/): a `reading-time` feature whose `tasks.md` has T-1.1 `Done`, T-1.2 and T-1.3 `Todo`, and T-1.4 as the verify task. A gap is planted on purpose: T-1.1 is marked `Done`, but `reading_time` rounds down and its only test passes at exactly 200 words, so FR-001 is unmet once verify-spec runs. FR-004 is blocked by Q-001.

[config.json](config.json) allows the Agent tool, file edits, and git (never needed for pushing), since the subagents do the work under the same permissions. The prompt is the slash command, because build-phase is user-only.

| Case | Tests |
|------|-------|
| `rework-recovers` | The whole loop: T-1.2 and T-1.3 are implemented in subagents, verify-spec finds the FR-001 gap, a `Reopen T-1.1` commit changes only Status, T-1.1 is reworked, verify-spec runs again with FR-001, FR-002, FR-003 met, and the verify task runs last. The reply is `done` with the `Next:` line. |
| `manual-check-done` | Its `committed/` folder adds a `report-page` feature whose FR-002 (a Copy button) has a `manual:` check, because the project has no browser test runner. verify-spec gives FR-002 `untested`; no task is reopened, and the reply is `done` with a `Check by hand: FR-002: ...` line. |
| `missing-tasks` | No `tasks.md` for the feature: `Phase ? ... stopped` with the no-tasks-file reason, no subagent, no change. |
| `routing-implement-one` | Routing: a request to implement one named task. build-phase must not fire. |

[hooks.py](hooks.py) grades two things apart, so a run shows which one failed: `summary: ...` when the summary lines themselves are wrong, and `outside the summary: ...` when the reply has other text, such as a sentence before a correct summary. Trace checks cannot tell a subagent's edit from build-phase's own, so "build-phase edits nothing itself" is on the manual list.

Known, at 3 runs each (Sonnet): 7 of 12 on 15 November 2026, every miss a sentence before a correct summary (`manual-check-done` 1 of 3, `rework-recovers` 1 of 3, `missing-tasks` 3 of 3). `missing-tasks` does this in most runs, on 0.11.0 as well: 16 of 20 runs that day across both versions. The rate depends on the machine: the same day on Linux (Claude Code 2.1.322, Sonnet 5.5, output style `default`, no user `CLAUDE.md`), `missing-tasks` on 0.12.0 passed 14 of 15 runs, the one miss again a sentence before a correct summary. No wording change was tried there, because one could not be measured against that baseline. Earlier, one `rework-recovers` run had its implement-task subagent use `git stash`, which implement-task's rules forbid.

Case folders, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

```bash
make eval SKILL=build-phase
```
