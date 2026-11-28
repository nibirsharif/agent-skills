# Task Rules

## Reading the plan

- **Tasked:** every phase in the plan's section 2, and only those. Phase numbers come from the plan and are never renumbered.
- **Blocked:** a `Blocked by Q-…: <topic>` entry in the plan's section 3 gets no task. Copy each entry word for word, on one line, into the tasks file's Blocked section, or write `None.` only when the plan's section 3 is `None.`. Never drop an entry, replace it with the text of its questions, or split it into one line per question.
- **Interface and data changes:** each item a phase lists there is built by a task of that phase, whether or not a Verify line names it. That task names the item in its title or Files, covers the phase's IDs whose behaviour needs it, and its Done when tests the item itself for those IDs. A later task that uses the item depends on that task and uses the item instead of building the same rule again. An item the code already has, found while exploring, gets no task: the Overview names it and the file that has it. An item that no ID of its phase needs is a question, as for a vague phase.
- **Open questions:** never tasked, never answered, never listed in the tasks file except inside a `Blocked by` entry.

## Stop and ask

Each stop is its line from the reply contract and nothing else.

- **No plan file, or no phase in it.** Do not task from the feature name or from requirements.
- **A phase lists a withdrawn ID, or one the `requirements.md` beside the plan does not have.** The line names the ID. Do not pick which side is right. With a pasted plan and no requirements file, trust the plan.
- **A phase needs more tasks than the limit.** Count before writing: list one task per distinct behaviour or interface and data change in the phase, plus the verify task, and compare the count with `tasks_max_per_phase` (or the limit the user stated). Never merge behaviours, drop the verify task, or combine unrelated work to fit, and never split the phase yourself; phase sizes belong to `write-plan`.
- **A phase is too vague to task** (its scope or interface changes leave a choice the code and the requirements do not decide). Ask the question in chat and write nothing.

## Exploring the code

Explore before writing a task. Look for the files and modules the phase's scope and interface changes name, the tests beside them and how they are run, and the patterns similar features follow. Name a file only after you have seen it. A file that does not exist yet is written `new: <what it is>`, never a guessed path. With no codebase, every file is `new:`, and the Overview says so.

## A task

Every task has six parts, in this order:

- **Title:** `#### T-<phase>.<n>: <imperative title>`, numbered from 1 in each phase, in build order.
- **Covers:** the `FR` and `NFR` IDs the task builds or proves. At least one, and only IDs from its own phase.
- **Files:** each file the task adds or changes, as `` `path` `` for an existing file or `new: <what it is>`, tests included. At most `tasks_max_files_per_task`.
- **Depends on:** the IDs of earlier tasks it needs, or `None.`. Within a phase, only earlier tasks; across phases, only tasks of earlier phases.
- **Done when:** one line: for each ID in Covers, `<ID>: <a test to add or command to run>`, or `<ID>: manual: <what a person does and sees>` where [Manual checks](#manual-checks) allows it. A check a reviewer can run or see, not "works" or "reviewed".
- **Status:** `Todo` in a new task. Only `implement-task` sets it to `Done`.

A task holds no code and no steps inside it: the title and its check are the task.

## Manual checks

A check is a test or a command whenever a test runner the project already has can drive the requirement's trigger and check its response. Only when none can is the check one a person makes: something seen on a screen, a device, or paper, a message arriving in a real inbox, a judgement. That check starts with the word `manual:`.

- **The word is fixed:** `<ID>: manual: <check>`, lowercase, directly after the ID. Other skills read the word, so a check for a person without it is treated as a missing test.
- **The check says what to do and what to see,** exactly enough for a person who did not write the code: `FR-007: manual: in the browser, open a link older than 24 hours: the page shows "Expired"`.
- **Per ID, not per task.** A task may prove one ID with a test and another with a manual check, separated by `;`.
- **Never to save work.** A test that is hard or slow to write is still a test. A behaviour that part of a test can reach gets that test.
- **Never add a runner to avoid one.** Which tools the project uses belongs to the plan: a task names no test tool that neither the plan nor the code has.
- **The task still builds the behaviour:** its Files list the code it changes.
- **The verify task** repeats each `manual:` check of its phase, word for word, beside the automated ones.

## Size and order

1. **One behaviour per task,** or one interface or data change. A behaviour is one event and everything the phase's requirements say about it: the requirement the event triggers, each `If ... then` requirement for that event going wrong, and an `NFR` that sets a threshold on its response. One task builds them together: it covers all their IDs and has a check for each, an exception's check in the test file of the requirement it is an exception to. Only when the task's files would still pass the limit does the `NFR` or the exception become the next task. Two events are two tasks, even in one file: a task that needs "and" to join two events is two tasks.
2. **Order by dependency.** Data and interfaces first, then behaviour, then failure handling, as the plan's phase does.
3. **Check with the change.** The check that proves a requirement is written in the task that builds the behaviour, or in an earlier task. Never leave all tests for a final task.
4. **Every task can be finished and committed on its own,** leaving the product working and the tests green. No task ends with a half-wired feature that a later task completes.
5. **End each phase with a verify task:** it covers every ID of the phase and its Done when runs the phase's Verify list from the plan. It is not counted as the task that builds an ID.

## Validation checklist

Run every item on the task list before returning it.

1. Every `FR` and `NFR` of a phase is in the Covers of at least one task of that phase other than its verify task, and no task covers an ID from another phase.
2. No blocked requirement, withdrawn ID, or open question has a task; each plan `Blocked by` entry is copied once.
3. No task depends on a later task or on a later phase.
4. No task has more files than the limit, and no phase has more tasks than the limit.
5. Every task has all six parts; Done when is one line and cites each ID in Covers; every new task is `Todo`.
6. Each requirement's check sits in the task that builds it or an earlier one, and each phase ends with its verify task.
7. Every path in Files was seen in the code; every other file is `new:`.
8. Every check a person must make starts with `manual:` after its ID, no other check does, and none is manual where a test runner in the project can make it.
9. Every item under a phase's Interface and data changes is named in the title or Files of a task of that phase, or the Overview names the file that already has it.
