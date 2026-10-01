---
name: write-spec
description: Write software requirements in EARS (Easy Approach to Requirements Syntax) from a feature description, user story, or draft requirements. Each requirement is one `shall` sentence using the While, When, Where, and If-then patterns and naming the one system that acts. Writes every requirement the input fully supports and asks questions for the rest instead of guessing systems, values, or thresholds; can save the result to a requirements file and extend it later. Use when the user asks to write, convert, rewrite, or tighten requirements, a requirements spec, `shall` statements, or EARS acceptance criteria, or asks for the requirements of a feature without naming a format. Not for Given/When/Then (Gherkin) scenarios, PRDs, or design documents.
---

# Write Spec (EARS)

Turn a feature description, user story, or draft requirements into EARS requirements, and keep them in a requirements specification file when a path is set. Write every requirement the input fully supports; turn every gap into a question.

## Before writing

- Always read [references/ears-rules.md](references/ears-rules.md) in full before producing anything: sentence structure, the five patterns, choosing a keyword, system and response rules, testability, banned words, functional versus non-functional, what to rewrite versus ask, and the validation checklist. This file is authoritative.
- Before writing or updating a file, read [references/ears-template.md](references/ears-template.md): the specification file template and how to fill it.
- Read [references/examples.md](references/examples.md) before your first reply in a conversation, and again whenever you are unsure of a keyword, a question, a follow-up reply, or a saved file.

## Scope

This skill writes EARS requirements only. It does not write Given/When/Then (Gherkin) scenarios, test cases, PRDs, design or architecture documents, or code. When asked for one of these, say that this skill does not produce it and offer EARS requirements for the same input. Never convert the input silently into another format.

Stop and ask instead of writing when:

- The input states no behaviour or property of any system. Write nothing, and ask what the system must do.
- The user asks you to assume or use defaults. Still write no value the user did not give: ask each gap as a question, with a proposed value where [Output](#output) allows one, and write the requirement after the user confirms.
- The user insists on a banned word or an untestable requirement. Do not write it. Keep its question open and say once which rule blocks it.

## Workflow

1. **Read the target file.** Find it as [Saving to a file](#saving-to-a-file) says, and read it if it exists: its highest `FR`, `NFR`, and `Q` IDs, its systems and terms, and its requirements.
2. **Split the input** into single requirements: one system reacting to one set of conditions. In a user story, the role and goal describe the trigger and the response.
3. **Fill the slots** for each requirement from the input, the user's answers, and the target file only: system, response, and any feature, precondition, and trigger.
4. **Choose the keywords** as the rules' "Choosing the keyword" section says.
5. **Write the sentence** in the fixed clause order.
6. **Classify** each requirement as functional or non-functional, as the rules' "Functional or non-functional" section says. The class sets the ID: `FR` for functional, `NFR` for non-functional (see [IDs](#ids)). A statement that gives a behaviour and a threshold on how fast or how well it happens becomes two requirements: an `FR` for the behaviour and an `NFR` for the threshold.
7. **Validate.** Run every item of the rules' validation checklist on each requirement and on the set. Fix what the rules say to rewrite. A requirement that still fails an item is not output: ask about the gap instead. Then run the [lint](#lint) on the draft. This step is required.
8. **Look for coverage gaps.** For each `When` requirement whose trigger has an evident failure case that the input does not cover (invalid or missing input, a timeout, a failure of another system), ask what the system does in that case. Never write the `If ... then` requirement for it yourself.
9. **Ask.** Give every open question an ID, and put the most important ones in this reply, as [Output](#output) says. Hold back a question whose wording depends on another's answer until that answer arrives.
10. **Return** the requirements that passed step 7, then the open questions, then **save** if a target path is set.

## Output

Return the requirements that pass the checklist, `FR` lines first and then `NFR` lines, then the open questions. If no requirement can be written, return only the questions. Nothing else: no preamble, no summary, no closing note, and no title, priority, or rationale on a requirement. Never mention the lint, the checklist, the rules, or how you worked; act on their findings without reporting them. The reply's first line is its first `FR-`, `NFR-`, or `Q-` line, and the only other line it may hold is the `<N> more open questions after these.` line.

```
FR-001: <EARS sentence>

FR-002: <EARS sentence>

NFR-001: <EARS sentence>

Q-001: <one direct question>? Proposed: <value>.
```

Put a blank line between lines so each renders on its own.

Ask one gap per question, on one line, for exactly what is missing: a system, value, unit, limit, threshold, name, or the response to an evident failure case. One gap is one decision the user makes. A value with its parts is one gap: a number with its unit, a time with the percentage of cases it holds for. Two things the user could decide separately are two questions: what a limit counts per, and how high it is. No padding, hedging, or apologies.

Add `Proposed:` only when the input suggests the value, or a named standard or common practice sets it (for example SPF, DKIM, and DMARC for email sender authentication, or WCAG 2.2 level AA). Never propose a business decision: a target, limit, retry count, retention period, price, or schedule that the business must choose. When there is nothing to propose, leave `Proposed:` out; never write `Proposed: none`. Never write the requirement until the user confirms the value.

Ask at most 10 questions in one reply. Put first the questions that unblock the most requirements, then the rest in input order. When more are open, end with one line: `<N> more open questions after these.` The user can answer by ID, or accept proposals with `accept Q-001, Q-004` or `accept all proposed`. Treat an accepted proposal as the user's answer.

When the user answers questions or adds input, return the requirements the answers change marked `(changed)` after the ID, the requirements they unblock marked `(new)`, and the next open questions, at most 10.

## IDs

- Functional requirements are `FR-001`, `FR-002`, and so on; non-functional requirements are `NFR-001`, `NFR-002`, and so on; questions are `Q-001`, `Q-002`, and so on. These are three separate sequences.
- Continue each sequence from its own highest ID in this conversation or the target file, whichever is higher. An answered question never becomes a requirement ID: it closes, and the requirement it unblocks takes the next free `FR` or `NFR` ID.
- A requirement's prefix is fixed when it is first written. When an answer or new input changes a requirement but not its class, rewrite it under its existing ID.
- When an answer shows that a requirement belongs to the other class, replace its text with `Withdrawn. Moved to <new ID>.` and write it under the next free ID of the other sequence.
- When the user withdraws or deletes a requirement, replace its text with `Withdrawn.` and keep the line, so its ID is never reused.
- An answered question is closed and drops out of the open questions in chat. In the file it becomes `Q-NNN: Closed. Answer: <the user's answer>`, so its ID is never reused and the answer stays on record.
- Never renumber.

## Saving to a file

Pick the path, in this order:

1. A path the user named.
2. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. Use `<spec_output_dir>/<feature-name>/requirements.md`, where `<feature-name>` is the input's feature in kebab-case (for example `password-reset`). First look at the existing `<spec_output_dir>/*/requirements.md` files: if one already covers this feature, use it. Ask when the input names no feature, or when more than one existing file could match.
3. Neither is set: write no file. If the user asked to save, ask for the path.

Write a file only when at least one requirement was written. A new file uses the [specification file template](references/ears-template.md).

If the file already exists and follows the template, update it:

- Add new `FR` lines at the end of the Functional section and new `NFR` lines at the end of the Non-Functional section, each with its source comment.
- Rewrite changed and withdrawn requirements in place under their existing IDs.
- Close answered questions in place and add new questions at the end of the section. The file holds every open question, including those not yet asked in chat.
- Add to Summary, Scope (including its Systems line), and References only what the new input states.
- Raise the version, update the date, and add one Revision History row, as the template says.

If the file exists but does not follow the template, change nothing yet. Say so and ask before rewriting it:

- If it holds `FR-NNN` lines and the user agrees, move it into the template. Keep every `FR` ID and every requirement's text. Turn each open question it lists into a `Q-NNN` line, in its order, continuing from the highest `Q` ID in the file.
- If it holds no `FR-NNN` lines, ask whether to use another path instead.

After writing, state the path in one line.

## Lint

Run [scripts/lint.py](scripts/lint.py) on every draft reply before you return it, and on every file you save. Do not skip it. Pass the draft on standard input, in one command and with no temporary file:

```bash
python3 <this skill folder>/scripts/lint.py - <<'EOF'
<the draft reply>
EOF
```

For a saved file, run `python3 <this skill folder>/scripts/lint.py <file>`.

- Fix every `ERROR`, then run it again until none remain.
- For each `CHECK`, reread the rule it names and fix the line unless the words are used in an allowed sense.
- Never report lint results in the reply.
- The lint checks only the mechanical rules. A clean result does not replace the validation checklist.

Skip the lint only when you cannot run commands at all; the checklist still applies.
