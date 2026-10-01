# agent-skills

My skills for coding agents such as Claude Code. Each skill is a folder with a `SKILL.md` that the agent loads when the task matches its description.

## Skills

| Skill | What it does |
|-------|--------------|
| [write-spec](skills/write-spec/SKILL.md) ([docs](docs/write-spec.md)) | Writes software requirements in EARS format. Writes every requirement the input supports and asks questions for the rest instead of guessing. |
| [write-plan](skills/write-plan/SKILL.md) ([docs](docs/write-plan.md)) | Turns a saved requirements file into an implementation plan: phases that each merge as one reviewable PR, with the requirement IDs each covers. Requirements that wait on open questions are listed as blocked, not guessed. |
| [write-tasks](skills/write-tasks/SKILL.md) ([docs](docs/write-tasks.md)) | Breaks each phase of a saved plan into small, ordered, verifiable tasks in `tasks.md`: each names the requirement IDs it covers, its files, what it depends on, and a check that shows it is done. A phase too big to task goes back to write-plan. |

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
| `spec_output_dir` | write-spec | Write a requirements specification to `<spec_output_dir>/<feature-name>/requirements.md`, updating the file if it exists. Empty means reply in chat only. write-plan reads `requirements.md` from there and writes `plan.md` beside it. |
| `plan_max_requirements_per_phase` | write-plan | The most `FR` and `NFR` IDs in one phase before it is split. Default 8. |
| `plan_max_files_per_phase` | write-plan | The most files a phase may add or change, tests included, before it is split. Default 10. |
| `tasks_max_files_per_task` | write-tasks | The most files one task may add or change, tests included. Default 3. |
| `tasks_max_per_phase` | write-tasks | The most tasks one phase may have; a phase that needs more goes back to write-plan to be split. Default 12. write-tasks reads `plan.md` from `spec_output_dir` and writes `tasks.md` beside it. |

## Adding a skill

See [AGENTS.md](AGENTS.md). In short: copy `examples/example-skill/` to `skills/<name>/`, fill it in, run `make test`.

## Layout

```
skills/<skill-name>/     one folder per skill (SKILL.md, optional references/ and scripts/)
docs/<skill-name>.md      what each skill does and when to use it, for people (not installed)
examples/example-skill/  blank skeleton for new skills
tests/validate.py        checks that apply to every skill
tests/test_*.py          unit tests for skill scripts and eval cases
evals/                   eval runner and checks; evals/<skill-name>/ holds a skill's cases (not installed)
.claude-plugin/          Claude Code plugin and marketplace manifests
setup.sh                 installer (symlinks)
```

## License

[MIT](LICENSE)
