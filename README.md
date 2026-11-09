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

Each skill is a folder with a `SKILL.md` that the agent loads when the task matches its description. Start with `/nibirsharif-skills:write-spec` on a feature description.

Requirements are written in [EARS](https://alistairmavin.com/ears/) (Easy Approach to Requirements Syntax): one `shall` sentence per requirement, with a fixed pattern for its trigger or condition, for example `When a user submits the reset form, the auth service shall send a reset link to the address.`

## Skills

| Skill | What it does |
|-------|--------------|
| [write-spec](skills/write-spec/SKILL.md) ([docs](docs/write-spec.md)) | Writes software requirements in [EARS](https://alistairmavin.com/ears/) format. Writes every requirement the input supports and asks questions for the rest instead of guessing. |
| [write-plan](skills/write-plan/SKILL.md) ([docs](docs/write-plan.md)) | Turns a saved requirements file into an implementation plan: phases that each merge as one reviewable PR, with the requirement IDs each covers. Requirements that wait on open questions are listed as blocked, not guessed. |
| [write-tasks](skills/write-tasks/SKILL.md) ([docs](docs/write-tasks.md)) | Breaks each phase of a saved plan into small, ordered, verifiable tasks in `tasks.md`: each names the requirement IDs it covers, its files, what it depends on, and a check that shows it is done. A phase too big to task goes back to write-plan. |
| [implement-task](skills/implement-task/SKILL.md) ([docs](docs/implement-task.md)) | Implements one task from `tasks.md`: only its files, with the test its check names, then marks it `Done` and commits it on the feature branch. Stops with one line when the task cannot be done as written. Never pushes. |
| [verify-spec](skills/verify-spec/SKILL.md) ([docs](docs/verify-spec.md)) | Checks the code against a saved requirements file: one verdict per FR and NFR (`met`, `partial`, `unmet`, `untested`, `cannot tell`, `skipped`), each with `file:line` and test evidence from running the project's tests, plus changed files no requirement covers. Read-only: edits and commits nothing. |
| [build-phase](skills/build-phase/SKILL.md) ([docs](docs/build-phase.md)) | Builds one phase of `tasks.md` end to end: implement-task for each task in a fresh subagent, then verify-spec in a separate one, reopening and reworking the tasks behind any gap, up to a round limit. Stops with the phase branch ready for you to push. Never pushes or opens a PR. |

`write-spec`, `write-plan`, `write-tasks`, and `build-phase` run only when you type them (`/nibirsharif-skills:write-spec`, or `/write-spec` from a clone install): they ask questions, save files, or make many commits, so the agent never starts them on its own. `implement-task` and `verify-spec` can also be started by the agent.

## Prerequisites

- **Claude Code.** The skills are built and tested on it. `build-phase` runs other skills in subagents through Claude Code's Agent and Skill tools, so it needs Claude Code.
- **git**, for `implement-task`, `verify-spec`, and `build-phase`: they work on branches and commits.
- **Python 3** (standard library only), for the scripts that lint requirements and read replies. A skill still works when the agent cannot run commands.

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
| `tasks_max_per_phase` | write-tasks | The most tasks one phase may have; a phase that needs more goes back to write-plan to be split. Default 12. write-tasks reads `plan.md` from `spec_output_dir` and writes `tasks.md` beside it; implement-task reads `tasks.md` from there. |
| `build_max_rework_rounds` | build-phase | The most rework rounds (reopen the tasks behind a requirement verify-spec does not find met, implement them again, verify again) before the run stops. Default 2. |
| `test_command` | implement-task, verify-spec, build-phase | The command that runs the project's whole test suite, for example `make test`. Empty means the skill finds it from the README, Makefile, package scripts, or CI config. |
| `base_branch` | implement-task, verify-spec, build-phase | The branch phase branches start from and drift is compared against. Empty means `main`, `master`, or the branch `origin/HEAD` names. |
| `branch_prefix` | implement-task, build-phase | Text put in front of each phase branch name, so `<feature>/phase-<n>` becomes `<branch_prefix><feature>/phase-<n>`. Include the slash, for example `team/`. Default empty. |

## Eval results

The latest recorded run of every eval case, on Claude Sonnet 5.5 in October 2026, graded by the current checks. Most cases ran 3 times. A run passes only when every check passes: routing, the tool calls it made (for example, nothing pushed, files staged by path), and the exact reply format.

| Skill | Cases | Runs passed | Misses |
|-------|-------|-------------|--------|
| write-spec | 7 | 19 of 21 | 1 run changed the input's terms; 1 run picked the wrong EARS keyword (`Where` for a state that changes at runtime) |
| write-plan | 6 | 18 of 18 | |
| write-tasks | 7 | 21 of 21 | |
| implement-task | 11 | 29 of 33 | 4 runs added a sentence before a correct stop line |
| verify-spec | 9 | 23 of 27 | 4 runs added a sentence before a correct stop line |
| build-phase | 3 | 7 of 7 | |

In the 8 implement-task and verify-spec misses the stop line itself was right; the agent wrote a sentence before it. No run failed a safety check: none pushed, staged files with `git add -A`, edited the requirements or plan, or marked a requirement `met` without a passing test. Run them yourself with `make eval SKILL=<name> RUNS=3` (it costs tokens). The cases are in [evals/](evals/).

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
