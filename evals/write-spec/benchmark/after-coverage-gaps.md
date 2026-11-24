# After the coverage-gaps and precedence rules

One run per input on Claude Sonnet 5.5, 2026-11-09, scored by hand the same way as [baseline-0.10.0.md](baseline-0.10.0.md). The dev first turn was run twice to see how much one run varies.

The held-out first-turn row was scored again on 2026-11-23, after hold-workspaces R1 was withdrawn ([#27](https://github.com/nibirsharif/agent-skills/issues/27)). The baseline reply had found R1, so its 21 of 24 is now 20 of 23. The reply of this run asked only from which event the 72 hours are measured, so R1 was one of its five misses, and its 19 of 24 is now 19 of 23. This record never listed its misses by input: scoring the five saved replies again gives 3 of 4, 5 of 5, 5 of 5, 4 of 5, and 2 of 5 with R1 missed, which is the 19.

| | Baseline 0.10.0 | After |
|---|---|---|
| First turn, dev: gaps found | 23 of 26 | 20 of 26 and 24 of 26 (two runs) |
| First turn, held out: gaps found | 20 of 23 | 19 of 23 |
| Follow-up turn, dev: gaps found | 4 of 8 | 6 of 8 |
| Follow-up turn, held out: gaps found | 3 of 6 | 4 of 6 |
| Follow-up turn, all: needed questions | 25 of 33 | 30 of 40 |
| Follow-up turn, all: requirements without `(new)` or `(changed)` | 30 of 61 | 0 of 57 |

## Reading

- The follow-up turn finds 10 of 14 open decisions, up from 7. That is at the three-item limit the [README](README.md) sets for calling a difference real, and the held-out half moved by one item.
- The first turn did not change measurably. The two dev runs differ by four items from each other, which is more than either differs from the baseline.
- The share of needed questions in the follow-up turn stayed at about three in four.

## Gaps found now that were missed before

- dev-thermostat, follow-up: the room temperature is not available; the relay when the setpoint changes.
- hold-workspaces, both turns: what a member who is not an admin receives when a delete is refused.
- dev-two-factor, first turn: a user who cannot supply the second factor.

## Gaps still missed

- dev-two-factor, follow-up: a lost authenticator app; how a user enables two-factor authentication.
- hold-workspaces: an invite to an address that is already a member; what "leaves" means as an event.
- dev-thermostat, first turn: a failed temperature sensor (asked in the follow-up turn).
