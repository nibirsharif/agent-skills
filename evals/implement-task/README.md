# implement-task evals

Cases that exercise the implement-task skill's rules on a small made-up project, [fixture/](fixture/): a `textstats` library with a `reading-time` feature whose `requirements.md`, `plan.md`, and `tasks.md` sit under `docs/specs/`. In `tasks.md`, T-1.1 is `Done`, T-1.2 and T-1.3 depend only on it, T-1.4 is the verify task, and FR-004 is blocked by Q-001.

[config.json](config.json) names it as the `"fixture"`, so every case starts in a copy committed on `main`, and a good run creates the `reading-time/phase-1` branch and commits there. `dirty-tree`, `spec-only-dirty`, `spec-and-code-dirty`, and `config-uncommitted` have a `dirty/` folder, copied over the fixture uncommitted.

| Case | Tests |
|------|-------|
| `next-task` | No task named: implements T-1.2, the first `Todo` task whose dependency is `Done`, runs the tests, commits on `reading-time/phase-1` with a `T-1.2:` subject, stages by path, never pushes, and replies with the five-line done report. |
| `named-task` | The user names T-1.3: implements it, not T-1.2. |
| `dependency-not-done` | The user names T-1.4, whose dependencies are `Todo`: a one-line stop, no code, no commit. |
| `missing-tasks` | No `tasks.md` for the feature: a one-line stop that points to write-tasks. |
| `blocked` | The user asks for FR-004, which is blocked: a one-line stop, and Q-001 is not answered. |
| `dirty-tree` | The working tree has an uncommitted change to code: a one-line stop before any change, and the change is left alone. |
| `config-uncommitted` | `.agent-skills-config.yaml` has uncommitted changes: the task runs as usual, and the file is never staged. From the Stage 5 real run ([evals/real-runs/2026-11-17.md](../real-runs/2026-11-17.md)). |
| `spec-only-dirty` | Only the feature's `plan.md` is uncommitted, as after write-tasks: commits it as `Add reading-time spec`, then implements T-1.2 and commits it. |
| `spec-and-code-dirty` | The spec and a code file are both uncommitted: a one-line stop naming only the code file, no spec commit, no branch switch. |
| `test-command` | The project config sets `test_command`: the skill runs that exact command, and the done report's Check line names it. |
| `test-leftover` | Running the tests writes `.last-test-run`, which the project neither commits nor ignores: the skill never commits it, removes it by path with `git clean` after the task's commit, and does not mention it. From the Stage 5 real run ([#4](https://github.com/nibirsharif/agent-skills/issues/4)), where `uv.lock` stopped the next task. |
| `service-missing` | The tests need a cache server on `127.0.0.1:6399`, and none is running: before editing anything, the skill stops with the missing-service line, not `check failed`. It starts no server, edits no code or test, commits no task, and removes nothing tracked. From the Stage 5 real run ([#5](https://github.com/nibirsharif/agent-skills/issues/5)), where one task started a PostgreSQL container and the next reported a failed check. |
| `origin-head` | The case's `default-branch` file makes `master` the default branch, which `origin/HEAD` names, beside a stale local `main` at an older, empty commit; the run starts on `master`. The skill takes `master` as the default, creates `reading-time/phase-1` from it, and never touches `main`. From the Stage 5 real run ([#7](https://github.com/nibirsharif/agent-skills/issues/7)), where the rule's order would have cut phase 1 from the stale `main`. |
| `routing-implement` | Routing: a request to do the next task, without naming the skill. The skill must fire. |
| `routing-tasks` | Routing: a request to write the task list, which the skill's description excludes. The skill must not fire. |

Known, on 15 November 2026 with Claude Code 2.1.322, `blocked` and `missing-tasks` at 3 runs each: 2 of 6 on `claude-sonnet-5-5` and 5 of 6 on `claude-sonnet-5`. Every miss was a sentence before a correct stop line. This is the opposite of build-phase, whose summary holds on `claude-sonnet-5-5` and not on `claude-sonnet-5`, so the miss is not explained by the model alone. The samples are small.

A larger sample of the same two cases on 16 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.322, 12 runs each) showed no wording that clearly helps, so none was kept:

| Wording | Passed |
|---|---|
| 0.12.0 as released | 7 of 12 (9 of 18 with the 6 runs above) |
| The rule stated once: the repeated "no sentence first" statements and the quoted wrong examples removed from `SKILL.md`, the rules, and the examples | 8 of 12 |
| Count the reply's lines before sending: 1 for a stop, 5 for a done report, delete the rest | 9 of 12 |

In the released wording's 12 runs, 2 of the 6 `missing-tasks` runs did not stop: asked for the next `invoice-export` task, which has no `tasks.md`, they implemented and committed `T-1.2` of `reading-time`, the one feature that has a task list. The checks caught both (`no task is reported done`, `nothing is committed`).

Across every saved `missing-tasks` run on `claude-sonnet-5-5` up to then, 4 of 53 did this. Two fixes were measured the same day on `missing-tasks`:

| Fix | Passed | Wrong feature | Sentence before the stop line |
|---|---|---|---|
| "Finding the files" reworded: a named feature is checked at one path only | 49 of 60 | 2 | 9 |
| `scripts/find_tasks.py` does the lookup and prints the stop line | 60 of 60 | 0 | 0 |

With the rewording alone, both wrong-feature runs ran `find . -name tasks.md`, found the one list, and used it. With the script the agent runs it first and replies with the line it prints, which also removed the sentence before the stop line in this case. The whole suite passed 11 of 11 at one run each with the script. `blocked` and the other stop lines do not come from the script, so their sentence-first rate is unchanged.

With `scripts/pick_task.py` finding the file, checking the working tree, picking the task, and printing the stop line (16 November 2026, `claude-sonnet-5-5`, Claude Code 2.1.322): the five stop-line cases (`blocked`, `dependency-not-done`, `dirty-tree`, `spec-and-code-dirty`, `missing-tasks`) passed 30 of 30 at 6 runs each, against about half before, and the whole suite 11 of 11 at one run each. The stop lines the script cannot decide (task mismatch, failed check, rework with nothing to fix) have no case and are unmeasured.

`config-uncommitted`, from the real run in [../real-runs/2026-11-17.md](../real-runs/2026-11-17.md): 3 of 3 on 17 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). In every run the commit staged only the task's files by path, so the uncommitted config file stayed out of it.

`test-leftover`, from finding D of the same run ([#4](https://github.com/nibirsharif/agent-skills/issues/4)): 3 of 3 on 18 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). Every run ran `git clean -fd -- .last-test-run` after the commit, then `git status --porcelain`. The whole suite then passed 13 of 13 at one run each.

`service-missing`, from finding E of the same run ([#5](https://github.com/nibirsharif/agent-skills/issues/5)): 3 of 3 on 18 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). Every run ran `python3 -m unittest` before any edit, started no server, and replied with the missing-service line; none switched to the phase branch, which the rules allow but do not need here. The whole suite then passed 14 of 14 at one run each.

`origin-head`, from finding I of the same run ([#7](https://github.com/nibirsharif/agent-skills/issues/7)): 3 of 3 on 18 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). Every run read `git branch -a`, which shows `origin/HEAD -> origin/master`, and created `reading-time/phase-1` from `master`. With 0.16.0's wording the same case passed 1 of 3, but only the `origin/HEAD` check tells the two wordings apart: those runs also cut the branch from `master`, because they started there and ran `git checkout -b`, so this model does not reproduce the stale-`main` base and the case cannot show that the fix prevents it. (One of those failures was a false match of the moved-branch check, since tightened.) The whole suite then passed 15 of 15 at one run each.

Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md). Checks with `"target": "trace"` read the agent's tool calls, so they show whether code was edited, tests were run, and what git did. Work through each case's "Review by hand" list: the checks cannot see the commit's contents.

```bash
make eval SKILL=implement-task
```
