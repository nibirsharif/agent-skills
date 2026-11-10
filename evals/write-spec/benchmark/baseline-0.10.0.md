# Baseline: write-spec 0.10.0

One run per input on Claude Sonnet 5.5, 2026-11-09, first reply only. Scored by hand against each `reference.md` as the [README](README.md) says. The reference lists were drafts when this was scored.

| Input | Requirements written | Gaps found | Needed questions | Invented values |
|-------|----------------------|------------|------------------|-----------------|
| dev-invoice-export | 0 | 6 of 7 | 9 of 10 | 0 |
| dev-thermostat | 3 | 3 of 4 | 3 of 4 | 0 |
| dev-two-factor | 0 | 4 of 5 | 6 of 7 | 0 |
| dev-webhooks | 1 | 5 of 5 | 10 of 10 | 0 |
| dev-wishlist | 0 | 5 of 5 | 8 of 9 | 0 |
| **dev total** | 4 | 23 of 26 | 36 of 40 | 0 |
| hold-reminders | 2 | 4 of 4 | 6 of 7 | 0 |
| hold-search-api | 1 | 5 of 5 | 10 of 10 | 0 |
| hold-signup-form | 0 | 5 of 5 | 9 of 10 | 0 |
| hold-smart-lock | 0 | 5 of 5 | 6 of 8 | 0 |
| hold-workspaces | 5 | 2 of 5 | 6 of 6 | 0 |
| **hold total** | 8 | 21 of 24 | 37 of 41 | 0 |
| **Total** | 12 | 44 of 50 | 73 of 81 | 0 |

Questions held back behind `<N> more open questions after these.` are not counted: 3 in dev-invoice-export, 2 in dev-webhooks, 4 in hold-search-api.

## Gaps missed

- dev-invoice-export R6: a day with no finalised invoices (may be among the 3 questions held back).
- dev-thermostat R2: the temperature sensor fails.
- dev-two-factor R5: a user who lost the second factor.
- hold-workspaces R2: an invite to an address that is already a member.
- hold-workspaces R3: a member who is not an admin tries to delete a note. The reply wrote the `shall not` and asked nothing.
- hold-workspaces R5: what "leaves" means as an event.

## Other findings

- 6 of 10 replies wrote no requirement. In each, a missing system name or an open boundary blocked every statement.
- hold-reminders began with the line `Split Q-002 into two questions.`, which breaks the reply contract.
- hold-signup-form Q-005 asks three error texts in one question.
- dev-two-factor asks about code validity and wrong codes before the user has chosen a code-based factor.

## Turn 2: the follow-up reply

One run per input on Claude Sonnet 5.5, 2026-11-09. Each `turn2.md` holds the input, the first reply above, and scripted answers to every question that reply asked. Scored by hand against each `reference-turn2.md`, which was written before the run.

| Input | Requirements written | Gaps found | Needed questions | Invented values | `(new)` markers |
|-------|----------------------|------------|------------------|-----------------|-----------------|
| dev-invoice-export | 5 | 2 of 2 | 4 of 7 | 0 | missing |
| dev-thermostat | 2 | 0 of 2 | 0 of 0 | 0 | present |
| dev-two-factor | 4 | 1 of 3 | 2 of 2 | 0 | present |
| dev-webhooks | 4 | 1 of 1 | 4 of 5 | 0 | present |
| dev-wishlist | 10 | none listed | 2 of 2 | 0 | missing |
| **dev total** | 25 | 4 of 8 | 12 of 16 | 0 | |
| hold-reminders | 10 | 1 of 1 | 3 of 4 | 0 | present |
| hold-search-api | 8 | 2 of 2 | 6 of 9 | 0 | present |
| hold-signup-form | 9 | none listed | 2 of 2 | 1 | missing |
| hold-smart-lock | 5 | none listed | 2 of 2 | 0 | missing |
| hold-workspaces | 4 | 0 of 3 | 0 of 0 | 0 | present |
| **hold total** | 36 | 3 of 6 | 13 of 17 | 1 | |
| **Total** | 61 | 7 of 14 | 25 of 33 | 1 | |

No reply had a lint error or text outside the requirement and question lines.

### Gaps missed

- dev-thermostat T1, T2: a failed temperature sensor; the relay when the setpoint changes. The reply asked nothing.
- dev-two-factor T1, T2: a lost authenticator app; how a user enables two-factor authentication.
- hold-workspaces T1, T2, T3: the reply to a refused delete; an invite to an existing member; what "leaves" means. The reply asked nothing.

Six of these seven were already missed in the first reply. A gap the first reply misses is not found later.

### Other findings

- 4 of 10 replies left out the `(new)` marker: the four whose first reply had written no requirement.
- The invented value: hold-signup-form places each error "next to" a field, where the input says only "inline".
- hold-reminders wrote four requirements for one answer ("logs the failure and does not retry"), one pair for "fails" and one for "bounces".
- The questions that were not needed ask for detail no answer suggested: a CSV header row, the PagerDuty escalation policy, a cursor expiry time, a `Retry-After` header.
