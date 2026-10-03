# verify-spec

Instructions the agent follows: [skills/verify-spec/SKILL.md](../skills/verify-spec/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Checks the code against a saved `requirements.md` and gives one verdict per requirement, each with the evidence behind it: the line where the behaviour is, and the test that proves it, run now. It runs the project's own test command once, changes nothing, and commits nothing.

It reads only `requirements.md` (and `plan.md` when it is there, to limit the check to one phase and to spot blocked requirements). It never reads `tasks.md`: a task marked `Done` says what someone intended, not what the code does.

## When to use it

- You finished a phase or a feature and want to know whether the requirements are really met, not just whether the tasks are `Done`.
- You inherited code that has a spec, or built it without the plan and task steps.
- Before review: to find the requirement nobody implemented, or implemented without a test.

It does not write requirements, plans, tasks, or code, and it is not a general code review. Without a requirements file, use `/code-review`.

## Output

One table, then three lines. Rows follow the order of the requirements file.

```
| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | met | textstats/counts.py:17; tests/test_counts.py::test_rounds_up_at_default_speed passed |
| FR-002 | untested | textstats/counts.py:15; no test passes a non-string to reading_time |
| FR-003 | unmet | no implementation found: reading_time takes no words-per-minute argument |
| FR-004 | skipped | Blocked by Q-001 |
| NFR-001 | cannot tell | no criterion; clarify with write-spec |
Tests: python3 -m unittest: 4 tests OK
Tally: 1 met, 1 unmet, 1 untested, 1 cannot tell, 1 skipped
Drift: textstats/formatting.py
```

| Verdict | Means |
|---------|-------|
| `met` | The code does what the statement says, and a test for it ran and passed |
| `partial` | Part of the statement is missing or wrong |
| `unmet` | No implementation found, or the test for it ran and failed |
| `untested` | The code does it, but no test exercises it, or the tests did not run |
| `cannot tell` | The requirement has no checkable criterion, such as "quickly" with no limit |
| `skipped` | Blocked by an open question, or outside the phase you asked for |

`Drift` lists changed files that no requirement covers: uncommitted files, plus the files changed on the feature branch. It lists them and leaves the judgement to you; a refactor is not necessarily a defect.

It stops with a single line instead when there is no `requirements.md` for the feature, the file has no `FR` or `NFR` requirements, or the ID or phase you named does not exist. The full list is in [the rules](../skills/verify-spec/references/verify-rules.md#stop-lines).

## FAQ

**Can I check just one phase, or one requirement?** Yes. Ask for "phase 2" (it needs `plan.md`) or name an ID such as `FR-003`. Requirements outside the phase appear as `skipped`.

**Can I paste requirements instead of using a file?** Yes. It verifies exactly what you pasted and compares nothing with a file.

**Why is a requirement `untested` when the code is right?** `met` needs both the code and a passing test. When two verdicts fit, it takes the weaker one, so a requirement is never rounded up.

**Why does it run my tests?** A test that exists is not evidence; one that passed in this run is. It runs the project's existing test command once and nothing else: no installs, no scripts that change data. When the tests cannot run, the `Tests:` line says why and no row is `met`.

**Does it tell me how to fix a gap?** No. A row says what is missing. Fix code with [implement-task](implement-task.md) and requirements with [write-spec](write-spec.md).

**Why did the reply start with a sentence?** The instructions say the reply is the table and nothing else, but in eval runs about one reply in ten opened with a short sentence anyway. The table that follows is still right.

## Verifying results

- Open one `met` row's cited line: it should be where the behaviour is, and the named test should assert the behaviour, not just call the code.
- A `Done` task in `tasks.md` has no effect on any verdict.
- `git status` after the run is what it was before: nothing edited, staged, or committed.

## Related skills

Checks the output of the chain [write-spec](write-spec.md) → [write-plan](write-plan.md) → [write-tasks](write-tasks.md) → [implement-task](implement-task.md). It reads `requirements.md` and, optionally, `plan.md` from `spec_output_dir`.
