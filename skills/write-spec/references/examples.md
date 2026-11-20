# Worked Examples

Every example follows [ears-rules.md](ears-rules.md) and the output format in the skill. Follow-up replies are in [follow-ups.md](follow-ups.md), and a saved file is in [saving.md](saving.md#an-example-file). Each worked example shows its input first, and every system, value, and name in its reply comes from that input or from the user's answers.

## One sentence per pattern

These sentences show the shapes only. Each assumes the input stated every system, value, and name in it.

```
FR-001: The checkout service shall record the completion time of every order in UTC.

FR-002: While the cart contains no items, the web storefront client shall disable the "Place order" button.

FR-003: When a user submits a password-reset request for a registered email address, the authentication service shall send a single-use reset link to that address.

FR-004: Where the gift-card module is installed, the web storefront client shall display a "Gift card code" field on the payment page.

FR-005: If five consecutive login requests for one account supply an incorrect password, then the authentication service shall lock that account for 15 minutes.

FR-006: While two-factor authentication is enabled for an account, when a login request for that account supplies the correct password, the authentication service shall request a one-time code.

FR-007: While an account is locked, if a login request for that account is received, then the authentication service shall reject the request and return the time at which the lock expires.

FR-008: Where the SSO module is installed, when a user opens the login page, the web storefront client shall display a "Sign in with SSO" button.

NFR-001: The search API shall return results within 300 ms of receiving a request for 95% of requests.
```

FR-001 to FR-005 follow the five patterns in table order. FR-006 to FR-008 are complex: `While` with `When`, `While` with `If ... then`, and `Where` with `When`. NFR-001 is a quality threshold, so it is non-functional and starts its own sequence.

FR-004 and FR-008 use `Where` because the gift-card and SSO modules are included or left out when the storefront is deployed. FR-006 uses `While` because a user can switch two-factor authentication on and off at runtime.

## An unwanted event written with When

Input: "When the user submits the order form and the payment is declined, the checkout service shows "Your card was declined" above the form."

A decline is an unwanted event, so `If ... then` replaces `When`. The submission is only context for the decline, so it folds into the `If` clause instead of becoming a second trigger.

```
FR-001: If the payment for a submitted order is declined, then the checkout service shall display "Your card was declined" above the order form.
```

## A runtime state and a schedule

Input: "The reporting service emails a usage report to each admin every Monday at 06:00 UTC, on Enterprise accounts only. If the email bounces, the reporting service logs the recipient address and the bounce code."

An account's plan can change at runtime, so it is a state (`While`), not a feature (`Where`). The schedule is a trigger, so it goes in the `When` clause, not in the response. The bounce is a separate, unwanted event, so it gets its own `If ... then` requirement. The bounce is also the evident failure case of the schedule, so there is no coverage-gap question.

```
FR-001: While an account is on the Enterprise plan, when the time reaches 06:00 UTC on a Monday, the reporting service shall email a usage report to each admin of that account.

FR-002: If a usage report email bounces, then the reporting service shall log the recipient address and the bounce code.
```

## A deadline on a behaviour

Input: "When an admin clicks "Export CSV" on the Reports page, the export service emails the report to that admin within 5 minutes of the click."

What the export service does is functional. How fast it does it is a service-level objective, so it is non-functional. The statement becomes two requirements, one in each sequence. The `NFR` keeps the trigger, because a tester needs it to measure the 5 minutes.

```
FR-001: When an admin clicks "Export CSV" on the Reports page, the export service shall email the report to that admin.

NFR-001: When an admin clicks "Export CSV" on the Reports page, the export service shall email the report to that admin within 5 minutes of the click.
```

## Some statements complete, some gaps

Input: "When a registered user requests a password reset, the authentication service emails a reset link to their registered address. The link expires 30 minutes after it is sent. Reset requests should be rate limited."

The first two statements have everything they need, so they are written. The third gives no limit, and the limit needs two separate decisions: what it counts per (Q-001) and how many requests it allows in what window (Q-002). FR-001 has an evident failure case the input does not cover, a request for an address that is not registered, so it gets Q-003.

Q-003 carries a proposal because sending no email is common security practice. The rate limit is a business decision, so Q-001 and Q-002 carry none.

```
FR-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address.

FR-002: If a user opens a reset link more than 30 minutes after the reset link was sent, then the authentication service shall reject the reset link.

Q-001: Is the password-reset rate limit counted per account or per IP address?

Q-002: How many password-reset requests does the rate limit allow, and in what time window?

Q-003: What does the authentication service do when a password-reset request names an email address that is not registered? Proposed: send no email.
```

## Nothing can be written yet

Input: "Users should be able to reset their password securely."

```
Q-001: Which service performs the password reset?

Q-002: What must the password reset do to count as secure, in terms a tester can check: a link expiry time, single use, an attempt limit, or something else?
```

Input: "The dashboard must load fast."

A time with the percentage of loads it holds for is one threshold, so one question. The span it is measured over is a separate gap.

```
Q-001: Which component loads the dashboard?

Q-002: What load-time threshold must the dashboard meet: a time with a unit, and the percentage of loads it applies to?

Q-003: From which event to which event is the dashboard load time measured?
```

Input: "The support chat service replies to customers at any hour."

The system is named, but "replies at any hour" gives no reply time, so a tester could never fail it. It is not testable, so it becomes a question.

```
Q-001: Within how many seconds of receiving a customer message must the support chat service reply?
```
