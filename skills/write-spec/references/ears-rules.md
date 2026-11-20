# EARS Rules

EARS (Easy Approach to Requirements Syntax, Mavin et al., Rolls-Royce) writes each requirement as one constrained sentence. These rules are the EARS ruleset plus stricter rules against ambiguity. Follow every rule without exception; a requirement is output only when it passes the [checklist](#checklist). The lint, [scripts/lint.py](../scripts/lint.py), catches the mechanical breaks: wording, clause order, banned words, open limits, missing time zones, and line format.

Wrong and Right pairs appear only where a rule is easy to get wrong. A Right uses only what its Wrong states, unless a note in parentheses says the input gave more. Their names and values are illustrations, not defaults. Full replies are in [examples.md](examples.md).

## Sentence structure

Every requirement is one sentence with its clauses in this order. Bracketed clauses are optional; never rearrange them:

`[Where <feature>,] [While <precondition>,] [When <trigger>, | If <trigger>, then] the <system> shall <response>.`

| Pattern | Keyword | Use when |
|---------|---------|----------|
| Ubiquitous | none | It holds at all times, with no feature, state, or trigger |
| State-driven | `While` | It applies for as long as a state holds |
| Event-driven | `When` | It responds to an expected event |
| Optional feature | `Where` | It applies only to products that include a feature |
| Unwanted behaviour | `If ... then` | It responds to an unwanted event |

A requirement may combine patterns in the clause order above. It has at most one `Where` clause and at most one `While` clause, either of which may join several conditions with `and`; at most one trigger, a `When` clause or an `If ... then` clause, never both; exactly one named system; and `shall` followed by one or more responses. A keyword is capitalised only when it starts the sentence: `While ..., when ..., the ...`.

Example: `While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust.`

## Choosing the keyword

Ask these in order for each condition in the input:

1. Is it a feature that a product, build, deployment, or licence either includes or does not, and that cannot change while the system runs? Use `Where`. Anything that can change at runtime (an account's plan, a user setting, a feature flag switched live) is a state: use `While`.
2. Is it true for a period of time (a mode, a status, a condition)? Use `While`.
3. Does it happen at an instant (a user action, a message arriving, a timer firing, a threshold being crossed)? It is a trigger. Use `When` for an expected event. Use `If ... then` for an unwanted one: a failure or fault, invalid input, misuse, an attack, or unexpected behaviour of another system, even when the input writes it with "when".
4. None of these? The requirement is Ubiquitous. Check that it truly holds in every state; if it does not, find the missing condition.

A precondition is something you can observe being true for a while. A trigger is something you could timestamp. An event that does not happen within a time limit ("no reply within 30 seconds") is a trigger at the instant the time runs out, not a state: `If ... then` when the missing event is unwanted (a reading, reply, or acknowledgement that should have arrived), `When` only when the timeout is expected. A schedule or interval ("every 6 hours", "every Monday at 06:00 UTC") is a trigger at the instant it fires: put it in a `When` clause, never in the response.

When a statement gives an expected event and an unwanted one, keep one trigger: fold the expected event into the `If` clause when it is only context (`If the payment for a submitted order is declined, ...`), or write two requirements when they describe two behaviours.

An `If ... then` requirement is an exception to the `When` requirement with the same trigger: it applies in place of the `When` requirement whenever its condition holds, so the pair is not a contradiction. Never repeat the opposite of that condition in the `When` requirement. Two expected behaviours that a condition chooses between are different: each states its own condition.

- **Wrong:** `When a user uploads a file of at most 25 MB, the upload service shall store the file.` beside `If a user uploads a file larger than 25 MB, then the upload service shall reject the upload.` (the exception's condition repeated)
- **Right:** `When a user uploads a file, the upload service shall store the file.` beside the same `If ... then` requirement.
- **Wrong:** `Where an account is on the Enterprise plan, ...` (a plan can change at runtime)
- **Right:** `While an account is on the Enterprise plan, ...`

## The system

- Name exactly one concrete system: the subsystem, service, component, client, or device that performs the response, for example `the checkout service`, `the engine control unit`, `the iOS push notification client`.
- These are not system names: `the system`, `the application`, `the app`, `the platform`, `the service`, `the software`, `the server`, `the backend`, `the frontend`, `it`.
- A system named for the whole input ("Requirements for the billing service: ...") or in a section heading applies to the statements under it that name no system. A statement whose subject is a not-a-name (`The system archives readings`) still needs a question: it may mean another system. Never take the system from a nearby statement or from context.
- Use the names on the target file's Systems line exactly. If a new name could be a listed system under another name, ask.
- Before asking which system a statement means, look in the project's README, the names of its top-level folders, and the Systems lines of the requirements files in `spec_output_dir`, and read nothing else for this. If they name exactly one system that could perform the response, add it to the question as `Proposed:`, in the project's words; otherwise ask without a proposal. Never write that name into a requirement before the user confirms it. Take only the name from the project: what the project already does (its requests, paths, fields, status codes, pages) is not input, so never write a requirement or ask a question because of it.

- **Wrong:** `The billing service shall send a receipt.` (from "The system sends a receipt", because the project's README describes a billing service)
- **Right:** no requirement yet. Ask: `Q-001: Which system sends the receipt? Proposed: the billing service.`

## The response

- Use `shall`, never another modal, in the active voice with the named system as its subject.
- State behaviour, not capability (`shall be able to`): the action, with a concrete verb for something observable from outside the system (`return`, `reject`, `log`, `display`, `send`, `store`, `disable`), and the condition that causes it.
- List several responses in one requirement only when they share the system and every condition and form one reaction (`reject the request and return HTTP status 401`); otherwise split them. Never join responses with `or`: alternatives hide the condition that picks one, so ask for it when the input does not give it. An `or` between conditions or triggers becomes one requirement per alternative.
- Use `shall not` only for a prohibition that can be tested (`The payment service shall not store full card numbers.`).
- `only` in the input (`shows the number only after access is granted`) makes a prohibition for every other case. Write the `shall not` for the other case. Write the positive behaviour as a separate requirement only when the input states it.
- Give every quantity a unit, and every time of day and every date or day boundary a time zone: `60 seconds`, `06:00 UTC`, `when the 1st day of a month begins in UTC`.
- Write every limit with an exact comparison: `more than`, `at least`, `at most`, `fewer than`. `up to`, `between X and Y`, and `within` with no starting point leave the boundary open: ask which side the boundary falls on unless the input says.

- **Wrong:** `While a homeowner has granted an installer access, the installer portal shall display the phone number of the homeowner to that installer.` (from "shows the number only after access is granted": the prohibition is lost)
- **Right:** `While a homeowner has not granted an installer access, the installer portal shall not display the phone number of the homeowner to that installer.`

## Testable

A requirement is testable when a tester could write a pass/fail check from the sentence alone: it gives the stimulus (state, feature, or trigger, or none for a Ubiquitous requirement), a response observable from outside the named system, and every value needed to judge the result (numbers with units, limits, names, message text, standards). If the input does not give one of these, ask.

A response that needs judgement to check is not observable: `an open-ended question`, `a friendly message`, `a relevant answer`. Ask for the exact text, or for a property a tester can check. A response stated as an absence (`without requiring a reply`, `independent of business hours`) is testable only when the sentence names the event to test with; otherwise ask what the system does in that event.

A quality requirement (performance, capacity, availability, accessibility) needs a measurable threshold with a unit, or a named standard such as WCAG 2.2 level AA. If the input gives only an impression ("must be fast", "must feel premium"), ask for a measurable proxy.

- **Wrong:** `When a user uploads a file, the storage service shall validate the file.` (validate against what?)
- **Right:** no requirement yet. Ask: `Q-001: What does the storage service check when it validates an uploaded file, and what does it do when a check fails?`

## Banned words

Words that hide an unanswered question are banned from requirement text: vague qualities (`fast`, `secure`, `user-friendly`), vague timing (`immediately`, `periodically`), vague amounts (`some`, `large`), optimisation words (`minimize`), hedges and escape clauses (`if possible`, `usually`), `and/or`, vague verbs (`handle`, `support`, `process`), open-ended lists (`etc.`, `such as`), pronouns (`it`, `they`), and placeholders (`TBD`). The lint flags each one and names the group it is listed under; the full list is in [banned-words.md](banned-words.md), which you need only when you cannot run the lint.

A word is banned only in the sense of its group: `about` as a vague amount ("approximately") is banned, but `a message about the order` is fine. Quoted text (UI labels, messages, identifiers), proper names the input gives, and questions are exempt. Replace each banned word, pronoun, or slash between alternatives (`email/SMS`) with what the input gives: a number with a unit, a complete list, a named actor, a concrete verb, or the noun it stands for; `this` and `that` are allowed only directly before a noun (`that address`). When the input gives no replacement, ask.

## Functional or non-functional

Classify each requirement before giving it an ID: `FR` for functional, `NFR` for non-functional.

- **Non-functional:** a measurable threshold on how fast or how well a system performs a response (a deadline, a latency with the percentage of cases it holds for, throughput, capacity, availability, an accessibility level), or a constraint the user confirmed (a mandated technology, platform, standard, or regulation).
- **Functional:** everything else, including security behaviour such as rejecting, locking, or logging.

A statement that gives both a behaviour and a threshold on that behaviour becomes two requirements: an `FR` for the behaviour, with no threshold, and an `NFR` for the threshold. The `NFR` keeps the conditions a tester needs, so the pair is not a duplicate. A deadline given with no percentage of cases holds for every case: write it as given, and ask for no percentage. A threshold in a condition, such as a timeout that triggers the response, is part of the stimulus and stays functional.

A technology, product, or vendor in the input ("store sessions in Redis") is an implementation choice until the user confirms it is a constraint. Ask first; write it, as an `NFR`, only after the user confirms.

- **Wrong:** `The session service shall store sessions in Redis.` (from "Store sessions in Redis", not yet confirmed)
- **Right:** no requirement yet. Ask: `Q-001: Is storing sessions in Redis a constraint the session service must meet?`

## Rewrite, or ask

Fix a requirement yourself whenever a rule above says how and the fix needs no new fact: split it, reorder its clauses, change its keyword or modal, make the system the subject, move a timeout or schedule into the trigger, repeat the noun a pronoun stands for, or use a replacement for a banned word that the input states elsewhere.

Leave out, without asking, a statement that requires no behaviour or property: background, rationale, a user story's "so that" clause, project dates. A stated purpose or scope still goes in the file's Summary or Scope.

Ask whenever the fix needs a fact the input does not give, which includes every case a rule above says to ask about, and also when a pronoun or term could mean two things that would be tested differently, or when two statements in the input, or a statement and an existing requirement, contradict each other. Never invent a system, value, name, or behaviour that the input, the user's answers, or the target file did not give, even a plausible one.

## Coverage gaps

A set of requirements can pass every rule above and still leave a case undecided. A coverage gap is a case that the requirements themselves make possible and that no requirement, no answer, and no statement in the input decides. Check every requirement of the set in every reply: those the reply writes, those written earlier in the conversation, and those in the target file. An answer can open a gap in an earlier requirement, and a gap missed in an earlier reply is still a gap.

For each requirement, look at:

- **The trigger failing:** its input is missing or not valid, it times out, or a system or device it depends on fails.
- **The other side of a condition:** the requirement applies only under a condition, which may be a `While` state, a limit, or a qualifier on the actor or the thing it acts on. What does the same trigger do when the condition does not hold?
- **A refusal:** the response is a `shall not` that withholds what a requester asked for. What does the requester receive instead?

Ask one question for each gap, unless another requirement decides the case or a question about it is open or closed. Never write the requirement for a gap yourself. Take gaps only from the words of the requirements and the input: a case that needs an actor, a thing, or a state that none of them mentions is not a gap.

## Checklist

Check each requirement against every section above: [Sentence structure](#sentence-structure), [Choosing the keyword](#choosing-the-keyword), [The system](#the-system), [The response](#the-response), [Testable](#testable), [Banned words](#banned-words), and [Functional or non-functional](#functional-or-non-functional), whose class sets the ID prefix. It holds nothing the input, the answers, or the target file did not give. Fix what [Rewrite, or ask](#rewrite-or-ask) lets you fix; a requirement that still fails is never output: ask about its gap instead.

Then check the whole set:

- One term for one thing, keeping the input's own terms and the target file's.
- No duplicates, and no contradictions within the set or with an existing requirement.
- IDs that follow the skill's ID rules.
- A question for every statement that could not be written, and for every [coverage gap](#coverage-gaps).
