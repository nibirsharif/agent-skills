# Changelog

Versions follow `.claude-plugin/plugin.json`. Claude Code uses that version to decide when installed users get an update, so every release bumps it.

## 0.2.0

- write-spec: non-functional requirements get their own ID sequence, `NFR-001`, `NFR-002`, …, next to `REQ-` (functional) and `Q-` (questions). Each sequence continues from its own highest ID.
- write-spec: a behaviour with a deadline or other quality threshold is split into a `REQ` for the behaviour and an `NFR` for the threshold. A timeout in a condition stays functional.
- write-spec: a requirement that moves to the other class is withdrawn with `Withdrawn. Moved to <ID>.` and written under the next ID of the other sequence.
- write-spec: files saved by 0.1.0 keep their `REQ` IDs in the Non-Functional section; new non-functional requirements start at `NFR-001`.
- write-spec lint: checks `NFR` lines, flags an `NFR` in the Functional section, and flags a deadline in a `REQ` response.

## 0.1.0

- First release as a Claude Code plugin (`nibirsharif-skills`), with one skill: `write-spec`.
