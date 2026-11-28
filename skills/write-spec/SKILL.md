---
name: write-spec
description: Write software requirements in EARS (Easy Approach to Requirements Syntax) from a feature description, user story, or draft requirements. Each requirement is one `shall` sentence using the While, When, Where, and If-then patterns and naming the one system that acts. Writes every requirement the input fully supports and asks questions for the rest instead of guessing systems, values, or thresholds; can save the result to a requirements file and extend it later. Not for Given/When/Then (Gherkin) scenarios, PRDs, or design documents.
disable-model-invocation: true
---

# Write Spec (EARS)

Turn a feature description, user story, or draft requirements into EARS requirements, and keep them in a requirements file when a path is set. Write every requirement the input fully supports; turn every gap into a question.

## Before writing

- Read [references/ears-rules.md](references/ears-rules.md) in full before producing anything. It is authoritative.
- Read [references/examples.md](references/examples.md) before your first reply in a conversation, and again when unsure of a keyword or a question.
- When the user answers your questions or adds input after an earlier reply, or the input changes, withdraws, or answers what the target file already holds, read [references/follow-ups.md](references/follow-ups.md) before replying.
- Before looking for `spec_output_dir`, or reading, writing, or updating a requirements file, read [references/saving.md](references/saving.md).

## Scope

This skill writes EARS requirements only. Asked for Given/When/Then (Gherkin) scenarios, test cases, a PRD, a design or architecture document, or code, say that it does not produce them and offer EARS requirements for the same input; never convert the input silently.

Stop and ask instead of writing when:

- No target is known: the user named no path and did not say chat only, and [scripts/target.py](scripts/target.py) prints `ask`, as [The path](references/saving.md#the-path) says. Write nothing yet. The question it prints is your whole reply, as written. After the user answers, go on with that answer for the rest of the conversation.
- The input states no behaviour or property of any system. Write nothing, and ask what the system must do.
- The user asks you to assume or use defaults. Still write no value the user did not give: ask each gap, with a proposal where [Output](#output) allows one.
- The user insists on a banned word or an untestable requirement. Do not write it. Keep its question open and say once which rule blocks it.

## Workflow

1. **Read the target file**, if it exists: its highest `FR`, `NFR`, and `Q` IDs, its systems and terms, and its requirements.
2. **Look for a named system's code.** When the input or an answer names a system, list the project's top-level folders. When one holds that system's code, read [references/code-facts.md](references/code-facts.md) and do what it says before step 3. Never skip the listing.
3. **Split the input** into single requirements: one system reacting to one set of conditions. In a user story, the role and goal describe the trigger and the response.
4. **Write each requirement** from the input, the user's answers, and the target file only, as the rules say.
5. **Check** each requirement and the set against the rules' [checklist](references/ears-rules.md#checklist), including coverage gaps. A requirement that still fails is not output: ask about its gap instead.
6. **Lint** the draft reply, as [Lint](#lint) says, which is required.
7. **Read [references/drafts.md](references/drafts.md)** once the lint is clean, and never before, and do what it says. Then return the reply, and save if a target path is set.

## Output

The reply holds `FR` lines, then `NFR` lines, then `Q` lines, then the `Draft:` lines step 7 adds, with a blank line between lines, and nothing else: no preamble, summary, or closing note, no title, priority, or rationale, and no word about the lint, the rules, or how you worked. Its first line is an `FR-`, `NFR-`, or `Q-` line.

```
FR-001: <EARS sentence>

Q-001: <one direct question>? Proposed: <value>.
```

- **IDs:** `FR` (functional), `NFR` (non-functional), and `Q` are three separate sequences. Each continues from its own highest ID in this conversation or the target file. Never renumber or reuse an ID.
- **One gap per question,** on one line, asking exactly what is missing. One gap is one decision the user makes: a number with its unit, or a time with the percentage of cases it holds for, is one gap; what a limit counts per and how high it is are two. No padding, hedging, or apologies.
- **`Proposed:`** only when the input suggests the value, a named standard or common practice sets it (SPF, DKIM, and DMARC for email sender authentication; WCAG 2.2 level AA), or the project names the one system a statement lacks, as [The system](references/ears-rules.md#the-system) says. Never propose a business decision: a target, limit, retry count, retention period, price, or schedule. With nothing to propose, leave `Proposed:` out. Write the requirement only after the user confirms.
- **At most 10 questions:** first those that unblock the most requirements, then the rest in input order, then coverage gaps. Hold back a question whose wording depends on another's answer. When more are open, end with the one line `<N> more open questions after these.`

## Lint

Run [scripts/lint.py](scripts/lint.py) on every draft reply, in one command with no temporary file, adding `--follow-up` before the `-` for any reply after the first in a conversation:

```bash
python3 <this skill folder>/scripts/lint.py - <<'EOF'
<the draft reply>
EOF
```

Fix every `ERROR` and rerun until none remain. For each `CHECK`, reread the rule it names and fix the line unless the words are used in an allowed sense. A clean lint does not replace the checklist. Skip it only when you cannot run commands.
