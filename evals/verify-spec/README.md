# verify-spec evals

Cases that exercise the verify-spec skill's rules on a small made-up project, [fixture/](fixture/): a `textstats` library whose `reading-time` feature has `requirements.md`, `plan.md`, and `tasks.md` under `docs/specs/`. The code has gaps planted on purpose:

| Requirement | State in the fixture | Right verdict |
|-------------|----------------------|---------------|
| FR-001 (round up at 200 wpm) | code and a passing test | `met` |
| FR-002 (`TypeError` for a non-string) | code, no test | `untested` |
| FR-003 (words-per-minute argument) | not implemented, though `tasks.md` says T-2.1 is `Done` | `unmet` |
| FR-004 (language speed) | `Blocked by Q-001` | `skipped` |
| FR-005 (empty string gives 0) | code and a passing test | `met` |
| NFR-001 ("quickly") | no criterion | `cannot tell` |
| NFR-002 (100,000 words in 100 ms) | a threshold, no benchmark | `untested` |

Plan phase 1 is FR-001, FR-002, FR-005; phase 2 is FR-003, NFR-001, NFR-002. The fixture starts on `main` with nothing uncommitted, so drift is `not checked (no feature branch)` unless a case adds an uncommitted file in its `dirty/` folder.

[config.json](config.json) allows only reading, `python3`, and read-only git, so an attempt to edit or commit shows in the transcript. Every reporting case checks the trace for edits and git writes, so none of them needs a case of its own.

| Case | Tests |
|------|-------|
| `mixed-spec` | The whole file: one row per ID with the verdicts above, the tally, and `Drift: textstats/formatting.py` for an uncommitted file no requirement covers. The Done tasks are not evidence. |
| `phase-scope` | "Verify phase 1": FR-001, FR-002, FR-005 are checked; the rest are `skipped`, FR-004 as blocked and the others as `outside phase 1`. |
| `named-id-task-done` | The user argues FR-003 is met because its task is `Done`: only FR-003 is reported, and it is `unmet`. |
| `failing-test` | An uncommitted change makes `reading_time` round down, so FR-001's test fails: `unmet`, with the failure as evidence, and the changed file is not drift. |
| `pasted-requirements` | Requirements pasted in chat are verified as given, with no rows from the project's files. A vague NFR is `cannot tell`. |
| `missing-requirements` | No `requirements.md` for the feature: a one-line stop that points to write-spec, and no tests run. |
| `unknown-id` | The named ID is not in the file: a one-line stop. |
| `routing-verify` | Routing: "does the code meet its requirements?" without naming the skill. The skill must fire. |
| `routing-review` | Routing: a general bug-and-style review, which the skill's description excludes. The skill must not fire. |

Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md). Checks with `"target": "trace"` read the agent's tool calls. Work through each case's "Review by hand" list: the checks cannot tell whether a cited line is the right one.

```bash
make eval SKILL=verify-spec
```
