---
name: write-plan
description: Write an implementation plan from a saved EARS requirements file (requirements.md from write-spec). Explores the codebase first, then splits the approach into phases that are each independently mergeable as one reviewable PR, lists the REQ and NFR IDs each phase covers, and saves plan.md next to the requirements. Open questions are never answered here: requirements that wait on them are listed as blocked. Use when the user asks to plan, break down, phase, or sequence the implementation of a feature that has written requirements, or asks how to build it in reviewable steps. Not for writing requirements, the per-phase task breakdown, or code.
---

# Write Plan

Turn a feature's `requirements.md` into `plan.md`: the approach, split into phases that each merge on their own. Read the code first; cover only requirements that are written.

## Reply contract

Your reply is one of three things, and its first character is the first character of that thing:

1. **The plan:** it starts with `## 1. Approach`. Nothing comes before it: not "Confirmed…", not "The folder is empty…", not "Planning from…". Say that there is no codebase or no file on disk inside the Approach.
2. **The stop line**, when the requirements file is missing or holds no requirement: exactly `No requirements file found at <path>. Run write-spec first to write the requirements, then run write-plan again.` Never offer options, ask about the feature, describe the empty folder, or draft requirements.
3. **The questions**, when an open question decides the core approach.

Write no text between tool calls. Details are in [Output](#output).

## Before writing

- Read [references/plan-rules.md](references/plan-rules.md) in full before producing anything: how to read the requirements file, what to explore, how to size and order phases, where each `NFR` goes, blocked requirements, and the validation checklist. This file is authoritative.
- Before writing or updating a file, read [references/plan-template.md](references/plan-template.md): the file template and how to fill it.
- Read [references/examples.md](references/examples.md) before your first reply in a conversation, and again when unsure of a phase split, a blocked entry, or a saved file.

## Scope

This skill writes the plan only. It does not write requirements, the per-phase task breakdown, or code. When asked for one, say so: for requirements or answers to open questions, point to `write-spec`; never write them here.

Never invent a requirement, a file, or a utility. A plan line names only what the requirements file states and what you found in the code.

## Workflow

Work silently. Write no text between tool calls and no text before the reply: no "confirmed", "the folder is empty", or "planning from…" lines. The only text you write is the reply that [Output](#output) describes.

1. **Find and read the requirements.** Find them as [Saving to a file](#saving-to-a-file) says. If none were pasted and the file is missing or holds no requirement, reply with one line that names the path and suggests `write-spec`, and stop. Do not ask about the feature, draft requirements, or offer to run `write-spec` yourself. If a `plan.md` already exists beside the file, read it too: you are updating it.
2. **Sort the requirements**, as the rules' "Reading the requirements file" section says: written `REQ` and `NFR` requirements, withdrawn lines, and open `Q-` questions with the requirements that wait on them.
3. **Check the approach.** If an open question would change the core approach (the architecture, a data model, a system boundary), stop and ask it in chat, and say the answer belongs in the requirements through `write-spec`. Do not plan around a guess. Otherwise go on.
4. **Explore the codebase** as the rules' "Exploring the code" section says.
5. **Choose the approach and the phases** as the rules say: group, order, split, and place each `NFR`.
6. **Fill each phase**: scope, requirement IDs, code to reuse, interface and data changes, how to verify, open questions.
7. **Validate** against the rules' checklist. Fix what fails; a check you cannot pass is a question, not a plan line.
8. **Return** the plan as [Output](#output) says, and **save** if a path is set.

## Output

- Saved: state the path in one line, then one line per phase: `Phase <n>: <title> (<IDs>)`, then the blocked requirements and the open questions' IDs. Never paste the whole file.
- Chat only: the plan itself, in the file template's order, without the title block and without Revision History. The reply's first line is `## 1. Approach` and it ends with the last open question, or `None.`. No preamble, no closing note, and no account of how you worked: not what you checked, found empty, or are about to produce. That there is no codebase, or no file on disk, goes in the first sentence of Approach, never above the heading.
- Stopped, or asking: only the one-line reason or the questions, with the same rule. For a missing or empty requirements file, reply exactly: `No requirements file found at <path>. Run write-spec first to write the requirements, then run write-plan again.` Never offer options, ask about the feature, or describe the empty folder.

## Saving to a file

Find the requirements, in this order:

1. Requirements the user pasted into the conversation. Plan from them even when they name a path that does not exist on disk.
2. A path the user named.
3. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. Use `<spec_output_dir>/<feature-name>/requirements.md`, where `<feature-name>` is the feature in kebab-case. If the user names no feature, list the existing `<spec_output_dir>/*/requirements.md` files and ask which one; if only one exists, use it.
4. None of these: ask for the path.

Write `plan.md` in the same folder as `requirements.md`, and only when that `requirements.md` exists on disk and was found through a path the user named or through `spec_output_dir`. Otherwise, or when the user asks for chat only, reply in chat only.

Phase sizes come from the same config files: `plan_max_requirements_per_phase` (default 8) and `plan_max_files_per_phase` (default 10).

If `plan.md` already exists, extend it as the template says and keep every phase number. When a newly written requirement could join an existing phase, ask which phases have merged before placing it. If `plan.md` exists but does not follow the template, change nothing yet: say so and ask before rewriting it.

After writing, state the path in one line.
