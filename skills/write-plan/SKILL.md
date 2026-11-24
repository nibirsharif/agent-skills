---
name: write-plan
description: Write an implementation plan from a saved EARS requirements file (requirements.md from write-spec). Explores the codebase first, then splits the approach into phases that are each independently mergeable as one reviewable PR, lists the FR and NFR IDs each phase covers, and saves plan.md next to the requirements. Open questions are never answered here; requirements that wait on them are listed as blocked. Not for writing requirements, the per-phase task breakdown, or code.
disable-model-invocation: true
---

# Write Plan

Turn a feature's `requirements.md` into `plan.md`: the approach, split into phases that each merge on their own. Read the code first; cover only requirements that are written.

## Reply contract

Your reply is one of four things, and its first character is the first character of that thing:

1. **The plan.**
   - Saved: the path in one line, then one line per phase, `Phase <n>: <title> (<IDs>)`, then the blocked requirements and the open questions' IDs. Never paste the whole file.
   - Chat only: the plan itself, in the file template's order, without the title block and without Revision History. The first line is `## 1. Approach`, whose first sentence says when there is no codebase or no file on disk, and the last is the last open question, or `None.`. When the requirements were pasted and the user did not ask for chat only, one more line ends it: exactly `Not saved: the requirements were pasted, not read from a file. Name a folder to save plan.md in.`
2. **The stop line**, and nothing else, when the requirements file is missing or holds no requirement: exactly `No requirements file found at <path>. Run write-spec first to write the requirements, then run write-plan again.`
3. **The questions**, and nothing else, when an open question decides the core approach, or the one location question when no path to the requirements is known: exactly `Where is requirements.md? Give its path, set `spec_output_dir` in `.agent-skills-config.yaml`, or paste the requirements.`
4. **The too-large line**, and nothing else, when one requirement alone needs more files than a phase may have: exactly `<ID> needs more than <n> files on its own. Split it with write-spec, then run write-plan again.`

Whichever it is, the reply has no preamble, no closing note, and no account of how you worked: not what you checked, counted, found empty, or are about to produce.

## Before writing

- Read [references/plan-rules.md](references/plan-rules.md) in full before producing anything. It is authoritative.
- Before writing a file, read [references/plan-template.md](references/plan-template.md).
- Read [references/examples.md](references/examples.md) before your first reply in a conversation, and again when unsure of a phase split, a blocked entry, or a saved file.

## Scope

This skill writes the plan only: no requirements, no per-phase task breakdown, no code. Never invent a requirement, a file, or a utility: a plan line names only what the requirements file states and what you found in the code. Never answer, close, or assume an open question; asked for an answer or for requirements, point to `write-spec`.

## Workflow

Work silently. Write no text between tool calls and none before the reply: the only text you write is the reply the contract describes.

1. **Find and read the requirements**, as [Saving to a file](#saving-to-a-file) says. A missing file, or one with no written requirement, is the stop line. If a `plan.md` already exists beside the file, read it: you are updating it, as [references/updating.md](references/updating.md) says.
2. **Sort the requirements** as the rules' "Reading the requirements file" section says: written, withdrawn, and blocked.
3. **Check for a stop** as the rules' "Stop and ask" section says: an open question that changes the core approach, or one requirement too large for a phase.
4. **Explore the codebase** as the rules' "Exploring the code" section says.
5. **Choose the approach and the phases** as the rules say: group, order, split, and place each `NFR`.
6. **Fill each phase** with the seven fields the rules list.
7. **Validate** against the rules' checklist. Fix what fails; a check you cannot pass is a question, not a plan line.
8. **Reply** as the [Reply contract](#reply-contract) says, and save as [Saving to a file](#saving-to-a-file) says.

## Saving to a file

Find the requirements, in this order:

1. Requirements the user pasted into the conversation. Plan from them even when they name a path that does not exist on disk.
2. A path the user names in this request.
3. `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. Use `<spec_output_dir>/<feature-name>/requirements.md`, where `<feature-name>` is the feature in kebab-case. If the user names no feature, list the existing `<spec_output_dir>/*/requirements.md` files and ask which one; if only one exists, use it.
4. None of these: A path to the feature's `requirements.md`, `plan.md`, or `tasks.md` that appears earlier in this conversation, named by the user or reported saved by a skill of this chain, gives the feature's folder, since the three files live together: use it when the file you need is in that folder and the user names no other feature. Otherwise ask for the path, and the question is your whole reply. Never search the project for the file or use a path you chose yourself.

Write `plan.md` in the same folder as `requirements.md` whenever the requirements were read from that file, found by one of these steps. Reply in chat only when the requirements were pasted or the user asks for chat only.

Phase sizes come from the same config files: `plan_max_requirements_per_phase` (default 8) and `plan_max_files_per_phase` (default 10).

If the `plan.md` that exists does not follow the template, change nothing yet: say so and ask before rewriting it.
