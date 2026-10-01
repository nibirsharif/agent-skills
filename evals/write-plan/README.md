# write-plan evals

Made-up requirements files that exercise the write-plan skill's rules, each with automatic checks and a short list to review by hand. Every run starts in an empty folder, so the requirements are pasted into the prompt and there is no codebase: a good reply says `None found.` for reuse instead of naming files.

| Case | Tests |
|------|-------|
| `missing-requirements` | The requirements file does not exist: one short reply that points to write-spec, and no plan. |
| `open-questions` | Two open questions block a requirement that is not written yet: the written requirements get a phase, the blocked requirement gets one `Blocked by` entry naming both questions, the closed question is not listed, and nothing is answered or planned for the blocked requirement. |
| `withdrawn` | A withdrawn requirement and one moved to `NFR-001`: neither withdrawn ID is planned, and the moved requirement is planned under its new ID. |
| `gap` | An open question decides the data model: the skill asks it, says the answer is recorded through write-spec, and writes no plan. |
| `multi-phase` | Nineteen requirements with a phase limit of 8: phases by flow, every ID in exactly one phase, no phase over the limits, and a deadline `NFR` placed with its `FR`. |
| `routing-phases` | Routing: a request to build saved requirements in reviewable PRs, without naming the skill. The skill must fire. |
| `routing-requirements` | Routing: a request to write requirements, which the skill's description excludes. The skill must not fire. |

The input requirements pass write-spec's lint (`python3 skills/write-spec/scripts/lint.py`). Case folders, the golden and bad replies, running, and adding a case work as described in [../write-spec/README.md](../write-spec/README.md).

```bash
make eval SKILL=write-plan
```

The `multi-phase` and `open-questions` goldens show the chat-only reply: the file template's sections, without the title block.
