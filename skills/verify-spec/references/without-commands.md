# Without check_scope.py

Read this only when you cannot run commands, so [check_scope.py](../scripts/check_scope.py) cannot run. You then do by hand what the script does, in the order below. Every rule in [verify-rules.md](verify-rules.md) holds unchanged.

## Find requirements.md

1. A path the user names in this request. If no file is there, reply with the no-requirements-file stop line for that path.
2. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root.
   - **The user names a feature:** the file is `<spec_output_dir>/<feature-name>/requirements.md` and no other. Check that one path and do not look for other `requirements.md` files. If it does not exist, reply with the no-requirements-file stop line for that path.
   - **The user names no feature:** list the existing `<spec_output_dir>/*/requirements.md` files; if only one exists, use it, otherwise ask which one.
3. None of these: a path from earlier in this conversation, as [SKILL.md](../SKILL.md#finding-the-files) says, else ask for the path.

## Check the scope

Stop at the first of these that holds:

1. The file has no line that starts with an `FR-<n>:` or `NFR-<n>:` ID.
2. The user names an ID that is not in the file.
3. The user names a phase, and no `plan.md` is beside the file.
4. The user names a phase that `plan.md` does not have.

Otherwise the scope is the named ID, the named phase, or the whole file, as [the rules](verify-rules.md#choosing-the-scope) say.

## The stop lines the script prints

Reply with the line alone: no text before or after it, and no backticks around it (they only mark the line here). In the last two, `<path>` is the path of `plan.md`.

- No requirements file: `No requirements file found at <path>. Run write-spec first, then run verify-spec again.`
- No requirement IDs: `<path> has no FR or NFR requirements. Run write-spec first, then run verify-spec again.`
- No such ID: `No requirement <ID> in <path>.`
- Phase named, no plan: `No plan file found at <path>, so phase <n> has no requirements list. Run write-plan first, then run verify-spec again.`
- No such phase: `No phase <n> in <path>.`
