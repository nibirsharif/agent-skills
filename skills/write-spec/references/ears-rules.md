# EARS Rules

EARS (Easy Approach to Requirements Syntax, Mavin et al., Rolls-Royce) writes each requirement as one constrained sentence. These rules are the EARS ruleset plus stricter rules against ambiguity. Follow every rule without exception.

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

## The system

- Name exactly one concrete system: the subsystem, service, component, client, or device that performs the response, for example `the checkout service`, `the engine control unit`, `the iOS push notification client`.
- These are not system names: `the system`, `the application`, `the app`, `the platform`, `the service`, `the software`, `the server`, `the backend`, `the frontend`, `it`.
- A system named once for the whole input (for example "Requirements for the billing service: ...") applies to every requirement in that input.

## The response

- Use `shall`. Never `should`, `may`, `might`, `will`, `can`, `must`, `needs to`, `has to`, `is required to`.
- Write in the active voice, with the named system as the subject of `shall`: `the web client shall display the message`, not `the message shall be displayed`.
- State behaviour, not capability. Not `shall be able to export`, `shall have the ability to`, or `shall be capable of`: write the action and the condition that causes it.
- Use a concrete verb for something observable from outside the system and testable: `return`, `reject`, `log`, `display`, `send`, `store`, `disable`, `enable`, `compute`, `transmit`.
- List several responses in one requirement only when they share the system and every condition and together form one reaction, for example `reject the request and return HTTP status 401`. Otherwise split them.
- Use `shall not` only for a prohibition that can be tested, for example `The payment service shall not store full card numbers.`
- Give every quantity a unit and every time of day a time zone: `60 seconds`, `06:00 UTC`.

## Terms

Use one term for one thing across all requirements. Keep the input's own terms.

## Banned words

Each banned word hides an unanswered question. The ban applies to the sense shown. The same word is allowed in another sense, inside quoted text (UI labels, messages, identifiers), or inside a proper name the input gives: `about` meaning "approximately" is banned but `a message about the order` is fine; `support` as a verb is banned but `the Customer Support page` is fine.

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

## Quality requirements

Performance, capacity, availability, accessibility, and other quality requirements follow the same rules. They are usually Ubiquitous, or State-driven when they apply only in one state: `The search API shall return results within 300 ms for 95% of requests.` They need a measurable threshold with a unit, or a named standard such as WCAG 2.2 level AA. If the input gives only an impression ("must be fast", "must feel premium", "must be enterprise-grade"), ask for a measurable proxy.

## Rewrite, or ask

Fix these yourself; they do not need the user:

- Several requirements in one sentence: split them.
- Clauses out of order: reorder them.
- A modal verb other than `shall`: change it to `shall`.
- A passive response: make the named system the subject.
- An unwanted event written with `When`: use `If ... then`.
- Both `When` and `If` in one sentence: keep one trigger. If the expected event is only context for the unwanted one, fold it into the `If` clause (`If the payment for a submitted order is declined, ...`). If they describe two behaviours, write two requirements.
- `Where` used for something that can change at runtime: use `While`.
- `or` between conditions or triggers: write one requirement per alternative.
- A pronoun whose noun is clear: repeat the noun.
- A banned word whose concrete replacement the input states elsewhere: use that replacement.
- A statement that requires no behaviour or property (background, rationale, a user story's "so that" clause, project dates): leave it out and do not ask about it.

Ask when:

- No system is named, or only a name from the not-a-name list above.
- The response is not observable, or depends on a banned word that the input gives no replacement for.
- A value the requirement needs is missing: a number, limit, threshold, unit, time zone, name, list item, or message text.
- A quality requirement has no measurable threshold.
- A pronoun or term could mean two things that would be tested differently.
- Two statements in the input, or a statement and an existing requirement, contradict each other.

Never invent a system, value, name, or behaviour that the input does not give, even a plausible one. Ask one direct question per gap: no padding, no hedging, no apologies.
