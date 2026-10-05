# implement-task evals

Cases that exercise the implement-task skill's rules on a small made-up project, [fixture/](fixture/): a `textstats` library with a `reading-time` feature whose `requirements.md`, `plan.md`, and `tasks.md` sit under `docs/specs/`. In `tasks.md`, T-1.1 is `Done`, T-1.2 and T-1.3 depend only on it, T-1.4 is the verify task, and FR-004 is blocked by Q-001.

[config.json](config.json) names it as the `"fixture"`, so every case starts in a copy committed on `main`, and a good run creates the `reading-time/phase-1` branch and commits there. `dirty-tree`, `spec-only-dirty`, and `spec-and-code-dirty` have a `dirty/` folder, copied over the fixture uncommitted.

| Case | Tests |
|------|-------|
| `next-task` | No task named: implements T-1.2, the first `Todo` task whose dependency is `Done`, runs the tests, commits on `reading-time/phase-1` with a `T-1.2:` subject, stages by path, never pushes, and replies with the five-line done report. |
| `named-task` | The user names T-1.3: implements it, not T-1.2. |
| `dependency-not-done` | The user names T-1.4, whose dependencies are `Todo`: a one-line stop, no code, no commit. |
| `missing-tasks` | No `tasks.md` for the feature: a one-line stop that points to write-tasks. |
| `blocked` | The user asks for FR-004, which is blocked: a one-line stop, and Q-001 is not answered. |
| `dirty-tree` | The working tree has an uncommitted change to code: a one-line stop before any change, and the change is left alone. |
| `spec-only-dirty` | Only the feature's `plan.md` is uncommitted, as after write-tasks: commits it as `Add reading-time spec`, then implements T-1.2 and commits it. |
| `spec-and-code-dirty` | The spec and a code file are both uncommitted: a one-line stop naming only the code file, no spec commit, no branch switch. |
| `routing-implement` | Routing: a request to do the next task, without naming the skill. The skill must fire. |
| `routing-tasks` | Routing: a request to write the task list, which the skill's description excludes. The skill must not fire. |

Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md). Checks with `"target": "trace"` read the agent's tool calls, so they show whether code was edited, tests were run, and what git did. Work through each case's "Review by hand" list: the checks cannot see the commit's contents.

```bash
make eval SKILL=implement-task
```
