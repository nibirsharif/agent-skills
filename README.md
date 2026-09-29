# agent-skills

My skills for coding agents such as Claude Code. Each skill is a folder with a `SKILL.md` that the agent loads when the task matches its description.

## Skills

| Skill | What it does |
|-------|--------------|
| [write-spec](skills/write-spec/SKILL.md) | Writes software requirements in EARS format. Writes every requirement the input supports and asks questions for the rest instead of guessing. |

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
| `spec_output_dir` | write-spec | Write a requirements specification to `<spec_output_dir>/<feature-name>/requirements.md`, updating the file if it exists. Empty means reply in chat only. |

## Adding a skill

See [AGENTS.md](AGENTS.md). In short: copy `examples/example-skill/` to `skills/<name>/`, fill it in, run `make test`.

## Layout

```
skills/<skill-name>/     one folder per skill (SKILL.md, optional references/ and scripts/)
examples/example-skill/  blank skeleton for new skills
tests/validate.py        checks that apply to every skill
tests/test_*.py          unit tests for skill scripts and eval cases
evals/                   eval runner and checks; evals/<skill-name>/ holds a skill's cases (not installed)
.claude-plugin/          Claude Code plugin and marketplace manifests
setup.sh                 installer (symlinks)
```

## License

[MIT](LICENSE)

## Acknowledgements

- [write-spec](skills/write-spec/SKILL.md) is based on the [EARS Specification Writer prompt](https://gist.github.com/tsaqib/03080922501618c3594678551b8c3810) by [@tsaqib](https://github.com/tsaqib).
- EARS (Easy Approach to Requirements Syntax) was created by [Alistair Mavin](https://alistairmavin.com/ears/) and colleagues at Rolls-Royce.
