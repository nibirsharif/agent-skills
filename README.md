# agent-skills

My skills for coding agents such as Claude Code. Each skill is a folder with a `SKILL.md` that the agent loads when the task matches its description.

## Skills

| Skill | What it does |
|-------|--------------|
| [write-spec](skills/write-spec/SKILL.md) | Writes software requirements in EARS format. Writes every requirement the input supports and asks questions for the rest instead of guessing. |

## Install

```bash
make install
```

This symlinks every folder in `skills/` into two places, so edits in this repo take effect immediately:

- `~/.agents/skills`: the shared location for agents that read it.
- `~/.claude/skills`: Claude Code does not scan `~/.agents/skills`, so it needs its own links.

It never overwrites an existing entry it did not create, and it removes links to skills that were renamed or deleted in this repo.

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
| `spec_output_dir` | write-spec | Write requirements to `<spec_output_dir>/<feature-name>/requirements.md`, adding to the file if it exists. Empty means reply in chat only. |

## Adding a skill

See [AGENTS.md](AGENTS.md). In short: copy `examples/example-skill/` to `skills/<name>/`, fill it in, run `make test`.

## Layout

```
skills/<skill-name>/     one folder per skill (SKILL.md, optional references/)
examples/example-skill/  blank skeleton for new skills
tests/validate.py        checks that apply to every skill
setup.sh                 installer (symlinks)
```

## Acknowledgements

- [write-spec](skills/write-spec/SKILL.md) is based on the [EARS Specification Writer prompt](https://gist.github.com/tsaqib/03080922501618c3594678551b8c3810) by [@tsaqib](https://github.com/tsaqib).
- EARS (Easy Approach to Requirements Syntax) was created by [Alistair Mavin](https://alistairmavin.com/ears/) and colleagues at Rolls-Royce.
