# EARS Output Formats and Examples

The rules are in [ears-rules.md](ears-rules.md). Every example here follows them.

## Response format

Requirements first, then open questions. Omit a part that is empty. Nothing else: no preamble, no summary, and no prose between requirements unless the user asks for rationale.

```
REQ-001: <requirement>

REQ-002: <requirement>

## Open questions

1. <question> (blocks: "<input statement>")
2. <question> (blocks: "<input statement>")
```

- One requirement per paragraph, with a blank line between requirements so each renders on its own.
- One question per gap. If one gap blocks several statements, ask it once and quote each statement it blocks.
- Add `(blocks: "<input statement>")` only when the input has more than one statement. Shorten a long statement with `...`.
- A question may offer the options the input suggests, ending with "or something else?".

## File format

The same content as the response, under a title:

```
# <Feature name> requirements

REQ-001: <requirement>

REQ-002: <requirement>

## Open questions

1. <question> (blocks: "<input statement>")
```

## One example per pattern

```
REQ-001: The checkout service shall record the completion time of every order in UTC.

REQ-002: While the cart contains no items, the web storefront client shall disable the "Place order" button.

REQ-003: When a user submits a password-reset request for a registered email address, the authentication service shall send a single-use reset link to that address within 60 seconds.

REQ-004: Where the gift-card module is installed, the web storefront client shall display a "Gift card code" field on the payment page.

REQ-005: If five consecutive login requests for one account supply an incorrect password, then the authentication service shall lock that account for 15 minutes.

REQ-006: While two-factor authentication is enabled for an account, when a login request for that account supplies the correct password, the authentication service shall request a one-time code.

REQ-007: While an account is locked, if a login request for that account is received, then the authentication service shall reject the request and return the time at which the lock expires.

REQ-008: Where the SSO module is installed, when a user opens the login page, the web storefront client shall display a "Sign in with SSO" button.
```

REQ-001 to REQ-005 follow the five patterns in table order. REQ-006 to REQ-008 are complex: `While` with `When`, `While` with `If ... then`, and `Where` with `When`.

REQ-004 and REQ-008 use `Where` because the gift-card and SSO modules are included or left out when the storefront is deployed. REQ-006 uses `While` because a user can switch two-factor authentication on and off at runtime.

## Worked examples

### An unwanted event written with When

Input: "When the user submits the order form and the payment is declined, the checkout service shows "Your card was declined" above the form."

A decline is an unwanted event, so `If ... then` replaces `When`. The submission is only context for the decline, so it folds into the `If` clause instead of becoming a second trigger.

```
REQ-001: If the payment for a submitted order is declined, then the checkout service shall display "Your card was declined" above the order form.
```

### A runtime state and a schedule

Input: "The reporting service emails a usage report to each admin every Monday at 06:00 UTC, on Enterprise accounts only. If the email bounces, the reporting service logs the recipient address and the bounce code."

An account's plan can change at runtime, so it is a state (`While`), not a feature (`Where`). The schedule is a trigger, so it goes in the `When` clause, not in the response. The bounce is a separate, unwanted event, so it gets its own `If ... then` requirement.

```
REQ-001: While an account is on the Enterprise plan, when the time reaches 06:00 UTC on a Monday, the reporting service shall email a usage report to each admin of that account.

REQ-002: If a usage report email bounces, then the reporting service shall log the recipient address and the bounce code.
```

### Some statements complete, one with a gap

Input: "When a registered user requests a password reset, the authentication service emails a reset link to their registered address. The link expires 30 minutes after it is sent. Reset requests should be rate limited."

The first two statements have everything they need, so they are written. The third gives no limit, so it becomes a question.

```
REQ-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address.

REQ-002: If a user opens a reset link more than 30 minutes after the reset link was sent, then the authentication service shall reject the reset link.

## Open questions

1. What is the rate limit for password-reset requests: how many requests, counted per account or per IP address, in what time window? (blocks: "Reset requests should be rate limited.")
```

### Nothing can be written yet

Input: "Users should be able to reset their password securely."

```
## Open questions

1. Which service performs the password reset?
2. What does "securely" require, in observable terms: a link expiry time, single use, an attempt limit, or something else?
```

Input: "The dashboard must load fast."

```
## Open questions

1. Which component loads the dashboard?
2. What is the maximum load time, at which percentile, and under what load?
```

Input: "The billing service should handle failed payments gracefully."

```
## Open questions

1. What does the billing service do when a payment fails: retry (how many times, at what interval), suspend the account, notify the customer, or something else?
```
