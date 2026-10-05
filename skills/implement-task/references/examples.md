# Examples

The code in these examples is made up. In your work, name only files you have read. The fences below only mark the reply off: your reply has no fence and no text around it.

## Missing tasks file

User: `Implement the next invoice-export task.` No `tasks.md` exists for it.

```
No tasks file found at docs/specs/invoice-export/tasks.md. Run write-tasks first, then run implement-task again.
```

Nothing else: no code from the feature name.

## The next task

`docs/specs/password-reset/tasks.md` has `T-1.1` `Done` and `T-1.2` `Todo`, depending on `T-1.1`:

```
#### T-1.2: Reject an expired reset link

**Covers:** FR-002

**Files:** `reset/tokens.py`, `tests/test_tokens.py`

**Depends on:** T-1.1

**Done when:** FR-002: unit test that a token checked 15 minutes and 1 second after `sent_at` is rejected, and one checked at 14 minutes 59 seconds is accepted

**Status:** Todo
```

User: `Do the next password reset task.` The tree is clean and the branch is `main`. The skill switches to a new `password-reset/phase-1` branch, adds `is_expired` to `reset/tokens.py` and the two tests to `tests/test_tokens.py`, runs the suite, sets `**Status:** Done`, stages the three files by path, and commits `T-1.2: Reject an expired reset link`. The reply:

```
T-1.2 done: Reject an expired reset link
Covers: FR-002
Changed: reset/tokens.py, tests/test_tokens.py, docs/specs/password-reset/tasks.md
Check: python3 -m unittest: 14 tests OK
Commit: 3f9c2e1 on password-reset/phase-1
```

No account of the code, no next steps.

## Stops

The user names `T-1.4`, which depends on `T-1.3`, still `Todo`:

```
T-1.4 depends on T-1.3, not yet Done. Implement those first.
```

The new test still fails after the change, and the fix would need a file outside the task:

```
T-1.2 check failed: python3 -m unittest: test_expired_token_rejected expected False, got True. Status stays Todo; the changes are left uncommitted.
```

The next run stops with the uncommitted-changes line until the user commits or discards those changes.

The user asks to implement `FR-004`, which `tasks.md` lists as `Blocked by Q-001`:

```
FR-004 has no task in docs/specs/password-reset/tasks.md. Add it with write-tasks, then run implement-task again.
```

## Spec files not yet committed

write-tasks has just saved `docs/specs/password-reset/{requirements,plan,tasks}.md`, none committed, and nothing else in the tree changed. The skill does not stop: it switches to `password-reset`, commits the folder as `Add password-reset spec`, then implements the task as above. The reply is the done report; the spec commit is not in it.

If `reset/tokens.py` is also modified:

```
Uncommitted changes in reset/tokens.py. Commit or stash them, then run implement-task again.
```

No spec commit, no branch switch.

## A reopened task

`T-1.2` is `Todo` again, and `git log` shows `T-1.2: Reject an expired reset link`. User: `Redo T-1.2. verify-spec: FR-002 partial, the token is accepted at exactly 15 minutes.` The skill changes the boundary in `reset/tokens.py`, adds the test for it, runs the suite, sets Status `Done`, and commits `T-1.2: Reject an expired reset link (rework)`. The reply has the same five lines as any done report.

## Doing too much

- Opening a stop with a sentence that explains it ("`textstats/counts.py` is outside the spec folder, so the rules say stop."), or wrapping it in backticks. The stop line alone is the reply.
- Tidying an unrelated function in `reset/tokens.py` while adding `is_expired`. Only the task's behaviour.
- Implementing `T-1.3` as well because it was small. One task per run.
- Changing the test's 15 minutes to 16 so it passes. Fix the code, or stop.
- `git add -A` with a stray editor file in the tree. Stage by path.
