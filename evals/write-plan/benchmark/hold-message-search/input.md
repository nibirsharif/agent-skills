Plan the implementation of the message-search feature. There is no codebase in this folder, and the requirements file is not on disk; this is docs/specs/message-search/requirements.md:

```markdown
# Requirements Specification: Message Search

**Version:** 1.0
**Date:** 2026-03-03
**Author:** Not given.
**Status:** Draft

## 1. Summary

Users search their chat messages by word.

## 2. Scope

### In Scope

- Searching messages and showing the results

### Out of Scope

None given.

**Systems:** chat app, chat service

## 3. Functional Requirements

FR-001: When a user enters a search word, the chat app shall display the messages of the user that contain the search word, newest first. <!-- Source: "search my messages" -->

FR-002: When a user selects a search result, the chat app shall open the conversation at the selected message. <!-- Source: "jump to the message" -->

FR-003: If no message contains the search word, then the chat app shall display `No messages found`. <!-- Source: "say when nothing matches" -->

Pending: Q-001.

## 4. Non-Functional Requirements

NFR-001: When a user enters a search word, the chat app shall display the search results within 1 second of the entry for 95% of searches. <!-- Source: "search is quick" -->

## 5. Open Questions

Q-001: Does the search run on the device, over the messages stored on the device, or in the chat service, over every message of the user? <!-- Source: "search my messages" -->

## 6. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | Not given. | Initial draft |

## 7. References

None given.
```
