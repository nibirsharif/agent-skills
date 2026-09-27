# write-spec evals

Made-up inputs that exercise the write-spec skill's rules, each with automatic checks and a short list to review by hand. No real product document is used here.

| Case | Tests |
|------|-------|
| `prd-solar-monitoring` | A 40-statement PRD full of traps: misuse written with When, a runtime setting written with Where, a response that needs judgement, `or` between responses, a contradiction, a statement with no system, an `only` that must stay a prohibition, a schedule, an implementation choice, business decisions, open limits, a time with no time zone, project dates. Also batching: more than 10 gaps. |
| `clean-feature` | A complete input: everything is written, and at most the coverage-gap question is asked. |
| `vague-only` | Only impressions and no system: questions only. |
| `assume-defaults` | The user asks for defaults: no value is assumed, and business decisions get no proposal. |

Each case folder holds:

- `input.md`: the prompt given to the agent.
- `checks.json`: requirement and question counts, patterns that must and must not appear, and the manual checklist.
- `golden.md`: a hand-written reply that passes every check. `make test` grades it, so a check that no reply could pass fails the build.
- `bad.md` (optional): a reply with known faults. `make test` confirms it fails.

## Running

Run every case through Claude Code, or name cases:

```bash
evals/write-spec/run.sh
evals/write-spec/run.sh prd-solar-monitoring clean-feature
```

All runs start in parallel, so a full run takes about as long as the slowest case. Options, set as environment variables:

- `MODEL=sonnet` (or `haiku`, or a full model ID): the model for the default agent.
- `RUNS=3`: run each case 3 times, to see how much results vary between runs.
- `AGENT="my-agent --print"`: another agent command, which takes the prompt as its last argument.

```bash
MODEL=sonnet RUNS=3 evals/write-spec/run.sh
```

Replies, run stats (turns, time, cost, and how often the lint ran or was blocked), full transcripts (`.jsonl`), and any error output are saved in `runs/`, which git ignores.

Grade a reply you produced yourself:

```bash
python3 evals/write-spec/grade.py evals/write-spec/cases/clean-feature reply.md
```

A case passes when the reply has no lint errors, holds nothing but requirement and question lines (and the "N more open questions" line), and passes every automatic check. Then work through the "Review by hand" list: the checks cannot tell whether a value was invented. Agents vary between runs, so run a case a few times before trusting one result.

## Adding a case

Copy a case folder, write the input, and write `golden.md` first. Then write checks that the golden passes and that a plausible wrong reply fails, and run `make test`.
