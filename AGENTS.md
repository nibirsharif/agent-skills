# Agent Skills

A personal collection of skills (`SKILL.md` folders) for coding agents such as Claude Code. Each skill is a self-contained folder that any agent supporting the Agent Skills format can load.

## Layout

- `skills/<skill-name>/`: one folder per skill, flat (no category folders). Installed by `setup.sh`.
  - `SKILL.md`: required. Frontmatter plus the instructions the agent follows.
  - `references/`: optional detail files that `SKILL.md` links to and tells the agent to read.
  - `scripts/`: optional helper scripts the skill tells the agent to run. Python 3 standard library only, and the skill must still work when the agent cannot run commands.
- `examples/example-skill/`: blank skeleton to copy when starting a new skill. Not installed.
- `tests/validate.py`: checks that apply to every skill (see below).
- `tests/test_*.py`: unit tests for a skill's scripts, run by `make test`.
- `agent-skills-config.yaml.template`: optional user settings that skills read.

## Adding a skill

1. Copy `examples/example-skill/` to `skills/<skill-name>/`.
2. Set `name` to exactly the folder name (lowercase, hyphens, at most 64 characters).
3. Write a `description` (at most 1024 characters) that says what the skill does and when to use it. The agent decides whether to load the skill from this text alone.
4. Keep `SKILL.md` short: workflow and output contract. Put long rules and examples in `references/` and link them with relative paths.
5. Run `make test`.

`make test` fails a skill when: `SKILL.md` or its frontmatter is missing; `name` is not kebab-case, is longer than 64 characters, differs from the folder name, or duplicates another skill's name; `description` is missing or longer than 1024 characters; the frontmatter has fields other than `name` and `description`; or a relative link in any `.md` file is broken or points outside the skill folder.

## Conventions

- Frontmatter has only `name` and `description`, so the skill works in any agent. Do not add tool-specific fields.
- Do not duplicate a rule in two files; state it once and link to it.
- A skill never invents values the user did not give. It asks.

## Commands

- `make test`: validate every skill and run the unit tests.
- `make install`: symlink skills into `~/.agents/skills` and `~/.claude/skills`. `make install TARGET=<dir>` installs into one directory instead.
- `make uninstall`: remove the symlinks this repo created.
