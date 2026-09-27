# EARS Rules

EARS (Easy Approach to Requirements Syntax, Mavin et al., Rolls-Royce) writes each requirement as one constrained sentence. These rules are the EARS ruleset plus stricter rules against ambiguity. Follow every rule without exception. The [validation checklist](#validation-checklist) at the end sums them up. Every requirement must pass it before it is output.

Most rule sections end with **Wrong** and **Right** pairs that show that one rule. A Right uses only what its Wrong states, unless a note in parentheses says the input gave more; without that input, ask instead. The system names and values in the pairs are illustrations, not defaults to reuse. Full replies are in [examples.md](examples.md).

## Sentence structure

Every requirement is one sentence with its clauses in this order. Bracketed clauses are optional; never rearrange them:

`[Where <feature>,] [While <precondition>,] [When <trigger>, | If <trigger>, then] the <system> shall <response>.`

Each requirement has:

- At most one `Where` clause and at most one `While` clause. Either may join several conditions with `and`.
- At most one trigger: a `When` clause **or** an `If ... then` clause, never both. Both keywords introduce a trigger, and an EARS requirement has zero or one trigger.
- Exactly one named system (see [The system](#the-system)).
- `shall` followed by one or more responses (see [The response](#the-response)).

A keyword is capitalised only when it starts the sentence. After a comma it is lowercase: `While ..., when ..., the ...`.

Reference example:
`While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust.`
Here `the aircraft is on ground` is the precondition, `reverse thrust is commanded` is the trigger, `the engine control system` is the system, and `enable reverse thrust` is the response.

- **Wrong:** `The authentication service shall lock the account when five consecutive logins fail.` (trigger after the response)
- **Right:** `If five consecutive login attempts for one account fail, then the authentication service shall lock that account.`
- **Wrong:** `When a user submits a payment, if the card is declined, then the checkout service shall ...` (two triggers)
- **Right:** `If the payment for a submitted order is declined, then the checkout service shall ...`

## The five patterns

| # | Pattern | Keyword | Use when | Template |
|---|---------|---------|----------|----------|
| 1 | Ubiquitous | none | It holds at all times, with no feature, state, or trigger | `The <system> shall <response>.` |
| 2 | State-driven | `While` | It applies for as long as a state holds | `While <precondition>, the <system> shall <response>.` |
| 3 | Event-driven | `When` | It responds to an expected event | `When <trigger>, the <system> shall <response>.` |
| 4 | Optional feature | `Where` | It applies only to products that include a feature | `Where <feature is included>, the <system> shall <response>.` |
| 5 | Unwanted behaviour | `If ... then` | It responds to an unwanted event | `If <trigger>, then the <system> shall <response>.` |

A requirement with more than one keyword is a complex requirement. It combines the patterns in the clause order above, for example `Where ..., when ...,` or `While ..., if ..., then`.

## Choosing the keyword

Ask these in order for each condition in the input:

1. Is it a feature that a product, build, deployment, or licence either includes or does not, and that cannot change while the system runs? Use `Where`. Anything that can change at runtime (an account's plan, a user setting, a feature flag switched live) is a state: use `While`.
2. Is it true for a period of time (a mode, a status, a condition)? Use `While`.
3. Does it happen at an instant (a user action, a message arriving, a timer firing, a threshold being crossed)? It is a trigger. Use `When` for an expected event. Use `If ... then` for an unwanted one: a failure or fault, invalid input, misuse, an attack, or unexpected behaviour of another system.
4. None of these? The requirement is Ubiquitous. Check that it truly holds in every state; if it does not, find the missing condition.

A precondition is something you can observe being true for a while. A trigger is something you could timestamp.

An event that does not happen within a time limit ("no reply within 30 seconds") is a trigger at the instant the time runs out, not a state. Use `When` if the timeout is expected, `If ... then` if it is unwanted.

A schedule or interval ("every 6 hours", "every Monday at 06:00 UTC") is a trigger at the instant it fires. Put it in a `When` clause, never in the response.

- **Wrong:** `The backup service shall copy the database every 6 hours.` (a schedule in the response)
- **Right:** `When 6 hours have passed since the previous database copy, the backup service shall copy the database.`
- **Wrong:** `Where an account is on the Enterprise plan, ...` (a plan can change at runtime)
- **Right:** `While an account is on the Enterprise plan, ...`
- **Wrong:** `When the payment gateway is down, the checkout service shall cancel the charge request.` (unwanted, and a state rather than an event)
- **Right:** `If the payment gateway returns no response within 10 seconds of a charge request, then the checkout service shall cancel the charge request.` (only when the input says how "down" is detected, here as 10 seconds without a response)

## The system

- Name exactly one concrete system: the subsystem, service, component, client, or device that performs the response, for example `the checkout service`, `the engine control unit`, `the iOS push notification client`.
- These are not system names: `the system`, `the application`, `the app`, `the platform`, `the service`, `the software`, `the server`, `the backend`, `the frontend`, `it`.
- A system named once for the whole input (for example "Requirements for the billing service: ...") applies to every requirement in that input. A section heading that names a system applies the same way to the statements under it that name no system.
- A statement whose subject is a name from the not-a-name list (`The system archives readings`) needs a question, even under such a heading: it may mean another system. Never take the system from a nearby statement or from context.
- Use the system names already in the target file's Scope (Systems line) exactly. If a new name could be a system already listed under another name, ask.

- **Wrong:** `The system shall send a receipt.`
- **Right:** `The billing service shall send a receipt.` (only when the input names the billing service)

## The response

- Use `shall`. Never `should`, `may`, `might`, `will`, `can`, `must`, `needs to`, `has to`, `is required to`.
- Write in the active voice, with the named system as the subject of `shall`: `the web client shall display the message`, not `the message shall be displayed`.
- State behaviour, not capability. Not `shall be able to export`, `shall have the ability to`, or `shall be capable of`: write the action and the condition that causes it.
- Use a concrete verb for something observable from outside the system and testable: `return`, `reject`, `log`, `display`, `send`, `store`, `disable`, `enable`, `compute`, `transmit`.
- List several responses in one requirement only when they share the system and every condition and together form one reaction, for example `reject the request and return HTTP status 401`. Otherwise split them.
- No `or` between responses. A response with alternatives hides the condition that picks one of them.
- Use `shall not` only for a prohibition that can be tested, for example `The payment service shall not store full card numbers.`
- `only` in the input (`shows the number only after access is granted`) makes a prohibition for every other case. Write the `shall not` for the other case. Write the positive behaviour as a separate requirement only when the input states it.
- Give every quantity a unit, and every time of day and every date or day boundary a time zone: `60 seconds`, `06:00 UTC`, `when the 1st day of a month begins in UTC`. The instant a day starts differs by time zone, so a tester needs it.
- Write every limit with an exact comparison: `more than`, `at least`, `at most`, `fewer than`. `up to`, `between X and Y`, and `within` with no stated starting point leave the boundary open.

- **Wrong:** `When a user saves a draft, the draft shall be stored.` (passive)
- **Right:** `When a user saves a draft, the document service shall store the draft.` (only when the input names the document service)
- **Wrong:** `The reporting service shall be able to export reports as CSV.` (capability)
- **Right:** `When an admin selects "Export CSV", the reporting service shall send the report as a CSV file.` (only when the input names that trigger)
- **Wrong:** `If a login fails, then the authentication service shall display an error or lock the account.` (`or` between responses)
- **Right:** two requirements, each with the condition that selects its response.
- **Wrong:** `While a homeowner has granted an installer access, the installer portal shall display the phone number of the homeowner to that installer.` (from "shows the number only after access is granted": the prohibition is lost)
- **Right:** `While a homeowner has not granted an installer access, the installer portal shall not display the phone number of the homeowner to that installer.`
- **Wrong:** `The upload service shall accept files between 1 KB and 25 MB.` (are 1 KB and 25 MB accepted?)
- **Right:** `If an uploaded file is smaller than 1 KB, then the upload service shall reject the upload.` and `If an uploaded file is larger than 25 MB, then the upload service shall reject the upload.` (only when the input says that files of exactly 1 KB and 25 MB are accepted)

## Testable

A requirement is testable when a tester could write a pass/fail check from the sentence alone, without asking anyone. The sentence must give:

- the stimulus: the state, feature, or trigger that sets up the test, or none for a Ubiquitous requirement;
- a response that can be observed from outside the named system;
- every value needed to judge the result: numbers with units, limits, names, message text, standards.

If any of these is missing and the input does not give it, ask.

A response that needs judgement to check is not observable: `an open-ended question`, `a friendly message`, `a relevant answer`. Ask for the exact text, or for a property a tester can check. A response stated as an absence (`without requiring a reply`, `independent of business hours`) is testable only when the sentence names the event to test with; otherwise ask what the system does in that event.

- **Wrong:** `When a user uploads a file, the storage service shall validate the file.` (validate against what?)
- **Right:** no requirement yet. Ask: `Q-001: What does the storage service check when it validates an uploaded file, and what does it do when a check fails?`

## Terms

Use one term for one thing across all requirements. Keep the input's own terms.

## Banned words

Each banned word hides an unanswered question. The ban applies to the sense shown. The same word is allowed in another sense, inside quoted text (UI labels, messages, identifiers), or inside a proper name the input gives: `about` meaning "approximately" is banned but `a message about the order` is fine; `support` as a verb is banned but `the Customer Support page` is fine. The ban applies to requirement text, not to questions.

- Vague qualities: `gracefully`, `appropriately`, `properly`, `correctly`, `sufficient`, `adequate`, `reasonable`, `acceptable`, `significant`, `robust`, `reliable`, `scalable`, `flexible`, `efficient`, `fast`, `slow`, `secure`, `user-friendly`, `easy`, `simple`, `intuitive`, `seamless`, `smooth`, `modern`, `clean`
- Vague timing: `immediately`, `instantly`, `promptly`, `quickly`, `soon`, `as soon as possible`, `ASAP`, `real-time`, `in real time`, `timely`, `periodically`, `regularly`
- Vague amounts: `some`, `several`, `many`, `few`, `most`, `a number of`, `a lot of`, `approximately`, `about`, `around`, `roughly`, `nearly`, `large`, `small`, `high`, `low`
- Optimisation words: `minimize`, `maximize`, `optimize`, `as much as possible`, `as few as possible`
- Hedges and escape clauses: `if possible`, `where possible`, `as appropriate`, `as applicable`, `where applicable`, `if necessary`, `as needed`, `as required`, `if practical`, `unless otherwise specified`, `to the extent possible`
- Frequency hedges: `usually`, `normally`, `typically`, `generally`, `often`, `sometimes`, `mostly`, `almost always`
- Ambiguous logic: `and/or`
- Vague verbs: `handle`, `support`, `manage`, `process`, `deal with`, `facilitate`, `take care of`
- Open-ended lists: `etc.`, `and so on`, `and more`, `such as`, `e.g.`, `for example`, `including but not limited to`
- Pronouns: `it`, `its`, `they`, `them`, `their`
- Placeholders: `TBD`, `TBC`, `TBA`, `to be defined`, `to be determined`, `XX`, `?`, `...`

Replace each banned word with a concrete value or verb that the input gives: a number with a unit, a complete list, a named actor, or a concrete verb from [The response](#the-response). Replace a pronoun, or a slash between alternatives (`email/SMS`), with what it stands for. `this` and `that` are allowed only directly before a noun: `that address`.

- **Wrong:** `When a user submits a search, the search API shall return results quickly.`
- **Right:** `When a user submits a search, the search API shall return results within 300 ms of the submission.` (only when the input gives 300 ms)

## Quality requirements

Performance, capacity, availability, accessibility, and other quality requirements follow the same rules. They are usually Ubiquitous, or State-driven when they apply only in one state: `The search API shall return results within 300 ms of receiving a request for 95% of requests.` They need a measurable threshold with a unit, or a named standard such as WCAG 2.2 level AA. If the input gives only an impression ("must be fast", "must feel premium", "must be enterprise-grade"), ask for a measurable proxy.

- **Wrong:** `The search API shall be fast.`
- **Right:** `The search API shall return results within 300 ms of receiving a request for 95% of requests.` (only when the input gives 300 ms and 95%)

## Functional or non-functional

Classify each requirement for the specification file:

- **Non-functional:** its response sets a measurable threshold on how well a system performs (time, throughput, capacity, availability, accessibility level), or it is a constraint the user confirmed (a mandated technology, platform, standard, or regulation).
- **Functional:** everything else, including security behaviour such as rejecting, locking, or logging.

A technology, product, or vendor in the input ("store sessions in Redis") is an implementation choice until the user confirms it is a constraint. Ask first; write it only after the user confirms.

- **Wrong:** `The session service shall store sessions in Redis.` (from "Store sessions in Redis", not yet confirmed)
- **Right:** no requirement yet. Ask: `Q-001: Is storing sessions in Redis a constraint the session service must meet?`

## Rewrite, or ask

Fix these yourself; they do not need the user:

- Several requirements in one sentence: split them.
- Clauses out of order: reorder them.
- A modal verb other than `shall`: change it to `shall`.
- A passive response: make the named system the subject.
- An unwanted event written with `When`: use `If ... then`.
- A timeout written as a state: make it a trigger at the instant the time runs out.
- A schedule or interval in the response: move it into a `When` clause.
- Both `When` and `If` in one sentence: keep one trigger. If the expected event is only context for the unwanted one, fold it into the `If` clause (`If the payment for a submitted order is declined, ...`). If they describe two behaviours, write two requirements.
- `Where` used for something that can change at runtime: use `While`.
- `or` between conditions or triggers: write one requirement per alternative.
- A pronoun whose noun is clear: repeat the noun.
- A banned word whose concrete replacement the input states elsewhere: use that replacement.
- A statement that requires no behaviour or property (background, rationale, a user story's "so that" clause, project dates): leave it out of the requirements and do not ask about it. A stated purpose or scope still goes in the file's Summary or Scope.

Ask when:

- No system is named, or only a name from the not-a-name list above, and no heading or whole-input system covers the statement. A not-a-name as the subject always needs a question.
- A new system name could be a system already in the target file under another name.
- The response is not observable, or depends on a banned word that the input gives no replacement for.
- The requirement is not [testable](#testable).
- A value the requirement needs is missing: a number, limit, threshold, unit, time zone, name, list item, or message text.
- A limit's boundary is open: `up to`, `between X and Y`, or `within` with no starting point.
- A response offers alternatives joined by `or`: ask which condition selects each.
- The input states an implementation choice ("store sessions in Redis"): ask whether it is a constraint the system must meet. If it is, write it as a non-functional requirement.
- A quality requirement has no measurable threshold.
- A pronoun or term could mean two things that would be tested differently.
- Two statements in the input, or a statement and an existing requirement, contradict each other.

Never invent a system, value, name, or behaviour that the input does not give, even a plausible one. Ask one direct question per gap: no padding, no hedging, no apologies.

## Validation checklist

Check every requirement against every item. If an item fails, fix it when [Rewrite, or ask](#rewrite-or-ask) says to rewrite. Otherwise leave the requirement out and ask a question. A requirement that fails any item is never output.

Each requirement:

1. Is one sentence, with its clauses in the fixed order.
2. Has at most one `Where`, at most one `While`, and at most one trigger (`When` or `If ... then`).
3. Uses the keyword that [Choosing the keyword](#choosing-the-keyword) gives for each condition.
4. Names exactly one concrete system, not one on the not-a-name list, and matching the target file's name for that system.
5. Uses `shall` once, in the active voice, with the named system as the subject.
6. States behaviour with an observable verb, not a capability, with no `or` between responses.
7. Gives every quantity a unit, every time of day and date boundary a time zone, and every limit an exact comparison.
8. Contains no banned word in its banned sense and no placeholder.
9. Is [testable](#testable) from the sentence alone.
10. Keeps every `only` in the input as a `shall not` for the other case.
11. Names no technology, product, or vendor unless the user confirmed it as a constraint.
12. Contains no system, value, name, or behaviour that the input, the user's answers, or the target file did not give.

The whole set:

- Uses one term for one thing, matching the input and the target file.
- Has no duplicates, and no two requirements, or a requirement and an existing one, that contradict each other.
- Uses IDs that are unique and continue from the highest existing ID.
- Has a question for every statement that could not be written.
