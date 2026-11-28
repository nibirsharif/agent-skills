# agent-skills

[![Test](https://github.com/nibirsharif/agent-skills/actions/workflows/test.yml/badge.svg)](https://github.com/nibirsharif/agent-skills/actions/workflows/test.yml)

Spec-driven skills for coding agents. They take a feature from a rough idea to verified code, and they stop and ask instead of guessing.

Agents given a vague request tend to invent the missing details (limits, systems, error handling), build everything in one big change, and then say it works. These skills split the work into steps that each leave a file you can read and correct:

```
idea → write-spec → write-plan → write-tasks → implement-task → verify-spec
        (EARS         (phases,      (small,       (one task,      (a verdict
       requirements)   one PR       verifiable    one commit)     per requirement,
                       each)        tasks)                        with evidence)

                      build-phase runs implement-task and verify-spec for a whole phase
```

- **Asks, never guesses.** A missing value, unit, or threshold becomes a question. No requirement is written with a number you did not give.
- **Traceable.** Every plan phase and task names the requirement IDs (`FR-001`, `NFR-002`) it covers, so verification can say which are `met`, `partial`, or `unmet`.
- **Safe by default.** Nothing pushes or opens a PR. Verification is read-only.
- **Tested.** `make test` validates every skill, and `make eval` runs each skill through an agent against graded cases: it must fire when it should, stay quiet when it should not, and keep its reply format. See [Eval results](#eval-results).

Each skill is a folder with a `SKILL.md` that the agent loads when the task matches its description. Start with `/nibirsharif-skills:write-spec` on a feature description, or see [How much of the chain to run](#how-much-of-the-chain-to-run) for a smaller change.

Requirements are written in [EARS](https://alistairmavin.com/ears/) (Easy Approach to Requirements Syntax): one `shall` sentence per requirement, with a fixed pattern for its trigger or condition, for example `When a user submits the reset form, the auth service shall send a reset link to the address.`

## How much of the chain to run

Four commands before any code is too much for a small feature. Scale the process to the change:

| Change | What to run |
|--------|-------------|
| Small change or bug fix | No spec. Write a specific prompt: name the file, describe the symptom, and say what "fixed" looks like. |
| Normal feature, one PR | `write-spec`, then ask the agent to build from `requirements.md`, then `verify-spec`. Skip the plan and the tasks. |
| Large feature, several PRs | The full chain: `write-spec`, `write-plan`, `write-tasks`, then `build-phase` for each phase, or `implement-task` and `verify-spec` by hand. |

In the middle row the build is a plain prompt, not a skill: `implement-task` and `build-phase` need a `tasks.md`. The rules they enforce are then yours to state in the prompt: work on a feature branch, commit in small steps, and do not push. `verify-spec` needs only `requirements.md`, so it works the same without a plan or a task list.

The eval results below and the recorded [real run](evals/real-runs/2026-11-17.md) cover the full chain. The middle row has no recorded run yet.

## Skills

| Skill | What it does |
|-------|--------------|
| [write-spec](skills/write-spec/SKILL.md) ([docs](docs/write-spec.md)) | Writes software requirements in [EARS](https://alistairmavin.com/ears/) format. Writes every requirement the input supports and asks questions for the rest instead of guessing. |
| [write-plan](skills/write-plan/SKILL.md) ([docs](docs/write-plan.md)) | Turns a saved requirements file into an implementation plan: phases that each merge as one reviewable PR, with the requirement IDs each covers. Requirements that wait on open questions are listed as blocked, not guessed. |
| [write-tasks](skills/write-tasks/SKILL.md) ([docs](docs/write-tasks.md)) | Breaks each phase of a saved plan into small, ordered, verifiable tasks in `tasks.md`: each builds one behaviour (a requirement with its exceptions and its threshold) and names the requirement IDs it covers, its files, what it depends on, and a check for each ID. A phase too big to task goes back to write-plan. |
| [implement-task](skills/implement-task/SKILL.md) ([docs](docs/implement-task.md)) | Implements one task from `tasks.md`: only its files, with the test its check names, then marks it `Done` and commits it on the feature branch. Stops with one line when the task cannot be done as written. Never pushes. |
| [verify-spec](skills/verify-spec/SKILL.md) ([docs](docs/verify-spec.md)) | Checks the code against a saved requirements file: one verdict per FR and NFR (`met`, `partial`, `unmet`, `untested`, `cannot tell`, `skipped`), each with `file:line` and test evidence from running the project's tests, plus changed files no requirement covers. Read-only: edits and commits nothing. |
| [build-phase](skills/build-phase/SKILL.md) ([docs](docs/build-phase.md)) | Builds one phase of `tasks.md` end to end: implement-task for each task in a fresh subagent, then verify-spec in a separate one, reopening and reworking the tasks behind any gap, up to a round limit. Stops with the phase branch ready for you to push. Never pushes or opens a PR. |

`write-spec`, `write-plan`, `write-tasks`, and `build-phase` run only when you type them (`/nibirsharif-skills:write-spec`, or `/write-spec` from a clone install): they ask questions, save files, or make many commits, so the agent never starts them on its own. `implement-task` and `verify-spec` can also be started by the agent.

## Prerequisites

- **Claude Code.** The skills are built and tested on it. `build-phase` runs other skills in subagents through Claude Code's Agent and Skill tools, so it needs Claude Code.
- **git**, for `implement-task`, `verify-spec`, and `build-phase`: they work on branches and commits.
- **Python 3** (standard library only), for the scripts that lint requirements, find the task list, read replies, and print build-phase's summary. A skill still works when the agent cannot run commands.

The other five skills are plain `SKILL.md` folders and load in any agent that reads the Agent Skills format, but they are only tested on Claude Code. Agents that ignore `disable-model-invocation` may start the user-only skills on their own.

## Install

In Claude Code, add this repo as a marketplace and install the plugin:

```
/plugin marketplace add nibirsharif/agent-skills
/plugin install nibirsharif-skills@nibirsharif
```

Skills from the plugin are named `nibirsharif-skills:<skill>`, for example `nibirsharif-skills:write-spec`.

For other agents, or to copy editable skill files into a project, use [skills.sh](https://skills.sh):

```bash
npx skills add nibirsharif/agent-skills
```

### From a clone, for working on the skills

```bash
make install
```

This symlinks every folder in `skills/` into two places, so edits in this repo take effect immediately:

- `~/.agents/skills`: the shared location for agents that read it.
- `~/.claude/skills`: Claude Code does not scan `~/.agents/skills`, so it needs its own links.

It never overwrites an existing entry it did not create, and it removes links to skills that were renamed or deleted in this repo. Do not install both the plugin and the symlinks, or Claude Code loads each skill twice.

To install into a single directory instead (check that tool's documentation for its path):

```bash
make install TARGET=<skills-dir>
```

To remove the links:

```bash
make uninstall
```

## Configuration

Optional. Copy [agent-skills-config.yaml.template](agent-skills-config.yaml.template) to `~/.agent-skills-config.yaml` (global) or `<project>/.agent-skills-config.yaml` (per project; wins over global).

| Key | Used by | Effect |
|-----|---------|--------|
| `spec_output_dir` | write-spec | Write a requirements specification to `<spec_output_dir>/<feature-name>/requirements.md`, updating the file if it exists. Empty means write-spec asks where to save. write-plan reads `requirements.md` from there and writes `plan.md` beside it. |
| `plan_max_requirements_per_phase` | write-plan | The most `FR` and `NFR` IDs in one phase before it is split. Default 8. |
| `plan_max_files_per_phase` | write-plan | The most files a phase may add or change, tests included, before it is split. Default 10. |
| `tasks_max_files_per_task` | write-tasks | The most files one task may add or change, tests included. Default 3. |
| `tasks_max_per_phase` | write-tasks | The most tasks one phase may have; a phase that needs more goes back to write-plan to be split. Default 16. write-tasks reads `plan.md` from `spec_output_dir` and writes `tasks.md` beside it; implement-task reads `tasks.md` from there. |
| `build_max_rework_rounds` | build-phase | The most rework rounds (reopen the tasks behind a requirement verify-spec does not find met, implement them again, verify again) before the run stops. Default 2. |
| `test_command` | implement-task, verify-spec, build-phase | The command that runs the project's whole test suite, for example `make test`. Empty means the skill finds it from the README, Makefile, package scripts, or CI config. |
| `check_commands` | implement-task, build-phase | A list of the project's other checks (lint, format, types), for example `ruff check .` and `ruff format --check .`. Each task runs them before it edits anything and again before its commit. Empty means the lint, format-check, and type-check commands the project's CI config runs, or none without a CI config. `none` means no checks. |
| `base_branch` | implement-task, verify-spec, build-phase | The branch phase branches start from and drift is compared against. Empty means the branch `origin/HEAD` names, else `main`, else `master`. |
| `branch_prefix` | implement-task, build-phase | Text put in front of each phase branch name, so `<feature>/phase-<n>` becomes `<branch_prefix><feature>/phase-<n>`. Include the slash, for example `team/`. Default empty. |

## Eval results

The latest recorded run of each skill's whole suite, on `claude-sonnet-5-5` with Claude Code 2.1.327 unless the row says otherwise. A run passes only when every check passes: routing, the tool calls it made (for example, nothing pushed, files staged by path), and the exact reply format. Each of these latest runs is three per case, enough to show a miss that turns up often but not a rare one; each skill's eval README in [evals/](evals/) has single cases run more often and the results on older models.

| Skill | Cases | Latest run | Notes |
|-------|-------|------------|-------|
| write-spec | 14 | 41 of 42: 3 runs each with the judge, 27 November 2026, after a script began finding the save folder and printing the location question ([#42](https://github.com/nibirsharif/agent-skills/issues/42)) | 37 of 39 on the thirteen cases before that change. The miss is `code-no-facts`, once, which opened with a sentence about the step it had just finished. `ask-location` run alone passed 18 of 20 before the change and 60 of 60 after, and 5 of 6 in two suite runs; about 1 reply in 40 that holds requirements still opens with such a sentence, which the change does not touch (see [evals/write-spec/](evals/write-spec/README.md#a-sentence-before-the-reply)). On the benchmark 0 or 1 first reply of 10 shows neither a requirement nor a draft, against 4 or 5 before drafts ([#21](https://github.com/nibirsharif/agent-skills/issues/21)), and the open decisions found are 39 to 41 of 49 against about 41 (see [after-drafts.md](evals/write-spec/benchmark/after-drafts.md)); it was not run again. The follow-up turn is not measured with drafts. |
| write-plan | 10 | 29 of 30: 3 runs each with the judge, 24 November 2026, after it began cutting the fewest phases that fit its limits ([#10](https://github.com/nibirsharif/agent-skills/issues/10)) | 29 of 30 before that change too. The miss is `ask-location`, a sentence before the location question, about 1 run in 8 as before. `multi-phase`, 19 requirements at 8 a phase, is cut into 4 phases where its golden reply had 5, and `phase-dependency` into 2 where it had 4. Its benchmark's five plans have 9 phases against 20, all in the reference ranges, and every other item holds; two new inputs with a project show the file limit cutting where there is code (see [evals/write-plan/](evals/write-plan/README.md)). A feature of many files in a large project is not measured. |
| write-tasks | 11 | 31 of 33: 3 runs each with the judge, 27 November 2026, after a task came to build one event's requirements together ([#44](https://github.com/nibirsharif/agent-skills/issues/44)) | 30 of 30 on the ten cases before that change. The misses: a `multi-phase` check that counted commas as files, since corrected, and one `oversized-phase` reply that joined two tasks to fit the limit, which run alone then passed 10 of 10. The new `event-tasks` passed 0 of 6 before the change and 8 of 8 after. On the benchmark, three runs have 105 build tasks against 141, 1.03 for each requirement against 1.38, with every ID covered and the order and the checks unchanged; the plan of the real run has 19 to 22 build tasks against 25 to 29 (see [evals/write-tasks/](evals/write-tasks/README.md)). The `ask-location` case, run alone, passed 0 of 12 before its change and 12 of 12 after ([#35](https://github.com/nibirsharif/agent-skills/pull/35)). |
| implement-task | 15 | 45 of 45: 3 runs each, 19 November 2026, after its rules were shortened | 45 of 45 before the change too. Run alone, `service-missing` misses about 1 run in 12, before and after: the agent adds the task's test before reading why the first test run failed, then undoes the edit and stops with the right line. The five stop-line cases passed 30 of 30 at 6 runs each once `pick_task.py` prints the line. |
| verify-spec | 9 | 27 of 27: 3 runs each, 26 November 2026, after three verdict rules were added ([#23](https://github.com/nibirsharif/agent-skills/issues/23)) | 27 of 27 on 19 November too, before them. Its benchmark has four harder projects besides the first six, and runs each three times. Before the rules, 203 of 213 rows were right and 9 of 129 gaps were called `met`: a check that one path skips, in 6 of 6 runs, and a rule kept outside the system the requirement names, in 3 of 6. After, 213 of 213 and none, with 70 of 71 rows the same in all three runs (see [after-verdict-rules.md](evals/verify-spec/benchmark/after-verdict-rules.md)). A project of hundreds of files is not measured. The two stop-line cases passed 12 of 12 at 6 runs each once `check_scope.py` prints the line. |
| build-phase | 14 | 41 of 42: 3 runs each, 19 November 2026, after its rules were shortened | The miss was `off-phase-branch`, with a correct reply: an implement-task subagent switched branch and back, which the check cannot tell from build-phase's own command. Run again alone, it passed 3 of 3. |

Before the lookup and summary scripts, the usual miss was a sentence written before a correct stop line or summary; the scripts now print those lines, and the eval READMEs record the rates before and after. No run failed a safety check: none pushed, staged files with `git add -A`, edited the requirements or plan, or marked a requirement `met` without a passing test. The closest was implement-task, asked for a feature with no task list, implementing another feature's task in 4 of 53 runs, which its lookup script now prevents (0 of 60; see [evals/implement-task/](evals/implement-task/README.md)). Run them yourself with `make eval SKILL=<name> RUNS=3` (it costs tokens).

## Adding a skill

See [AGENTS.md](AGENTS.md). In short: create `skills/<name>/SKILL.md` modelled on an existing skill, add its docs and evals, run `make test`.

## Layout

```
skills/<skill-name>/     one folder per skill (SKILL.md, optional references/ and scripts/)
docs/<skill-name>.md      what each skill does and when to use it, for people (not installed)
tests/validate.py        checks that apply to every skill
tests/test_*.py          unit tests for skill scripts and eval cases
evals/                   eval runner and checks; evals/<skill-name>/ holds a skill's cases (not installed)
.claude-plugin/          Claude Code plugin and marketplace manifests
setup.sh                 installer (symlinks)
```

## License

[MIT](LICENSE)
