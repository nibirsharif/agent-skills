# write-spec

Instructions the agent follows: [skills/write-spec/SKILL.md](../skills/write-spec/SKILL.md). This page is for you: when to use it and what to expect.

## Overview

Turns a feature description, user story, or rough requirements into EARS requirements: one `shall` sentence each, using the While, When, Where, and If-then patterns, naming the one system that acts. Functional requirements are `FR-001` onwards, non-functional ones `NFR-001` onwards, and questions `Q-001` onwards.

It writes every requirement the input fully supports and asks a question for each gap. It never invents a system, a value, or a threshold, even when you say "assume defaults": it asks, and proposes a value only when your input or a named standard (WCAG, SPF/DKIM/DMARC) gives one.

## When to use it

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

Set `spec_output_dir` in [the config](../README.md#configuration) and the result is saved to `<spec_output_dir>/<feature-name>/requirements.md`, which write-plan reads next. Without it, nothing is written.

## FAQ

**A behaviour with a deadline became two requirements. Why?** The behaviour is an `FR` and the threshold is an `NFR`, so the plan can place the threshold with the behaviour it constrains. A timeout that triggers a response stays functional.

**Why so many questions?** Each is one decision you would otherwise find out about in code review. Accept the proposals you agree with and answer the rest.

**Can I renumber?** No. IDs are never reused: withdrawn requirements keep their line as `Withdrawn.`, and answered questions become `Closed. Answer: ...`.

## Verifying results

- Every requirement names one system and can be checked by a test.
- No value in a requirement is one you did not give or confirm.
- Each question is one decision, not two.
- The saved file keeps its IDs across updates.

## Related skills

First step of the chain: **write-spec** → [write-plan](write-plan.md) → [write-tasks](write-tasks.md). Open questions stay in `requirements.md` until you answer them here; the later skills treat requirements that wait on them as blocked.

## Acknowledgements

- write-spec is based on the [EARS Specification Writer prompt](https://gist.github.com/tsaqib/03080922501618c3594678551b8c3810) by [@tsaqib](https://github.com/tsaqib).
- EARS (Easy Approach to Requirements Syntax) was created by [Alistair Mavin](https://alistairmavin.com/ears/) and colleagues at Rolls-Royce.
