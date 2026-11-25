# Drafts

Read this in every reply, once the lint is clean on the reply's requirements and questions. It adds `Draft:` lines below the questions and changes nothing above them.

A draft shows the user what an answer will unblock. It is a statement of the input that waits on questions in this reply, written as the EARS sentence it will become, with `[Q-NNN]`, the question that fills it, in place of each missing part.

## Rules

- Write a draft for each statement that says what the system does and under which conditions, and whose own words lack only a system name or a value that questions in this reply ask for. Other open questions about the statement, such as a coverage gap or a case beside it, do not stop its draft.
- Change no requirement and no question, and add, split, reorder, or drop none. One question can fill slots in several drafts. When no question in the reply asks for a missing part, write no draft for that statement.
- A draft follows every rule a requirement follows and holds only the input's words and its slots. A slot stands for all that is missing and follows the input's own words directly: add no word around it that the input does not give, not even a word its question uses. Several slots can stand side by side.
- Write none for a coverage gap, for a statement that gives only an impression (`fast`, `secure`, `quick`), or for one that does not say what the system does. When no statement qualifies, the reply stays as it is.
- A draft is not a requirement: it takes no ID and is never saved.
- Draft lines come last, below the question lines and the `<N> more open questions after these.` line, with a blank line between lines.

- **Wrong:** `If a backup fails, then the [Q-001] shall post an alert in the [Q-002] channel and retry the backup [Q-003] times at intervals of [Q-004].` (from "Admins are alerted when a backup fails, and the backup is retried": the input gives no post, no channel, no count, and no interval)
- **Right:** `If a backup fails, then the [Q-001] shall alert the admins [Q-002] and retry the backup [Q-003] [Q-004].`

Then run the lint on the whole reply once more and fix every `ERROR`, changing only the draft lines. Return the reply as the skill's Output section says, also when no draft was added: its first line is an `FR-`, `NFR-`, or `Q-` line, and it holds no word about drafts, this file, or the lint.

## Example

Input: "When a payment succeeds, the system emails a receipt to the payer. Each account admin gets a usage summary by email at 09:00 on the 1st day of each month. Late payers should be chased."

The linted reply holds four questions and no requirement. The first two statements say what happens, and their own words lack only what Q-001 and Q-002 ask, so each becomes a draft; Q-003, a coverage gap of the first, does not stop it. The third statement does not say what any system does, so it gets none.

```
Q-001: Which system emails the receipt and the usage summary?

Q-002: In which time zone is 09:00 on the 1st day of a month measured?

Q-003: What happens when the receipt email cannot be delivered?

Q-004: What does chasing a late payer consist of, in terms a tester can check?

Draft: When a payment succeeds, the [Q-001] shall email a receipt to the payer.

Draft: When the time reaches 09:00 [Q-002] on the 1st day of a month, the [Q-001] shall email a usage summary to each account admin.
```
