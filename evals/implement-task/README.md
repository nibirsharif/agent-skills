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
| `check-commands` | The project config sets `check_commands` to a docstring check that the usual change for T-1.2 fails: the skill runs it after its change and before its commit, fixes what it reports inside the task's Files, and names the command in the Check line. From the Stage 5 real run ([#9](https://github.com/nibirsharif/agent-skills/issues/9)), where a task committed a test file that failed the project's format check. |
| `ci-checks` | No `check_commands`; the project's CI config runs the same check as a lint step, and a publish step in another job: the skill takes the lint command from the CI config, runs it before its commit, and never runs the publish step. |
| `check-fails` | The configured check already fails on `main`, in a file outside the task's Files: before editing anything, the skill stops with the failed-check line naming the command. It does not fix the other file, and commits nothing. |
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

Shorter rules, the next piece of [#24](https://github.com/nibirsharif/agent-skills/issues/24), 19 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). `implement-rules.md` went from 1,947 to 1,501 words: each rule is stated once, the settings lookup is named once, the branch rule is a short list, and the two wrong stop-line examples are one. What `pick_task.py` decides (finding `tasks.md`, the working-tree check, picking the task, and the eight stop lines it prints) moved to `without-commands.md` (573 words), read only when the script cannot run. With `SKILL.md` (1,256 to 1,079) and `examples.md` (660, unchanged), a run reads 3,240 words where it read 3,863. The rules file is a quarter shorter, not the third aimed for: what is left is the reply and commit formats, the default-branch wording shared with verify-spec, and rules stated nowhere else, several of which no case covers (rework, manual checks, the verify task, task mismatch, a failed check).

The whole suite at 3 runs:

| Wording | Passed |
|---|---|
| Before the change | 45 of 45 |
| First cut | 44 of 45: `service-missing` 2 of 3, a sentence before a correct stop line (`Missing service: tests need a server on 127.0.0.1:6399.`) |
| Final: the first cut with two `SKILL.md` texts restored | 45 of 45 |

The first cut had also taken out of `SKILL.md` the `Work silently` paragraph and, from the workflow step that runs the tests before editing, the sentence that names the missing-service stop. `service-missing` run alone:

| Wording | Passed |
|---|---|
| Before the change | 11 of 12 (17 of 18 with the 6 runs recorded above) |
| First cut | 7 of 9 (9 of 12 with the suite's 3) |
| Final | 8 of 9 (11 of 12 with the suite's 3) |

The four misses in this table had a correct reply and one cause, on the old wording as on the new: the first test run was piped through `tail -3`, which shows only `FAILED (errors=1)`, and the agent added the task's test before reading why. It then read the error, undid its edit (three times with `git checkout --`, which the check for a reset catches), and stopped with the right line. So the case misses about 1 run in 12 with the rules as they were, and a suite at 3 runs will sometimes show it. The first cut's 3 misses in 12 against 1 in 18 is a small sample, but both removed texts bear on what missed, so both are back, with `as the tree stands` and `the code was never tested` in the missing-service rule. The rules do not yet say to read why a run failed before editing; that would be a new rule, not a trim. The one miss before the change also failed the stand-in-server check falsely: its pattern `ncat` matches `\ncat >>` in a command with a line break.

In the final suite run, every run that loaded the skill ran `pick_task.py` (42 of 45; the other three are `routing-tasks`), and none read `without-commands.md`: the harness always allows commands, so that file, and the pasted-task-list path that now reads it, have no case. Also cut with no case that would show a difference: the second and later phases' branch base (the fixture has one phase), `Later runs find a clean tree and make no spec commit`, and the examples `podman run` and `pg_ctl` in the missing-service rule.

`check-commands`, `ci-checks`, and `check-fails`, from finding L of the real run ([#9](https://github.com/nibirsharif/agent-skills/issues/9)): 9 of 9 at 3 runs each on 23 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). Every run ran `python3 tools/check_docstrings.py` once before any edit; the six that built the task ran it again after the last edit of `counts.py` and before the commit, and named it in the Check line. No `ci-checks` run ran the publish step, and no `check-fails` run edited a file. The whole suite then passed 18 of 18 at one run each. Two things the runs show that the checks do not:

- Only one of the six building runs saw the check fail on its own change and fixed it (a `ci-checks` run: the docstring, inside the task's Files). The other five had read `tools/check_docstrings.py` before editing and named `TypeError` in the docstring at the first edit, so the cases show that the check runs, less often that a failure is fixed.
- All six building runs set Status to `Done` in `tasks.md` before their last run of the tests and the check, and the one that saw the check fail set it between the failure and the fix. Every check passed before the commit, so nothing wrong was committed, but the workflow sets Status only after every check passes. No case checks that order.

The rule adds 137 words to what every run reads (3,377, from 3,240), so the skill's word budget went from 3,350 to 3,480: the rule is new behaviour, and no existing rule could carry it.

Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md). Checks with `"target": "trace"` read the agent's tool calls, so they show whether code was edited, tests were run, and what git did. Work through each case's "Review by hand" list: the checks cannot see the commit's contents.

```bash
make eval SKILL=implement-task
```
