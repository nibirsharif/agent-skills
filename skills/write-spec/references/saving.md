# Saving to a file

Read this before looking for `spec_output_dir`, or reading, writing, or updating a requirements file.

## The path

Pick the path in this order:

1. A path the user named.
2. Otherwise, unless the user asked for chat only, run [../scripts/target.py](../scripts/target.py) by its full path, with the project as the current directory. It reads the config files: do not look for or read them yourself. Do what it prints:
   - `dir <path>`: the folder, with a relative `spec_output_dir` already resolved against the project root. Use `<path>/<feature-name>/requirements.md`, where `<feature-name>` is the input's feature in kebab-case (for example `password-reset`). First look at the existing `<path>/*/requirements.md` files: if one already covers this feature, use it. Ask when the input names no feature, or when more than one existing file could match.
   - `ask <question>`: no folder is set. Write no requirement and run nothing more: `<question>` is your whole reply, as written.
3. Only when you cannot run commands, find the folder yourself: `spec_output_dir` from `.agent-skills-config.yaml` in the project root (the repository root, or the current directory outside a repository), else from `~/.agent-skills-config.yaml`. Resolve a relative `spec_output_dir` against the project root. When neither sets it, the whole reply is the one line `Where should I save the requirements? Give a path, set `spec_output_dir` in `.agent-skills-config.yaml`, or say "chat only".`

Write a file only when at least one requirement was written, and none when the user answers "chat only" or asked for chat only at the start. After writing, state the path in one line, the last of the reply, and run the lint on the file without `--follow-up`, since a file holds no markers: `python3 <this skill folder>/scripts/lint.py <file>`. Fix every `ERROR`.

## A new file

A new file copies the [template](#template) at the end of this file.

- Replace every `[...]` and `<...>`, and `YYYY-MM-DD` with today's date.
- Fill Summary, Scope, and References only with what the input states. Write `None given.` under any heading or subheading the input leaves empty.
- Write the Author only when the user gave a name; otherwise write `Not given.` Do not ask for it.
- The requirement lines in sections 3 and 4 show the pattern shapes. Replace them with the real requirements, `FR` lines in section 3 and `NFR` lines in section 4, and keep no line the input does not support. When requirements the input states for a section wait on open questions, end the section with `Pending: Q-011, Q-020.`, naming those questions; update it as questions close and remove it when none are left. A section with no requirements and nothing pending holds `None given.`
- End each requirement and question line with `<!-- Source: <the input statement or answer it comes from> -->`. For a coverage-gap question, name the requirement: `<!-- Source: coverage gap in FR-001 -->`.
- Keep one requirement or question per line, with a blank line between lines, no `(new)` or `(changed)` markers, and no `Draft:` lines: a statement shown as a draft is in the file only as its questions. No priority, dependencies, user story, or titled subsections.
- The Systems line lists every system the requirements name, spelled as they spell it.
- Section 5 holds every open question, including those not yet asked in chat, and every question answered before the file was written, closed in the form [Updating a file](#updating-a-file) gives. It holds `None.` only while there has never been a question.
- A new file is version 1.0.

## Updating a file

If the file exists and follows the template:

- Add new `FR` lines at the end of section 3 and new `NFR` lines at the end of section 4, each with its source comment.
- Rewrite changed and withdrawn requirements in place under their existing IDs, as [follow-ups.md](follow-ups.md#existing-ids) says, without the markers.
- Close each answered question in place as `Q-NNN: Closed. <the question as asked, without its Proposed: part> Answer: <the user's answer>`, so a reader sees what was asked and what was decided; `Closed. Answer: Yes.` means nothing on its own. Add new questions at the end of section 5.
- Add to Summary, Scope (including its Systems line), and References only what the new input states.
- Raise the minor version by one (1.0, 1.1, 1.2), update the date, and add one Revision History row that names the IDs added, changed, withdrawn, or closed.

If the file exists but does not follow the template, change nothing yet. Say so and ask before rewriting it:

- If it holds `FR-NNN` lines and the user agrees, move it into the template. Keep every `FR` ID and every requirement's text. Turn each open question it lists into a `Q-NNN` line, in its order, continuing from the highest `Q` ID in the file.
- If it holds no `FR-NNN` lines, ask whether to use another path instead.

## An example file

The password-reset requirements from [examples.md](examples.md#some-statements-complete-some-gaps), saved after the [follow-up reply](follow-ups.md#example) with `spec_output_dir: docs/specs`. The user gave no author name. The file is `docs/specs/password-reset/requirements.md`:

```markdown
# Requirements Specification: Password Reset

**Version:** 1.1
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

A registered user can reset a password through a reset link sent by email. The link expires, and reset requests are rate limited.

## 2. Scope

### In Scope

- Password reset through an emailed reset link

### Out of Scope

None given.

**Systems:** authentication service

## 3. Functional Requirements

FR-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address. <!-- Source: "When a registered user requests a password reset, the authentication service emails a reset link to their registered address." -->

FR-002: If a user opens a reset link more than 15 minutes after the reset link was sent, then the authentication service shall reject the reset link. <!-- Source: "The link expires 30 minutes after it is sent."; changed to 15 minutes by the user -->

FR-003: If a password-reset request is received for an account that already had at least 5 password-reset requests in the preceding 60 minutes, then the authentication service shall reject the request. <!-- Source: answers to Q-001 and Q-002 -->

FR-004: If a password-reset request names an email address that is not registered, then the authentication service shall not send an email. <!-- Source: answer to Q-003 -->

## 4. Non-Functional Requirements

NFR-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address within 2 minutes of receiving the request for 99% of requests. <!-- Source: "the reset email must go out within 2 minutes of the request for 99% of requests" -->

## 5. Open Questions

Q-001: Closed. Is the password-reset rate limit counted per account or per IP address? Answer: per account. <!-- Source: "Reset requests should be rate limited." -->

Q-002: Closed. How many password-reset requests does the rate limit allow, and in what time window? Answer: at most 5 in any rolling 60 minutes. <!-- Source: "Reset requests should be rate limited." -->

Q-003: Closed. What does the authentication service do when a password-reset request names an email address that is not registered? Answer: send no email. <!-- Source: coverage gap in FR-001 -->

Q-004: What does the authentication service display to a user whose password-reset request names an email address that is not registered? <!-- Source: coverage gap in FR-004 -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft: FR-001, FR-002, Q-001 to Q-003 |
| 1.1 | 2026-03-03 | Not given. | Added FR-003, FR-004, NFR-001; changed FR-002; closed Q-001 to Q-003; added Q-004 |

## 7. References

None given.
```

## Template

Everything below the line is copied into a new file; nothing above it is.

---


# Requirements Specification: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Author:** [Name]
**Status:** Draft

## 1. Summary

[What the input says the feature does and why, in 1 to 3 sentences.]

## 2. Scope

### In Scope

- [What the input includes]

### Out of Scope

- [What the input excludes]

**Systems:** [each system the requirements name, comma-separated]

## 3. Functional Requirements

FR-001: The <system> shall <response>. <!-- Source: [...] -->

FR-002: When <trigger>, the <system> shall <response>. <!-- Source: [...] -->

FR-003: While <precondition>, the <system> shall <response>. <!-- Source: [...] -->

FR-004: Where <feature is included>, the <system> shall <response>. <!-- Source: [...] -->

FR-005: If <unwanted event>, then the <system> shall <response>. <!-- Source: [...] -->

## 4. Non-Functional Requirements

NFR-001: The <system> shall <response> within <number> <unit> of <starting event> for <percentage> of <operations>. <!-- Source: [...] -->

NFR-002: The <system> shall comply with <named standard and level>. <!-- Source: [...] -->

NFR-003: The <system> shall <constraint the user confirmed>. <!-- Source: [...] -->

## 5. Open Questions

Q-001: <one direct question>? Proposed: <value>. <!-- Source: [...] -->

Q-002: Closed. <the question as asked>? Answer: <the user's answer> <!-- Source: [...] -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial draft |

## 7. References

- [Document, ticket, or standard the input names]
