# write-spec evals

Made-up inputs that exercise the write-spec skill's rules, each with automatic checks and a short list to review by hand. No real product document is used here.

| Case | Tests |
|------|-------|
| `prd-solar-monitoring` | A 40-statement PRD full of traps: misuse written with When, a runtime setting written with Where, a response that needs judgement, `or` between responses, a contradiction, a statement with no system, an `only` that must stay a prohibition, a schedule, an implementation choice, business decisions, open limits, a time with no time zone, project dates. Also batching: more than 10 gaps. |
| `clean-feature` | A complete input: everything is written, and at most the coverage-gap question is asked. |
| `nfr-ids` | Functional and non-functional requirements take separate `FR` and `NFR` sequences, and a deadline on a behaviour is split into an `FR` and an `NFR`. |
| `followup-answers` | A follow-up turn: three of six questions are answered and a deadline is added. New requirements are marked `(new)` and continue the sequences, the unchanged requirement is not repeated, answered questions are not asked again, and unanswered ones keep their IDs. |
| `followup-first-requirements` | A follow-up turn after a first reply of questions only: the first requirements are still marked `(new)`, start at `FR-001`, and new questions continue after the highest `Q` ID. |
| `propose-system` | The input names no system and the project's README names one: the question carries it as `Proposed:`, the statement is shown as a draft without that name, and no requirement is written before the user confirms. The project is in the case's `dirty/` folder. |
| `code-facts` | The project holds the named system's code, and two facts in it would change a requirement: a rule the input does not mention that stops a response, and a value the input says is today's where the code has another. Each gets a question that names its file, the contradicted statement is not written, the other three are, and no requirement comes from the code ([#22](https://github.com/nibirsharif/agent-skills/issues/22)). |
| `code-no-facts` | The same project where the code differs from the input only in what the input changes (a status code, a return value): both statements are written and no question is asked because of the code. |
| `draft-slots` | One statement is complete, one lacks only a time zone, one lacks only its system, and one gives only an impression: the first is written, the next two are drafts with the question's ID where the missing part goes, and the impression gets questions and no draft ([#21](https://github.com/nibirsharif/agent-skills/issues/21)). |
| `vague-only` | Only impressions and no system: questions only, and no draft. |
| `assume-defaults` | The user asks for defaults: no value is assumed, and business decisions get no proposal. |
| `ask-location` | No path in the request, no `spec_output_dir` (the input is sent as written, not through the chat-only prompt): the reply is the one location question and no requirement. |
| `spec-dir` | The same request where the project's config sets `spec_output_dir`: the skill's `target.py` gives the folder, the file is saved at `docs/specs/password-reset/requirements.md`, the reply's last line states that path, and the location question is not asked ([#42](https://github.com/nibirsharif/agent-skills/issues/42)). The config is in the case's `dirty/` folder. |
| `routing-gherkin` | Routing: a Given/When/Then request, which the skill's description excludes. The skill must not fire. |

Each case folder holds:

- `input.md`: the input. The runner wraps it in the prompt from [config.json](config.json), which names the skill, except in routing cases, which are sent as written.
- `checks.json`: the checks, in the format described in [evals/grading.py](../grading.py): line counts, patterns that must and must not appear, whether the skill must fire, expectations for the LLM judge, and a checklist to review by hand.
- `golden.md`: a hand-written reply that passes every check. `make test` grades it, so a check that no reply could pass fails the build. Required when the case checks the reply.
- `bad.md` (optional): a reply with known faults. `make test` confirms it fails.
- `committed/` (optional): files copied over the skill's fixture before it is committed, for a case that needs its own committed files, such as a project config.
- `dirty/` (optional): files copied over the skill's fixture after it is committed, and left uncommitted, for a case that needs a dirty working tree.

A skill whose cases need code to work on names a folder in its `config.json` as `"fixture"`. Every case of that skill starts in a copy of it, committed as a git repository on `main`. Without one, each run starts in an empty folder.

Besides each case's checks, every reply except in a `"fires": false` case must pass [hooks.py](hooks.py): the skill's lint finds no errors, and the reply holds nothing but requirement, draft, and question lines (and the "N more open questions" line), except that its last line may state the path of a saved file.

## Running

Run every case through Claude Code, or name cases:

```bash
make eval SKILL=write-spec
python3 evals/run.py write-spec prd-solar-monitoring clean-feature
```

The runner loads this repo's skills as a plugin, so no install is needed. If write-spec is also installed with `make install`, it loads twice; run `make uninstall` first for a clean routing result. All runs start in parallel, so a full run takes about as long as the slowest case. Options:

- `MODEL=sonnet` (`--model`): the model for the agent.
- `RUNS=3` (`--runs`): run each case 3 times. Agents vary between runs, and whether a skill fires varies most, so read routing cases over several runs.
- `JUDGE=1` (`--judge`): also grade each case's `expectations` with an LLM judge, one more call per run.
- `--agent "my-agent --print"`: another agent command, which takes the prompt as its last argument. Checks that need a transcript are then reported as skipped.

```bash
make eval SKILL=write-spec MODEL=sonnet RUNS=3 JUDGE=1
```

Replies, run stats (turns, time, cost, how often the lint ran or was blocked, and which skills fired), full transcripts (`.jsonl`), judge results, and any error output are saved in `runs/`, which git ignores. Work through each case's "Review by hand" list: the checks cannot tell whether a value was invented.

## Questions about the code

`code-facts` and `code-no-facts` are the cases for [#22](https://github.com/nibirsharif/agent-skills/issues/22): write-spec may ask about a fact in a named system's code that would change a requirement, and writes no requirement from the code. All runs on `claude-sonnet-5-5` with Claude Code 2.1.327, 24 November 2026.

| Wording | `code-facts` | `code-no-facts` | What the misses were |
|---------|--------------|-----------------|----------------------|
| The lookup as a line under Before writing | 2 of 3 | 0 of 3 read the code | 4 of the 6 runs never looked at the project, so they read neither the rules for the code nor the code: the `code-facts` miss, which wrote the 30 days as a requirement, and all three `code-no-facts` runs, whose replies passed without the code. The case now also checks that the code was read. |
| The lookup as Workflow step 2 | 5 of 6 | 6 of 6 | All 12 runs listed the project and read the rules. The miss read search results in place of the files and never saw the rule in `schema.sql`. Two `code-no-facts` runs were first marked failed by a check that expected a path with a slash; their replies were right. |
| The same, and each file read in full | 3 of 3 | 15 of 15 | The whole-suite run with the judge, and 12 more `code-no-facts` runs the same night. All 18 runs read each file in full, 4 files at most. |

In the 10 passing `code-facts` runs both questions name the right file, the three other statements are written from the input's words, and the 30 days are not written. Five of them also ask, naming a file, whether a cancelled booking still counts as a stored booking. No `code-no-facts` run asked a question because of the code or put its status 400 in the reply.

Not measured: the limit of 5 files, since the cases' project holds 5; a large project, where 5 files may not hold the fact; and the real project of [the first real run](../real-runs/2026-11-17.md), which was not run again.

### A shorter wording, not kept

The rules in `code-facts.md` are 809 words. A cut to 664 words was tried the same day and not kept. It removed what the rules repeat from `SKILL.md` and `ears-rules.md` (when to read them, the limit of 10 questions, that the code is not input), the reasons given for two rules, and the requirement lines of the example.

| Rules | `code-facts` | `code-no-facts` | `propose-system` |
|-------|--------------|-----------------|------------------|
| Cut | 9 of 9 | 13 of 15 | 6 of 6 |
| 809 words | 3 of 3 | 15 of 15 | 3 of 3 |

- Both `code-no-facts` misses opened the reply with "Lint is clean, so here are the requirements." before a correct reply. With this few runs a split of 2 in 15 against 0 in 15 comes up by chance about 1 time in 4, so the cut is neither shown to cause the line nor cleared. It saved only words the budget does not count, so the 809 words stay.
- One `code-facts` run on the cut rules read a search's output in place of the files, as the miss under the second wording did. The files are short, so the output showed both facts and the run passed.
- The first cut, of 642 words, had dropped the line about a system in a `Proposed:` the user has not confirmed. That line is used: 4 of the 9 `propose-system` runs opened the rules with only such a system, and none read code.
- The whole-suite run on the cut rules was 33 of 36. Besides one of the `code-no-facts` misses, two `ask-location` replies put a sentence before the question, such as "No target is set, so I'm asking before writing anything." `ask-location` does not open these rules. It missed the same way three times on 19 November, and passed 3 of 3 before and after that run the same day.

## Drafts

`draft-slots` is the case for [#21](https://github.com/nibirsharif/agent-skills/issues/21), and `propose-system` and `vague-only` check drafts too: a statement that lacks only a system name or a value is shown as a `Draft:` line below the questions, and an impression gets none. The rules are in the skill's `references/drafts.md`, which the workflow opens only after the requirements and questions are linted. Read up front, the same rules made every reply ask fewer questions: see the [benchmark record](benchmark/after-drafts.md). All runs on `claude-sonnet-5-5` with Claude Code 2.1.327, 25 November 2026, 3 runs each with the judge.

| Run | Passed | What the misses were |
|-----|--------|----------------------|
| The suite, first wording of `drafts.md` | 35 of 39 | Two replies opened with a sentence: "No statement lacks a value that a question asks for, so there are no drafts." in `clean-feature`, and one about the lint in `propose-system`. `drafts.md` now ends by saying what the reply's first line is, also when no draft was added. One `draft-slots` reply asked 9 questions where the case allowed 8; it allows 10 now. One `prd-solar-monitoring` reply wrote an installed add-on with `While`. |
| The suite, after that fix | 37 of 39 | No reply opened with a sentence. `nfr-ids` asked a fourth coverage question, with no draft involved. One `draft-slots` reply wrote the passive late-fee statement with the system of the statements around it; the input now says "The system adds a late fee", as `prd-solar-monitoring` does for its statement with no system. |
| `draft-slots` alone, 6 runs, after that | 5 of 6 | One reply wrote a draft for "Paying must be quick". The rule against a draft for an impression now names `fast`, `secure`, and `quick`. |
| The six cases a draft can appear in, after that | 18 of 18 | `draft-slots`, `vague-only`, `propose-system`, `prd-solar-monitoring`, `clean-feature`, `assume-defaults`. |

Not measured: the follow-up turn with drafts. `followup-first-requirements` and `followup-answers` passed 6 of 6 in each suite run, but their first replies, which the input quotes, hold no draft.

## A sentence before the reply

[#42](https://github.com/nibirsharif/agent-skills/issues/42): some replies open with one sentence about the step the agent just finished, such as "No target is set, so I'm asking before writing anything." or "Lint is clean, so here are the requirements." Everything after the sentence is right. All runs below are on `claude-sonnet-5-5` with Claude Code 2.1.327, 26 and 27 November 2026.

**The location question.** `ask-location`, 20 runs at a time:

| Skill text | Passed | The misses |
|------------|--------|------------|
| `master` at 0.20.0 | 18 of 20 | Both open with the sentence. |
| A rule in `SKILL.md` that the last message is the reply and never starts with a sentence about what was found, with two of the sentences as examples | 16 of 20 | All four open with the sentence. Not kept. |
| `scripts/target.py` reads the config and prints the question | 60 of 60, then 5 of 6 in two whole-suite runs | One reply: "No target is known, so I can't write the requirements yet." |

- Without the script the agent looked for the two config files itself, in two or three commands of its own choosing, and some runs listed the user's home folder. In the 40 runs without it, the 14 that had a thinking step before the last message all passed, and 6 of the other 26 opened with the sentence: with no thinking step, what the agent concluded from its lookups went into the reply.
- With the script, the last thing the agent reads is the question itself, and it runs one command where it ran two or three: 5 turns for 7, and $0.125 a run for $0.137. No run with the script had a thinking step before the last message, so the 65 of 66 are all of the kind that missed 6 of 26.
- The three batches of 20 differ in one sentence each (below); the two suite runs are on the text that was kept.

**A sentence before the script runs.** In 12 of the 66 runs the agent wrote a sentence before the command, such as "No path named; run target.py." The eval grades the last message only, so these runs pass, and a person in an interactive session sees that sentence above the question. No run without the script had one. Two wordings against it changed nothing and were not kept: "Write no text between tool calls." in `SKILL.md`'s Output (2 of 20, against 3 of 20 without it) and "Write no text before the command" beside the step in `saving.md` (6 of 20).

**Every other reply.** Not fixed. Two whole-suite runs with the judge, 14 cases at 3 runs each:

| Run | Passed | The misses |
|-----|--------|------------|
| The lint's last line reworded to "When you send the reply, start it with its first FR-, NFR-, or Q- line: no sentence before it, and no word about this lint." | 38 of 42 | Two open with a sentence: the one `ask-location` miss above, and a `followup-first-requirements` reply that explained why it kept a wording the lint had marked `CHECK`. The reworded line was the last thing that reply's agent read, so it was not kept. The other two: `nfr-ids` asked a fourth question, and `draft-slots` wrote no requirement for its one complete statement. |
| The text that was kept | 41 of 42 | `code-no-facts` opened with "No statement qualifies for a draft, so the reply stays as linted." |

So about 1 reply in 40 that holds requirements still opens with a sentence (2 of the 72 here), as before the change, and a suite run of 42 has one more often than not. Each of them reports the step just finished: the lint, or the drafts. A rule against it is already the last thing the agent reads in both places, in the lint's last line and at the end of `drafts.md`. Showing that a further change helps at this rate needs a few hundred runs. It is left as it is: a person reads the reply, and the sentence changes neither the lines after it nor the saved file.

`spec-dir`, the new case for the folder the script prints, passed 6 of 6 in the two suite runs: every run ran the script, read neither config file itself, and saved to `docs/specs/password-reset/requirements.md`. Three runs before them did the same and were failed only by [hooks.py](hooks.py), which did not yet allow the last line that states the saved file's path.

## The size of a spec

Measured for [#44](https://github.com/nibirsharif/agent-skills/issues/44), 27 November 2026 (`claude-sonnet-5-5`, Claude Code 2.1.327); no rule of write-spec changed. The benchmark's follow-up turn now has a size measure, counted by [benchmark/size.py](benchmark/size.py): 1.82 requirements for each input statement after the turn (71 for 39 in each of three runs), about a third of them from coverage-gap answers, and 37 questions still open. The baseline, and the two options for write-spec that were tried and not taken (coverage gaps one level deep, and a size line at the end of the reply), are in [benchmark/baseline-size.md](benchmark/baseline-size.md). The same script counts a saved requirements file by source; the real run's 29 requirements are in [its record](../real-runs/2026-11-17.md#the-29-requirements-by-source).

## Adding a case

Copy a case folder, write the input, and write `golden.md` first. Then write checks that the golden passes and that a plausible wrong reply fails, and run `make test`.
