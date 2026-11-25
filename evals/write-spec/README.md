# write-spec evals

Made-up inputs that exercise the write-spec skill's rules, each with automatic checks and a short list to review by hand. No real product document is used here.

| Case | Tests |
|------|-------|
| `prd-solar-monitoring` | A 40-statement PRD full of traps: misuse written with When, a runtime setting written with Where, a response that needs judgement, `or` between responses, a contradiction, a statement with no system, an `only` that must stay a prohibition, a schedule, an implementation choice, business decisions, open limits, a time with no time zone, project dates. Also batching: more than 10 gaps. |
| `clean-feature` | A complete input: everything is written, and at most the coverage-gap question is asked. |
| `nfr-ids` | Functional and non-functional requirements take separate `FR` and `NFR` sequences, and a deadline on a behaviour is split into an `FR` and an `NFR`. |
| `followup-answers` | A follow-up turn: three of six questions are answered and a deadline is added. New requirements are marked `(new)` and continue the sequences, the unchanged requirement is not repeated, answered questions are not asked again, and unanswered ones keep their IDs. |
| `followup-first-requirements` | A follow-up turn after a first reply of questions only: the first requirements are still marked `(new)`, start at `FR-001`, and new questions continue after the highest `Q` ID. |
| `propose-system` | The input names no system and the project's README names one: the question carries it as `Proposed:`, and no requirement is written before the user confirms. The project is in the case's `dirty/` folder. |
| `code-facts` | The project holds the named system's code, and two facts in it would change a requirement: a rule the input does not mention that stops a response, and a value the input says is today's where the code has another. Each gets a question that names its file, the contradicted statement is not written, the other three are, and no requirement comes from the code ([#22](https://github.com/nibirsharif/agent-skills/issues/22)). |
| `code-no-facts` | The same project where the code differs from the input only in what the input changes (a status code, a return value): both statements are written and no question is asked because of the code. |
| `vague-only` | Only impressions and no system: questions only. |
| `assume-defaults` | The user asks for defaults: no value is assumed, and business decisions get no proposal. |
| `ask-location` | No path in the request, no `spec_output_dir` (the input is sent as written, not through the chat-only prompt): the reply is the one location question and no requirement. |
| `routing-gherkin` | Routing: a Given/When/Then request, which the skill's description excludes. The skill must not fire. |

Each case folder holds:

- `input.md`: the input. The runner wraps it in the prompt from [config.json](config.json), which names the skill, except in routing cases, which are sent as written.
- `checks.json`: the checks, in the format described in [evals/grading.py](../grading.py): line counts, patterns that must and must not appear, whether the skill must fire, expectations for the LLM judge, and a checklist to review by hand.
- `golden.md`: a hand-written reply that passes every check. `make test` grades it, so a check that no reply could pass fails the build. Required when the case checks the reply.
- `bad.md` (optional): a reply with known faults. `make test` confirms it fails.
- `committed/` (optional): files copied over the skill's fixture before it is committed, for a case that needs its own committed files, such as a project config.
- `dirty/` (optional): files copied over the skill's fixture after it is committed, and left uncommitted, for a case that needs a dirty working tree.

A skill whose cases need code to work on names a folder in its `config.json` as `"fixture"`. Every case of that skill starts in a copy of it, committed as a git repository on `main`. Without one, each run starts in an empty folder.

Besides each case's checks, every reply except in a `"fires": false` case must pass [hooks.py](hooks.py): the skill's lint finds no errors, and the reply holds nothing but requirement and question lines (and the "N more open questions" line).

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
| The same, and each file read in full | 3 of 3 | 3 of 3 | In the whole-suite run, with the judge. |

In the 10 passing `code-facts` runs both questions name the right file, the three other statements are written from the input's words, and the 30 days are not written. Five of them also ask, naming a file, whether a cancelled booking still counts as a stored booking. No `code-no-facts` run asked a question because of the code or put its status 400 in the reply.

Not measured: the limit of 5 files, since the cases' project holds 5; a large project, where 5 files may not hold the fact; and the real project of [the first real run](../real-runs/2026-11-17.md), which was not run again.

## Adding a case

Copy a case folder, write the input, and write `golden.md` first. Then write checks that the golden passes and that a plausible wrong reply fails, and run `make test`.
