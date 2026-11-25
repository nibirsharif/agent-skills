Set: dev. A project on disk: a Python package with `unittest` tests, and a web page in plain JavaScript that has no test runner. The requirements are read from `docs/specs/note-tags/requirements.md`. Five written requirements in three places of the code: they fit one phase.

Written IDs (5): FR-001 to FR-004, NFR-001.

Phase count: 1. The feature changes about 6 files (`notes/store.py`, `notes/cli.py`, `tests/test_store.py`, `tests/test_cli.py`, `web/app.js`, and perhaps `web/index.html`), under the limit of 10, and 5 requirements are under the limit of 8.

Before: none.

Together (same phase):
- T1: NFR-001 with FR-003, the response it limits.
- T2: FR-001 with FR-002: one call, accepted or rejected.

Code:
- C1: the Size is `about <n> files` with n from 4 to 8.
- C2: Reuse names `notes/store.py` and `notes/cli.py` by path, and at least one of the two test files.
- C3: no path is named that is not in the project, unless the plan says the file is new.
- C4: no tool the project lacks is named (pytest, Jest, Playwright, Selenium, a benchmark library).

Blocked: none. Section 3 is `None.`

One sensible cut: one phase with all five IDs.
