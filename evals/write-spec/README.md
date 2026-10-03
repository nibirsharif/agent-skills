# write-spec evals

Made-up inputs that exercise the write-spec skill's rules, each with automatic checks and a short list to review by hand. No real product document is used here.

| Case | Tests |
|------|-------|
| `prd-solar-monitoring` | A 40-statement PRD full of traps: misuse written with When, a runtime setting written with Where, a response that needs judgement, `or` between responses, a contradiction, a statement with no system, an `only` that must stay a prohibition, a schedule, an implementation choice, business decisions, open limits, a time with no time zone, project dates. Also batching: more than 10 gaps. |
| `clean-feature` | A complete input: everything is written, and at most the coverage-gap question is asked. |
| `nfr-ids` | Functional and non-functional requirements take separate `FR` and `NFR` sequences, and a deadline on a behaviour is split into an `FR` and an `NFR`. |
| `vague-only` | Only impressions and no system: questions only. |
| `assume-defaults` | The user asks for defaults: no value is assumed, and business decisions get no proposal. |
| `routing-shall-statements` | Routing: a request for shall statements that does not name the skill. The skill must fire. |
| `routing-gherkin` | Routing: a Given/When/Then request, which the skill's description excludes. The skill must not fire. |

Each case folder holds:

- `input.md`: the input. The runner wraps it in the prompt from [config.json](config.json), which names the skill, except in routing cases, which are sent as written.
- `checks.json`: the checks, in the format described in [evals/grading.py](../grading.py): line counts, patterns that must and must not appear, whether the skill must fire, expectations for the LLM judge, and a checklist to review by hand.
- `golden.md`: a hand-written reply that passes every check. `make test` grades it, so a check that no reply could pass fails the build. Required when the case checks the reply.
- `bad.md` (optional): a reply with known faults. `make test` confirms it fails.
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

## Adding a case

Copy a case folder, write the input, and write `golden.md` first. Then write checks that the golden passes and that a plausible wrong reply fails, and run `make test`.
