# Agent Skills

A personal collection of skills (`SKILL.md` folders) for coding agents such as Claude Code. Each skill is a self-contained folder that any agent supporting the Agent Skills format can load.

## Layout

- `skills/<skill-name>/`: one folder per skill, flat (no category folders). Installed by `setup.sh`.
  - `SKILL.md`: required. Frontmatter plus the instructions the agent follows.
  - `references/`: optional detail files that `SKILL.md` links to and tells the agent to read.
  - `scripts/`: optional helper scripts the skill tells the agent to run. Python 3 standard library only, and the skill must still work when the agent cannot run commands.
- `docs/<skill-name>.md`: for people, not agents: what the skill does, when to use it, what to expect, common questions. Not installed. Link to `SKILL.md` for the rules rather than repeating them.
- `examples/example-skill/`: blank skeleton to copy when starting a new skill. Not installed.
- `tests/validate.py`: checks that apply to every skill (see below).
- `tests/test_*.py`: unit tests, run by `make test`: a skill's scripts, and `test_evals.py`, which checks every eval case and grades its golden and bad replies.
- `evals/`: eval cases, not installed. `run.py` runs a skill's cases through an agent and grades the replies (`make eval SKILL=<name>`); `grading.py` holds the checks and describes the `checks.json` format. Each `evals/<skill-name>/` has a `config.json` (prompt template, allowed tools, commands to count), `cases/<case>/`, an optional `hooks.py` for the skill's own reply rules, and a README.
- `agent-skills-config.yaml.template`: optional user settings that skills read.
- `.claude-plugin/`: the Claude Code plugin (`plugin.json`) and the marketplace that lists it (`marketplace.json`). `plugin.json`'s `skills` array names the released skills; a skill folder that is not listed there is a draft.

## Adding a skill

1. Copy `examples/example-skill/` to `skills/<skill-name>/`.
2. Set `name` to exactly the folder name (lowercase, hyphens, at most 64 characters).
3. Write a `description` (at most 1024 characters) that says what the skill does and when to use it. The agent decides whether to load the skill from this text alone.
4. Keep `SKILL.md` short: workflow and output contract. Put long rules and examples in `references/` and link them with relative paths.
5. Write `docs/<skill-name>.md` from the existing docs' headings: Overview, When to use it, Output, FAQ, Verifying results, Related skills.
6. Add evals in `evals/<skill-name>/`: a `config.json` and at least one case where the skill must fire, one where a close request must not fire it (`"fires": false`), and one or two that check its behaviour. Give each case that checks the reply a `golden.md`. See [evals/write-spec/](evals/write-spec/) for an example.
7. Run `make test`, then `make eval SKILL=<skill-name> RUNS=1` until it passes, then once with `RUNS=3 JUDGE=1`.
8. When the skill is ready to release, add it to the `skills` array in `.claude-plugin/plugin.json` and to `README.md`, then release (below).

`make test` fails a skill when: `SKILL.md` or its frontmatter is missing; `name` is not kebab-case, is longer than 64 characters, differs from the folder name, or duplicates another skill's name; `description` is missing or longer than 1024 characters; the frontmatter has fields other than `name`, `description`, and `disable-model-invocation`, or `disable-model-invocation` is not `true` or `false`; or a relative link in any `.md` file is broken or points outside the skill folder. It also fails when an entry in `plugin.json`'s `skills` array is not a folder directly under `skills/` with a `SKILL.md`.

## Conventions

- Frontmatter has only `name` and `description`, so the skill works in any agent. The one exception is `disable-model-invocation: true`, for a skill that should run only when the user types its name: one that takes outward or risky actions, or one the model should never pick on its own (the write-spec, write-plan, and write-tasks authoring steps: they ask questions and save files, so the user decides when they start). A user-only skill cannot be called through the Skill tool, so an eval prompt for it names it as a slash command, and it has no "fires": true routing case. Agents that do not know the field ignore it. Write such a skill's `description` for a person browsing commands, without "Use when" trigger phrases.
- The plugin manifests live in `.claude-plugin/`, never in a skill's frontmatter.
- A skill that needs another skill says "Call the Skill tool with `<name>`". It never links into another skill's folder.
- Do not duplicate a rule in two files; state it once and link to it.
- A skill never invents values the user did not give. It asks.
- A skill gets a lint script only when its output has mechanical rules that a script can check with no false positives, and eval runs show the agent breaking them. Most skills need none.

## Releasing

1. Bump `version` in `.claude-plugin/plugin.json` and in the plugin's entry in `.claude-plugin/marketplace.json`. Claude Code uses it to decide when installed users get an update, so a change without a bump never reaches them.
2. Add the changes to `CHANGELOG.md`.
3. Run `make test` and `claude plugin validate .claude-plugin/plugin.json`. Its one warning, that `CLAUDE.md` at the root is not loaded, is expected: that file is for working on this repo, not shipped with the plugin.
4. Commit, then run `claude plugin tag .` to create the release tag (it checks that both versions agree) and push the tag.

## Commands

- `make test`: validate every skill and run the unit tests. Free: no agent calls.
- `make eval SKILL=<name>`: run a skill's eval cases through Claude Code and grade them. Costs tokens. `MODEL=`, `RUNS=`, `JUDGE=1`.
- `make install`: symlink skills into `~/.agents/skills` and `~/.claude/skills`. `make install TARGET=<dir>` installs into one directory instead.
- `make uninstall`: remove the symlinks this repo created.
