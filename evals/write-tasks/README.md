# write-tasks evals

Made-up plan files that exercise the write-tasks skill's rules, each with automatic checks and a short list to review by hand. Every run but `ask-location`'s starts in an empty folder, so the plan is pasted into the prompt and there is no codebase: a good reply marks every file `new:` instead of naming paths.

| Case | Tests |
|------|-------|
| `missing-plan` | The plan file does not exist: one short reply that points to write-plan, and no tasks. |
| `single-phase` | One phase, three requirements: six-part tasks in dependency order, every ID covered by a building task, a check that cites each ID, a verify task last. |
| `multi-phase` | Two phases: task IDs numbered per phase, each phase ends with its verify task, and no task depends on a later one. |
| `blocked` | The plan has a blocked requirement and open questions: nothing is tasked for it, no question is answered, the `Blocked by` entry is copied once. |
| `plan-mismatch` | The plan lists an ID that requirements.md withdraws: a one-line stop, no tasks. |
| `oversized-phase` | A phase needs more tasks than the stated limit: a one-line stop that sends the user to write-plan. |
| `interface-item` | The phase's Interface and data changes list a helper that no Verify line names: a task builds it, before the commands that use it. |
| `event-tasks` | Two events, each with an `If ... then` exception, and one with an `NFR`: each event is one task that covers its requirements together with a check for each ID, no exception is a task of its own, and the two events are two tasks. |
| `pasted-not-saved` | `single-phase`'s input sent without the chat-only line: the tasks are in chat, and their last line says they were not saved. |
| `ask-location` | No `spec_output_dir`, no path in the request, and a `plan.md` in a folder of the project: the reply is the location question alone, with no search of the project and nothing saved. The project is in the case's `dirty/` folder, and the input is sent as written, without the chat-only line. |
| `routing-plan` | Routing: a request to write the plan from requirements, which the skill's description excludes. The skill must not fire. |

Shorter rules, the next piece of [#24](https://github.com/nibirsharif/agent-skills/issues/24), 19 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). What a run reads went from 3,928 to 3,225 words: `SKILL.md` 1,062 to 925, `task-rules.md` 1,449 to 1,274, `examples.md` 904 to 745, `tasks-template.md` 513 to 281. The template is counted because the runs read it for a chat reply too (22 of 24 before and after), so the word budget now lists it. `SKILL.md`'s Output section is merged into the reply contract; each stop is stated once, with its line in the contract and what not to do in the rules; the checklist is 9 items where it was 11; the examples that repeated a rule or a line of the contract are gone (the missing-plan and oversized-phase stops, three of five wrong splits); and the rules for changing a `tasks.md` that exists moved from the template to `updating.md` (185 words), read only then.

The whole suite at 3 runs with the judge:

| Wording | Passed | Passed, the checks without the judge |
|---|---|---|
| Before the change | 22 of 27 | 26 of 27 |
| First cut: `SKILL.md`, the rules, the examples | 23 of 27 | 27 of 27 |
| Second cut: the template too, with `updating.md` | 24 of 27 | 27 of 27 |
| Final: the second cut with two examples restored | 23 of 27 | 27 of 27 |

The one miss of a check was before the change: a `single-phase` reply with a `## 4. Revision History` table in chat. Every other miss is the judge's, on three expectations. A reply like the golden one fails the first two:

- `single-phase`, "No requirement is added, reworded, or split, and no task is a layer such as Database or UI": 3 of 3 before, then 3, 2, and 3 of 3. The judge reads a requirement covered by two tasks as split, the token store task as a Database layer, and a check the plan's Verify list does not have as added. The golden reply and the skill's own example do all three, as the rules ask.
- `oversized-phase`, "does not merge unrelated work into fewer tasks and does not split the phase itself": 0 of 3 before, then 1 of 3 each time, on a reply that is the golden line word for word. The judge reads "Split it in plan.md with write-plan" as splitting the phase.
- `interface-item`, "No task other than the helper's builds the file path": 2 of 3 before, 0 of 9 after. In both, the judge's own evidence finds no such task ("Under a strict reading, no other task builds the path, so this should pass") and marks the expectation failed all the same.

The two examples restored are about `manual:`; the benchmark showed the need, not the suite: see [benchmark/after-shorter-rules.md](benchmark/after-shorter-rules.md), which also has the benchmark before and after (no column moved by more than the spread between runs). In the final suite run every run that loaded the skill read `task-rules.md` (24 of 24; the other three runs are `routing-plan`), 23 read `examples.md`, and none read `updating.md`: no case has a `tasks.md` to update, before or after, so that path is untested. Also cut with no case that would show a difference: saving to a file (every case replies in chat), and a phase too vague to task.

Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

Judge wording, 23 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). Two expectations failed correct replies on 19 November: `single-phase`'s second in 11 of 12 runs, and `oversized-phase`'s in 3 of 12. Both now say what counts as meeting them. Reworded, they passed in 6 of 6 new runs, on the nine `single-phase` replies saved from 19 November, and on the golden replies (3 and 8 judgings), and failed five hand-made violations in 10 of 10 judgings: layer-name titles, an added `FR-003`, a rewritten requirement sentence, three merged tasks, and Phase 1 divided into two phases. The run was 5 of 6: one `single-phase` run failed its first expectation, which is unchanged. There the judge answered "failed" with evidence that ends "Marking pass is warranted", as it did for one of the nine saved replies: it wrote the verdict before the evidence. [grading.py](../grading.py) now asks for the evidence first, in the judge's schema and in its prompt (the schema alone moved it in 8 of 36 judgings). On 12 saved `single-phase` replies the first expectation then failed 0 of 72 judgings, against 3 of 72 before, two of the three with evidence that concludes it is met. The violations still failed 10 of 10, and the two cases passed 6 of 6.

The location question without a search, 23 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). With no `spec_output_dir` and no path in the request, the skill asks where `plan.md` is and never searches the project for it. The new `ask-location` case has a `plan.md` and its `requirements.md` under `notes/room-booking/`, and its checks on the tool calls fail a read of `notes/`, a `find`, a recursive `ls`, an `ls` or Glob with a wildcard, and a Write or Edit. Before the change it passed 0 of 12. Every run listed or searched the project in its first command, after reading `SKILL.md` and the rules: `ls` with `find . -name plan.md` in one Bash call (7 runs), or else a `find` over every file, `ls -laR`, or a Glob with `**`. Ten runs then asked the question all the same, nine as their whole reply and one after a sentence (`Per the skill, I can't use a path I found by searching the project.`). Two read the plan and the requirements they found and saved a six-task `tasks.md` beside them.

Workflow step 1 now says that a path comes only from the request, the conversation, or the two config files, names what not to run until one of them gives it (`ls`, `find`, Glob), and says the question is asked even with a `plan.md` in plain sight: the reply's first word is `Where`. write-plan has the same fault, and its step 1 gets the same two sentences. That is 60 words: `SKILL.md` goes from 925 to 985 and a run reads 3,285, inside the budget of 3,330. The lookup rule shared with four other skills is unchanged.

| Step 1 | Passed | Listed or searched | Read the plan | Saved a `tasks.md` | A sentence before the question |
|---|---|---|---|---|---|
| Before the change | 0 of 12 | 12 | 2 | 2 | 1 |
| After | 12 of 12, and 3 of 3 in the suite | 0 | 0 | 0 | 0 |

Each of the 15 runs after the change reads the two config files, by Read or `cat`, and replies with the question alone. The whole suite at 3 runs with the judge passed 30 of 30, with 33 judge verdicts and none failed; the nine cases that were there before passed 27 of 27. Every one of them that pastes a plan also names its path, so a probe that is not committed sent `single-phase`'s plan with no path anywhere: 6 of 6 runs wrote the tasks in chat and none asked for a location.

More tasks a phase, 24 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327). The default `tasks_max_per_phase` is 16, from 12. write-plan now fills a phase up to its limit of 8 requirements ([#10](https://github.com/nibirsharif/agent-skills/issues/10)), and such a phase needs about one task per requirement and per interface item, plus the verify task. A table-booking plan whose Phase 1 has 8 requirements was pasted in three times at each limit: at 12, one run stopped with `Phase 1 needs more than 12 tasks.` and the others wrote 12 and 11 tasks; at 16, the three runs wrote 10, 9, and 9. The rule for a task's size is unchanged, and so are the benchmark and its references. The `multi-phase` check for a phase over the limit follows the new number. The whole suite at one run each passed 10 of 10; `oversized-phase` states its own limit of 3.

One event per task, 27 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327), for [#44](https://github.com/nibirsharif/agent-skills/issues/44). A task builds one behaviour, and a behaviour is now one event with everything the phase's requirements say about it: the requirement the event triggers, each `If ... then` requirement for that event going wrong, and an `NFR` that sets a threshold on its response. One task covers their IDs, with a check for each. Before, each requirement was a task of its own, and the real run's 29 requirements became 24 build tasks, 17 of them in the same two files. On the benchmark three runs have 105 build tasks against 141, 1.03 for each requirement against 1.38, with coverage, order, and the checks unchanged: [benchmark/after-event-tasks.md](benchmark/after-event-tasks.md), which also has the real run's plan tasked again (19, 19, and 22 build tasks against 25, 29, and 25).

The new `event-tasks` case has an upload with a size exception and a deadline, and a delete with an ownership exception:

| Wording | Passed |
|---|---|
| Before the change | 0 of 6 |
| First wording: the exception or the `NFR` is the next task only when the task's files would pass the limit | 4 of 6 |
| Final: the same, and an exception's check goes in the test file of the requirement it is an exception to | 8 of 8, and 3 of 3 in the suite |

Before the change every reply wrote five or six tasks, one for each requirement. On the first wording two replies gave each exception a test file of its own, counted the task's files over the limit of 3, and wrote the exception as the next task.

The golden replies of `single-phase`, `multi-phase`, `blocked`, `pasted-not-saved`, and `interface-item` follow the rule: the email with its deadline is one task, and so are the export with its refusal and the new password with its length check. In the suite's runs every reply to the password-reset cases joined the email and its deadline (12 of 12).

The whole suite at 3 runs with the judge passed 30 of 30 on the first wording, before `event-tasks` was added, and 31 of 33 on the final one, with 33 judge verdicts and one failed. The two misses:

- `multi-phase`, once: the check for a task over 3 files counted commas, and a joined task's file description held two (`handler that checks the token, checks the password length, updates the password ...`). The task has three files. The check now counts `new:` entries in the four cases with no codebase, and the same reply passes.
- `oversized-phase`, once: the reply joined the token store with the expiry check and wrote three tasks to fit the limit of 3, which the rules forbid. The phase now needs four tasks, one over the limit, where it needed five. Run alone, the case then passed 10 of 10, and the wording before the change passed 10 of 10 at a limit of 4, the same one task over. So it is 1 miss in 13 runs, and the case is unchanged.

A run reads 3,412 words, from 3,285, and the budget is 3,500, from 3,330: the size rule is 96 words longer, and the examples 31: a task that is too small is new there, and the separate deadline task is gone. Not measured: a build from a joined task, by implement-task or build-phase.

```bash
make eval SKILL=write-tasks
```

[benchmark/](benchmark/README.md) measures task size, order, and whether the checks can be run, which these cases do not.
