# Follow-up Replies

Read this when the user answers questions or adds input after an earlier reply in the conversation, and when a conversation's first input changes or withdraws a requirement, or answers a question, that the target file already holds. Everything in the skill's Output section still applies.

## What the reply holds

- The requirements the answers or new input change, marked `(changed)` after the ID.
- The requirements they unblock or add, marked `(new)`. A requirement written for the first time is `(new)`, also when every earlier reply held only questions.
- The next open questions, at most 10.
- The drafts step 7 of the workflow adds, for the statements that still wait on a question. A draft whose slots are all answered is written as a requirement, marked `(new)`.

A requirement that did not change is not returned. Every requirement line carries one of the two markers; the lint's `--follow-up` option fails a line without one. The first reply of a conversation is the exception, also when it changes the target file: it carries no markers and is linted without `--follow-up`, so a withdrawn line there is `<ID>: Withdrawn.`

The user can answer by ID, or accept proposals with `accept Q-001, Q-004` or `accept all proposed`. An accepted proposal is the user's answer.

## Existing IDs

- An answered question closes and drops out of the open questions. It never becomes a requirement ID: the requirement it unblocks takes the next free `FR` or `NFR` ID. A question still unanswered keeps its ID.
- A requirement's prefix is fixed when it is first written. When an answer or new input changes a requirement but not its class, rewrite it under its existing ID.
- When an answer shows that a requirement belongs to the other class, its line becomes `<ID> (changed): Withdrawn. Moved to <new ID>.`, and the requirement is written under the next free ID of the other sequence, marked `(new)`.
- When the user withdraws or deletes a requirement, its line becomes `<ID> (changed): Withdrawn.`, so its ID is never reused.

## Example

The first reply, to "When a registered user requests a password reset, the authentication service emails a reset link to their registered address. The link expires 30 minutes after it is sent. Reset requests should be rate limited.", is in [examples.md](examples.md#some-statements-complete-some-gaps). The user answers: "Q-001: per account. Q-002: at most 5 in any rolling 60 minutes. Q-003: yes. Also, make the link expire after 15 minutes, and the reset email must go out within 2 minutes of the request for 99% of requests."

The answers unblock two requirements, and the new input changes FR-002. The email deadline is a threshold on FR-001's response, so it is a new non-functional requirement: NFR-001, the first in its own sequence, while FR-001 stays as it is. FR-004 withholds the email the user asked for, so the [coverage-gap](ears-rules.md#coverage-gaps) check asks what the user gets instead.

```
FR-002 (changed): If a user opens a reset link more than 15 minutes after the reset link was sent, then the authentication service shall reject the reset link.

FR-003 (new): If a password-reset request is received for an account that already had at least 5 password-reset requests in the preceding 60 minutes, then the authentication service shall reject the request.

FR-004 (new): If a password-reset request names an email address that is not registered, then the authentication service shall not send an email.

NFR-001 (new): When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address within 2 minutes of receiving the request for 99% of requests.

Q-004: What does the authentication service display to a user whose password-reset request names an email address that is not registered?
```
