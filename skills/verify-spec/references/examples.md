# Examples

The code in these examples is made up. In your work, cite only files and lines you have opened. The fences below only mark the reply off: your reply has no fence and no text around it.

## Missing requirements file

User: `Does the invoice-export feature meet its spec?` No `requirements.md` exists for it.

```
No requirements file found at docs/specs/invoice-export/requirements.md. Run write-spec first, then run verify-spec again.
```

Nothing else: no review of the code from the feature name.

## Unknown ID

User: `Is FR-009 met?` `requirements.md` has FR-001 to FR-005.

```
No requirement FR-009 in docs/specs/reading-time/requirements.md.
```

Nothing else: no verdicts for the requirements that do exist, no remarks on the code.

## A mixed report

`docs/specs/password-reset/requirements.md` has FR-001 to FR-004 and NFR-001, and FR-004 is `Blocked by Q-001`. The code on the `password-reset` branch sends the link and rejects an expired one, but nothing checks the token was already used, and the rate limit is written with no test. The tests ran: 14 passed. `reset/audit.py` was added and no requirement mentions it.

```
| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | met | reset/mail.py:21; tests/test_mail.py::test_sends_link passed |
| FR-002 | met | reset/tokens.py:34; tests/test_tokens.py::test_expired_token_rejected passed |
| FR-003 | unmet | no implementation found: searched reset/ for used-token handling |
| FR-004 | skipped | Blocked by Q-001 |
| NFR-001 | untested | reset/limits.py:12 allows 5 requests per hour; no test exercises it |
Tests: python3 -m unittest: 14 tests OK
Tally: 2 met, 1 unmet, 1 untested, 1 skipped
Drift: reset/audit.py
```

The rows say what is missing and stop there: no "add a check in `tokens.py`".

## Weaker verdict, and a vague requirement

FR-005 says the system shall return the whole minutes needed to read the text, rounded up, at 200 words per minute. `reading_time` at `textstats/counts.py:40` divides by 200 and rounds down, and its one test uses 400 words, which both roundings give the same answer for. NFR-002 says the library shall be fast.

```
| ID | Verdict | Evidence |
|----|---------|----------|
| FR-005 | partial | textstats/counts.py:40 rounds down, not up; tests/test_counts.py::test_reading_time passed but uses 400 words, where both agree |
| NFR-002 | cannot tell | no criterion; clarify with write-spec |
Tests: python3 -m unittest: 6 tests OK
Tally: 1 partial, 1 cannot tell
Drift: none
```

A passing test does not make FR-005 `met`: its body never drives the rounding.

## One phase

`plan.md` Phase 1 lists FR-001 and FR-002; FR-003 is in Phase 2. User: `Verify phase 1.`

```
| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | met | textstats/counts.py:40; tests/test_counts.py::test_200_words_one_minute passed |
| FR-002 | met | textstats/counts.py:36; tests/test_counts.py::test_non_string_raises passed |
| FR-003 | skipped | outside phase 1 |
Tests: python3 -m unittest: 9 tests OK
Tally: 2 met, 1 skipped
Drift: not checked (no feature branch)
```

## Tests that cannot run

No test command can be found, so nothing was run. FR-001 has code at `textstats/counts.py:40` and a test file that looks right.

```
| ID | Verdict | Evidence |
|----|---------|----------|
| FR-001 | untested | textstats/counts.py:40; tests/test_counts.py::test_200_words_one_minute exists but was not run |
Tests: not run: no test command found in README, Makefile, or CI config
Tally: 1 untested
Drift: none
```

## Doing too much

- Explaining the scope or the branch before the table ("On the default branch, so no drift check applies."). That belongs in the Drift line.
- Following a stop line with what the code turned out to hold. The stop line is the whole reply.
- Opening with a sentence ("Most requirements are met, but two have gaps."), or closing with advice ("Next, implement FR-003."). The report alone is the reply.
- Marking FR-002 `met` because `tasks.md` says T-1.2 is `Done`. Status is never evidence.
- Marking a row `met` from the test's name without reading its body.
- Rounding up: a test that passes only for easy inputs is `partial` or `untested`, never `met`.
- Fixing the missing check while verifying, or adding the missing test. This skill changes nothing.
- Checking FR-004 and calling it `unmet` when it is `Blocked by Q-001`. It is `skipped`, and its evidence is the question, even when a phase was named.
- Listing a refactor as a defect. Drift lists the file and leaves the judgement to the user.
