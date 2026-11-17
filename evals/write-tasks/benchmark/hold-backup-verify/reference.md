Set: hold. A project on disk: a Python package with `unittest` tests run by `make test`, a mailer that takes the SMTP connection as an argument, and a module that drives a status light on a device. Two phases, six IDs.

IDs (6): Phase 1: FR-001, FR-002, FR-003, NFR-001. Phase 2: FR-004, FR-005.

Order (the first task is earlier in the phase than the second):
- O1: Phase 1: the task that writes the checksum file comes before the task that adds `backup verify`.
- O2: Phase 1: the `OK` result (FR-002) comes before, or is in the same task as, the `CORRUPT` result with exit status 1 (FR-003).
- O3: Phase 2: a task that reports a failed verification depends on the Phase 1 task that verifies, and on no task after it.

Manual:
- M1: FR-004 is not `manual:`. `mailer.send` takes the SMTP connection, so a `unittest` test can pass a stand-in and check the one email. A real inbox as the only check saves work a test can do.
- M2: NFR-001 is not `manual:`. A test over a 1 GB archive is slow, and it is still a test.
- M3: FR-001, FR-002, and FR-003 are not `manual:`.
- FR-005 is not scored: a test of what `panel.set_light` is asked to do, a `manual:` look at the light, or both, are all defensible.

Files:
- F1: these existing files are named as paths where a task changes them: `backup/archive.py`, `backup/cli.py`, `backup/schedule.py`, `tests/test_archive.py`. `backup/mailer.py` and `backup/panel.py` are used, and changed only if a task says why.
- F2: no path is named that is not in the project. A test file that does not exist is `new:`.
- F3: no test tool the project lacks is named (pytest, a mail catcher, a benchmark library).

Blocked: none. The section is `None.`
