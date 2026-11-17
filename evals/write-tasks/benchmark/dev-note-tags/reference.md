Set: dev. A project on disk: a Python package with `unittest` tests, and a web page in plain JavaScript that has no test runner. One phase, five IDs.

IDs (5): FR-001, FR-002, FR-003, FR-004, NFR-001.

Order (the first task is earlier in the phase than the second):
- O1: the task that adds `Store.add_tag` and the `tags` list comes before the task that rejects a long tag.
- O2: it comes before the task that filters `list --tag`.
- O3: it comes before the task that draws the labels on the page.
- O4: the filter (FR-003) comes before, or is in the same task as, its speed check (NFR-001).

Manual:
- M1: FR-004 is `manual:`. Nothing in the project can run `web/app.js`: the README says the page has no tests, and the only runner is `python3 -m unittest`.
- M2: FR-001, FR-002, FR-003, and NFR-001 are not `manual:`. `unittest` can drive each, the timing included.
- M3: the verify task repeats the FR-004 `manual:` check word for word.

Files:
- F1: these existing files are named as paths where a task changes them: `notes/store.py`, `notes/cli.py`, `tests/test_store.py`, `tests/test_cli.py`, `web/app.js`, `web/index.html`.
- F2: no path is named that is not in the project. A test file that does not exist is `new:`.
- F3: no test tool the project lacks is named (pytest, Jest, Playwright, Selenium, a benchmark library).

Blocked: none. The section is `None.`
