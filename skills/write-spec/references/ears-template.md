# Specification File Template

Use the template below the line for every new requirements file. Everything above the line is instructions and is never copied into the file. Sentence rules are in [ears-rules.md](ears-rules.md); a filled-in file is in [examples.md](examples.md#a-saved-file).

- Replace every `[...]` and `<...>`, and `YYYY-MM-DD` with today's date.
- Fill Summary, Scope, and References only with what the input states. Write `None given.` under any heading or subheading the input leaves empty.
- Write the Author only when the user gave a name; otherwise write `Not given.` Do not ask for it.
- The requirement lines in sections 3 and 4 show the pattern shapes. Replace them with the real requirements and keep no line the input does not support. When requirements the input states for a section wait on open questions, end the section with `Pending: Q-011, Q-020.`, naming those questions; update it as questions close and remove it when none are left. A section with no requirements and nothing pending holds `None given.`
- Put each requirement in section 3 or 4 as the rules' [Functional or non-functional](ears-rules.md#functional-or-non-functional) section says: `FR` lines in section 3, `NFR` lines in section 4.
- End each requirement and question line with `<!-- Source: <the input statement or answer it comes from> -->`. For a coverage-gap question, name the requirement: `<!-- Source: coverage gap in FR-001 -->`.
- Keep one requirement or question per line, with a blank line between lines. No priority, dependencies, user story, or titled subsections.
- The Systems line lists every system the requirements name, spelled as they spell it.
- Section 5 holds `None.` while there has never been a question. Closed questions stay in it, in the form [IDs](../SKILL.md#ids) gives.
- A new file is version 1.0. Each update raises the minor version by one (1.0, 1.1, 1.2) and adds one Revision History row that names the IDs added, changed, withdrawn, or closed.

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

Q-002: Closed. Answer: <the user's answer> <!-- Source: [...] -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial draft |

## 7. References

- [Document, ticket, or standard the input names]
