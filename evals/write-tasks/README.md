# write-tasks evals

Made-up plan files that exercise the write-tasks skill's rules, each with automatic checks and a short list to review by hand. Every run starts in an empty folder, so the plan is pasted into the prompt and there is no codebase: a good reply marks every file `new:` instead of naming paths.

| Case | Tests |
|------|-------|
| `missing-plan` | The plan file does not exist: one short reply that points to write-plan, and no tasks. |
| `single-phase` | One phase, three requirements: five-part tasks in dependency order, every ID covered by a building task, a check that cites each ID, a verify task last. |
| `multi-phase` | Two phases: task IDs numbered per phase, each phase ends with its verify task, and no task depends on a later one. |
| `blocked` | The plan has a blocked requirement and open questions: nothing is tasked for it, no question is answered, the `Blocked by` entry is copied once. |
| `plan-mismatch` | The plan lists an ID that requirements.md withdraws: a one-line stop, no tasks. |
| `oversized-phase` | A phase needs more tasks than the stated limit: a one-line stop that sends the user to write-plan. |
| `routing-tasks` | Routing: a request to break a plan's phase into tasks, without naming the skill. The skill must fire. |
| `routing-plan` | Routing: a request to write the plan from requirements, which the skill's description excludes. The skill must not fire. |

Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

```bash
make eval SKILL=write-tasks
```
