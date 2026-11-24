# write-tasks evals

Made-up plan files that exercise the write-tasks skill's rules, each with automatic checks and a short list to review by hand. Every run starts in an empty folder, so the plan is pasted into the prompt and there is no codebase: a good reply marks every file `new:` instead of naming paths.

| Case | Tests |
|------|-------|
| `missing-plan` | The plan file does not exist: one short reply that points to write-plan, and no tasks. |
| `single-phase` | One phase, three requirements: six-part tasks in dependency order, every ID covered by a building task, a check that cites each ID, a verify task last. |
| `multi-phase` | Two phases: task IDs numbered per phase, each phase ends with its verify task, and no task depends on a later one. |
| `blocked` | The plan has a blocked requirement and open questions: nothing is tasked for it, no question is answered, the `Blocked by` entry is copied once. |
| `plan-mismatch` | The plan lists an ID that requirements.md withdraws: a one-line stop, no tasks. |
| `oversized-phase` | A phase needs more tasks than the stated limit: a one-line stop that sends the user to write-plan. |
| `interface-item` | The phase's Interface and data changes list a helper that no Verify line names: a task builds it, before the commands that use it. |
| `pasted-not-saved` | `single-phase`'s input sent without the chat-only line: the tasks are in chat, and their last line says they were not saved. |
| `routing-plan` | Routing: a request to write the plan from requirements, which the skill's description excludes. The skill must not fire. |

Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

Judge wording, 23 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). Two expectations failed correct replies on 19 November: `single-phase`'s second in 11 of 12 runs, and `oversized-phase`'s in 3 of 12. Both now say what counts as meeting them. Reworded, they passed in 6 of 6 new runs, on the nine `single-phase` replies saved from 19 November, and on the golden replies (3 and 8 judgings), and failed five hand-made violations in 10 of 10 judgings: layer-name titles, an added `FR-003`, a rewritten requirement sentence, three merged tasks, and Phase 1 divided into two phases. The run was 5 of 6: one `single-phase` run failed its first expectation, which is unchanged. There the judge answered "failed" with evidence that ends "Marking pass is warranted", as it did for one of the nine saved replies: it wrote the verdict before the evidence. [grading.py](../grading.py) now asks for the evidence first, in the judge's schema and in its prompt (the schema alone moved it in 8 of 36 judgings). On 12 saved `single-phase` replies the first expectation then failed 0 of 72 judgings, against 3 of 72 before, two of the three with evidence that concludes it is met. The violations still failed 10 of 10, and the two cases passed 6 of 6.

```bash
make eval SKILL=write-tasks
```

[benchmark/](benchmark/README.md) measures task size, order, and whether the checks can be run, which these cases do not.
