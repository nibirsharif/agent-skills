# Task Rules

These rules are authoritative for `write-tasks`. A task list is checked against the [checklist](#validation-checklist) before it is returned.

## Reading the plan

`plan.md` has phases (section 2), blocked requirements (section 3), and open questions (section 4). Each phase lists its `FR` and `NFR` IDs, the code to reuse, the interface and data changes, and how to verify each ID.

- **Tasked:** every phase in section 2, and only those. Phase numbers come from the plan and are never renumbered.
- **Blocked:** a `Blocked by Q-…: <topic>` entry in the plan's section 3. It gets no task. Copy each entry word for word, on one line, into the tasks file's Blocked section, or write `None.` only when the plan's section 3 is `None.`. A plan entry is never dropped. Never replace an entry with the text of its questions, and never split one into one line per question.
- **Interface and data changes:** each item a phase lists there is built by a task of that phase, whether or not a Verify line names it. That task names the item in its title or Files, covers the phase's IDs whose behaviour needs it, and its Done when tests the item itself for those IDs. A later task that uses the item depends on that task and uses the item instead of building the same rule again. The one exception is an item the code already has, found while exploring: it gets no task, and the Overview names it and the file that has it. An item that no ID of its phase needs is a question, as for a vague phase.
- **Open questions:** never tasked, never answered, never listed in the tasks file except inside a `Blocked by` entry.
- **Requirements file:** when `requirements.md` is beside the plan, check that every ID in a phase is a written requirement there. With a pasted plan and no file, trust the plan.

## Stop and ask

- The plan file is missing or has no phase: reply with the stop line and stop. Do not task from the feature name or from requirements.
- A phase lists a withdrawn ID or an ID that `requirements.md` does not have: stop with the line that names the ID. Do not pick which side is right.
- A phase would need more tasks than the limit: stop with the line that names the phase. Count before writing: list one task per distinct behaviour or interface and data change in the phase, plus the verify task, and compare the count with `tasks_max_per_phase` (or the limit the user stated). Never merge behaviours, drop the verify task, or combine unrelated work to fit, and never split the phase yourself; phase sizes belong to `write-plan`.
- A phase is too vague to task (its scope or interface changes leave a choice the code and the requirements do not decide): ask the question in chat and write nothing.

## Exploring the code

Explore before writing a task. Look for the files and modules the phase's scope and interface changes name, the tests beside them and how they are run, and the patterns similar features follow. Name a file only after you have seen it. A file that does not exist yet is written `new: <what it is>`, never a guessed path. With no codebase, every file is `new:`, and the Overview says so.

## A task

A task is one focused change that can be finished and committed on its own, with the tests green.

Every task has six parts, in this order:

- **Title:** `#### T-<phase>.<n>: <imperative title>`, numbered from 1 in each phase, in build order.
- **Covers:** the `FR` and `NFR` IDs the task builds or proves. At least one, and only IDs from its own phase.
- **Files:** each file the task adds or changes, as `` `path` `` for an existing file or `new: <what it is>`, tests included. At most `tasks_max_files_per_task` (default 3).
- **Depends on:** the IDs of earlier tasks it needs, or `None.`. A task depends only on tasks that come before it in the file.
- **Done when:** one line: for each ID in Covers, `<ID>: <a test to add or command to run>`, or `<ID>: manual: <what a person does and sees>` where [Manual checks](#manual-checks) allows it. A check a reviewer can run or see, not "works" or "reviewed".
- **Status:** `Todo` in a new task. Only `implement-task` sets it to `Done`.

A task holds no code and no steps inside it: the title and its check are the task.

## Manual checks

A check is a test or a command whenever a test runner the project already has can drive the requirement's trigger and check its response. Only when none can is the check one a person makes: something seen on a screen, a device, or paper, a message arriving in a real inbox, a judgement. That check starts with the word `manual:`.

- **The word is fixed:** `<ID>: manual: <check>`, lowercase, directly after the ID. Other skills read the word, not the wording of the check, so a check for a person without it is treated as a test that is missing.
- **The check says what to do and what to see,** exactly enough for a person who did not write the code: `FR-007: manual: in the browser, open a link older than 24 hours: the page shows "Expired"`.
- **Per ID, not per task.** A task may prove one ID with a test and another with a manual check, separated by `;`.
- **Never to save work.** A test that is hard or slow to write is still a test. A behaviour that part of a test can reach gets that test.
- **Never add a runner to avoid one.** Which tools the project uses belongs to the plan: a task names no test tool that neither the plan nor the code has.
- **The task still builds the behaviour:** its Files list the code it changes.
- **The verify task** repeats each `manual:` check of its phase, word for word, beside the automated ones.

## Size and order

1. **Small.** One behaviour, or one interface or data change, per task. A task that needs "and" to describe two separate behaviours is two tasks. A phase holds at most `tasks_max_per_phase` tasks (default 12).
2. **Order by dependency.** Data and interfaces first, then behaviour, then failure handling, as the plan's phase does. Within a phase, each task depends only on earlier tasks; across phases, only on tasks of earlier phases.
3. **Check with the change.** The check that proves a requirement is written in the task that builds the behaviour, or in an earlier task. Never leave all tests for a final task.
4. **Every task leaves the product working** and the tests green. No task ends with a half-wired feature that a later task completes.
5. **End each phase with a verify task:** it covers every ID of the phase and its Done when runs the phase's Verify list from the plan. It is not counted as the task that builds an ID.

## Validation checklist

Run every item on the task list before returning it.

1. Every `FR` and `NFR` of a phase is in the Covers of at least one task of that phase other than its verify task, and no task covers an ID from another phase.
2. No blocked requirement, withdrawn ID, or open question has a task; each plan `Blocked by` entry is copied once.
3. No task depends on a later task, and no task of one phase depends on a later phase.
4. No task has more files than the limit, and no phase has more tasks than the limit.
5. Every task has title, Covers, Files, Depends on, Done when, and Status; Done when is one line and cites each ID in Covers; every new task is `Todo`.
6. Each requirement's check sits in the task that builds it or an earlier one.
7. Each phase ends with its verify task.
8. Every path in Files was seen in the code; every other file is `new:`; with no codebase, every file is `new:`.
9. No code, no new requirement, no change to the plan's phases, and no open question answered.
10. Every check a person must make starts with `manual:` after its ID, no other check does, and none is manual where a test runner in the project can make it.
11. Every item under a phase's Interface and data changes is named in the title or Files of a task of that phase, or the Overview names the file that already has it.
