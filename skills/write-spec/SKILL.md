---
name: write-spec
description: Write software requirements in EARS (Easy Approach to Requirements Syntax) from a feature description, user story, or draft requirements. Each requirement is one `shall` sentence using the While, When, Where, and If-then patterns and naming the one system that acts. Writes every requirement the input fully supports and asks questions for the rest instead of guessing systems, values, or thresholds; can save the result to a requirements file and extend it later. Use when the user asks to write, convert, rewrite, or tighten requirements, a requirements spec, `shall` statements, or EARS acceptance criteria, or asks for the requirements of a feature without naming a format. Not for Given/When/Then (Gherkin) scenarios, PRDs, or design documents.
---

# Write Spec (EARS)

Turn a feature description, user story, or draft requirements into EARS requirements. Write every requirement the input fully supports; turn every gap into a question.

## Before writing

Read both reference files in full before producing anything:

- [references/ears-rules.md](references/ears-rules.md): sentence structure, the five patterns, choosing a keyword, system and response rules, banned words, and what to rewrite versus ask. This file is authoritative.
- [references/ears-template.md](references/ears-template.md): response and file formats, question format, and worked examples.

## Workflow

1. **Split the input** into single requirements: one system reacting to one set of conditions. In a user story, the role and goal describe the trigger and the response.
2. **Fill the slots** for each requirement from the input only: system, response, and any feature, precondition, and trigger.
3. **Choose the keywords** as the rules' "Choosing the keyword" section says.
4. **Write the sentence** in the fixed clause order.
5. **Check it** against every rule, banned words included. Fix what the rules say to rewrite. Anything still missing is a gap: ask about it and leave that requirement out.
6. **Check the set.** One term per thing, no duplicates, no two requirements that contradict each other or a requirement already in the target file.

## Output

Return the requirements that pass every rule, then the open questions, in the format in the template file. If no requirement can be written, return only the questions.

Number requirements from `REQ-001`, or continue from the highest ID already in this conversation or the target file. When an answer or new input changes an existing requirement, rewrite it under its existing ID. Never renumber requirements or reuse an ID.

When the user answers questions, return the requirements the answers unblock, any requirements the answers change, and the questions still open.

## Saving to a file

Pick the path, in this order:

1. A path the user named.
2. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Use `<spec_output_dir>/<feature-name>/requirements.md`, where `<feature-name>` is the input's feature in kebab-case (for example `password-reset`). Resolve a relative `spec_output_dir` against the project root.
3. Neither is set: write no file.

Write a file only when at least one requirement was written.

If the file already exists and holds `REQ-NNN` lines, update it:

- Add new requirements after the last one, continuing its numbering.
- Rewrite changed requirements in place under their existing IDs.
- Replace the open questions section with the current open questions, or remove it when none remain.
- Delete a requirement only when the user asks, and never reuse its ID.

If the file exists but holds no `REQ-NNN` lines, say so and ask before changing it. After writing, state the path in one line.
