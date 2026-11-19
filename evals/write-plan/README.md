# write-plan evals

Made-up requirements files that exercise the write-plan skill's rules, each with automatic checks and a short list to review by hand. Every run starts in an empty folder, so the requirements are pasted into the prompt and there is no codebase: a good reply says `None found.` for reuse instead of naming files.

| Case | Tests |
|------|-------|
| `missing-requirements` | The requirements file does not exist: one short reply that points to write-spec, and no plan. |
| `open-questions` | Two open questions block a requirement that is not written yet: the written requirements get a phase, the blocked requirement gets one `Blocked by` entry naming both questions, the closed question is not listed, and nothing is answered or planned for the blocked requirement. |
| `withdrawn` | A withdrawn requirement and one moved to `NFR-001`: neither withdrawn ID is planned, and the moved requirement is planned under its new ID. |
| `gap` | An open question decides the data model: the skill asks it, says the answer is recorded through write-spec, and writes no plan. |
| `multi-phase` | Nineteen requirements with a phase limit of 8: phases by flow, every ID in exactly one phase, no phase over the limits, and a deadline `NFR` placed with its `FR`. |
| `phase-dependency` | Eleven requirements written with the report first and submission in the middle: the phases follow what each step needs, not the order of the IDs. |
| `oversized-requirement` | One requirement that alone needs more than the 10-file phase limit: no plan, the requirement is named, and the user is sent to write-spec to split it. |
| `ask-location` | No `spec_output_dir`, no path, and the requirements sit in a folder the user moved them to (`dirty/notes/`): the whole reply is the location question, and the project is not searched. Sent as written, without the chat-only line. |
| `pasted-not-saved` | `withdrawn`'s input sent without the chat-only line: the plan is in chat, and its last line says it was not saved. |
| `routing-requirements` | Routing: a request to write requirements, which the skill's description excludes. The skill must not fire. |

The input requirements pass write-spec's lint (`python3 skills/write-spec/scripts/lint.py`). Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

```bash
make eval SKILL=write-plan
```

The `multi-phase` and `open-questions` goldens show the chat-only reply: the file template's sections, without the title block.

Known, on 16 November 2026 with `claude-sonnet-5-5` (Claude Code 2.1.322):

- Before the too-large stop was a rule, `oversized-requirement` passed 0 of 3: each reply spread FR-001 over three or four phases and gave the other phases a `**Requirements:**` line with no ID (`None alone (part of FR-001)`, `continues FR-001`).
- With the rule, it passed 4 of 4, each reply the stop line alone. `phase-dependency` passed 4 of 4 and `multi-phase` 4 of 4 beside it, and the whole suite 8 of 8 at one run each.
- The rule did not stop a plan it should write: the five benchmark inputs that need a plan each got one.

[benchmark/](benchmark/README.md) measures the quality of the phase cuts, which these cases do not.
