# Updating an existing tasks.md

Read this only when a `tasks.md` already exists beside the plan. The file keeps the [template](tasks-template.md)'s layout.

- A phase has started when any of its tasks is `Done`. Ask which phases have started only when the file has no Status lines; never assume. Tasks of started phases stay as they are, with their IDs and Status.
- A phase whose requirements changed and has not started is re-split from the plan; its task IDs may change and every task is `Todo`. Say so in the Revision History.
- A phase already started that gains a requirement gets new tasks after the existing ones, with the next numbers, Status `Todo`, and a new last verify task. Earlier tasks keep their IDs.
- A new phase in the plan is appended. A requirement that left the plan is removed from its tasks; a task left with no ID is removed.
- Update **Plan** with the new `plan.md` version.
- Each update raises the minor version and adds one Revision History row naming the phases and task IDs added, changed, or removed.
