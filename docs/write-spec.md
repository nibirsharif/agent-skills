# write-spec

Instructions the agent follows: [skills/write-spec/SKILL.md](../skills/write-spec/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Turns a feature description, user story, or rough requirements into EARS requirements: one `shall` sentence each, using the While, When, Where, and If-then patterns, naming the one system that acts. Functional requirements are `FR-001` onwards, non-functional ones `NFR-001` onwards, and questions `Q-001` onwards.

It writes every requirement the input fully supports and asks a question for each gap. It never invents a system, a value, or a threshold, even when you say "assume defaults": it asks, and proposes a value only when your input or a named standard (WCAG, SPF/DKIM/DMARC) gives one.

It writes requirements from your words only, never from what your code does today. When your input names a system that the project has code for, it reads a few of that system's files and asks about a fact there that would change a requirement, naming the file.

## When to use it

Type `/nibirsharif-skills:write-spec` (or `/write-spec` when installed from a clone). The agent never starts this skill on its own.

- You have a PRD, a story, or a paragraph and want testable requirements from it.
- You have vague "should" statements to tighten.
- You want to extend an existing `requirements.md` with new input or answers.

It does not write Given/When/Then scenarios, PRDs, design documents, or code. Ask for those and it says so and offers EARS instead.

## Output

A reply that is only requirement lines followed by question lines, at most 10 questions at a time. When more are open, the last line says how many.

```
FR-001: When a user submits an email address on the Forgot Password page, the auth service shall send a reset link to that address.

Q-001: What does the auth service do when the address is not registered? Proposed: send no email.
```

Answer by ID. `accept Q-001, Q-004` takes those proposals; `accept all proposed` takes every proposal. Changed requirements come back marked `(changed)`, newly unblocked ones `(new)`.

Set `spec_output_dir` in [the config](../README.md#configuration) and the result is saved to `<spec_output_dir>/<feature-name>/requirements.md`, which write-plan reads next. Without it, and with no path in your request, it asks where to save before writing anything; answer with a path or `chat only`, and nothing is written for `chat only`.

## FAQ

**Why does it ask new questions after I answer?** Every reply checks the whole set of requirements for cases nothing decides yet: a trigger that fails, the other side of a condition, and what a user receives when a `shall not` refuses a request. Your answers add requirements, and those can open such cases.

**Why does it ask which system, when my project has only one?** A requirement must name the system that acts, and the skill never writes a name you did not give. It does look at your saved requirements files, the root README, and the top-level folder names, and when they point to one system it asks with that name as `Proposed:`. Reply `accept Q-001` to use it.

**Why does a question name a file in my code?** Your input named a system the project has code for, and that code shows something that would change a requirement: a statement relies on something the code does not do or record, the code enforces a rule that your input does not mention and that stops a response from happening as you stated it, or the input says what the system does today and the code does otherwise. The question states the fact and its file so you can check it, and carries no proposal: whether the code or the input is right is your decision. It reads at most 5 files for a system, found by searching for your input's own words, so on a large project it can miss a fact. It never asks about what the feature changes, or about how the code is built.

**A behaviour with a deadline became two requirements. Why?** The behaviour is an `FR` and the threshold is an `NFR`, so the plan can place the threshold with the behaviour it constrains. A timeout that triggers a response stays functional.

**Why so many questions?** Each is one decision you would otherwise find out about in code review. Accept the proposals you agree with and answer the rest.

**Can I renumber?** No. IDs are never reused: withdrawn requirements keep their line as `Withdrawn.`, and answered questions become `Closed. <the question> Answer: ...`, so the file keeps both what was asked and what you decided.

## Verifying results

- Every requirement names one system and can be checked by a test.
- No value in a requirement is one you did not give or confirm, and none comes from the code.
- A question that names a file states something that file really shows.
- Each question is one decision, not two.
- The saved file keeps its IDs across updates.

## Related skills

First step of the chain: **write-spec** → [write-plan](write-plan.md) → [write-tasks](write-tasks.md). Open questions stay in `requirements.md` until you answer them here; the later skills treat requirements that wait on them as blocked.

## Acknowledgements

- write-spec is based on the [EARS Specification Writer prompt](https://gist.github.com/tsaqib/03080922501618c3594678551b8c3810) by [@tsaqib](https://github.com/tsaqib).
- EARS (Easy Approach to Requirements Syntax) was created by [Alistair Mavin](https://alistairmavin.com/ears/) and colleagues at Rolls-Royce.
