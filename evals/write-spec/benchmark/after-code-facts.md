# After questions about facts the code holds

The change for [#22](https://github.com/nibirsharif/agent-skills/issues/22): when the input names a system, write-spec lists the project's top-level folders, and when one holds that system's code it reads at most 5 of its files and asks about a fact there that would change a requirement. No benchmark input has a project, so this run checks one thing: that the new step does not make a reply without a project invent a value. One run per input on `claude-sonnet-5-5` with Claude Code 2.1.327, 2026-11-24, first turn only.

Only invented values were scored, by hand, the same way as [after-shorter-rules.md](after-shorter-rules.md). Gaps found and needed questions were not scored, and the follow-up turn was not run.

| Input | Requirements written | Invented values |
|-------|----------------------|-----------------|
| dev-invoice-export | 0 | 0 |
| dev-thermostat | 4 | 0 |
| dev-two-factor | 0 | 0 |
| dev-webhooks | 3 | 0 |
| dev-wishlist | 0 | 0 |
| **dev total** | 7 | 0 |
| hold-reminders | 5 | 0 |
| hold-search-api | 2 | 0 |
| hold-signup-form | 0 | 0 |
| hold-smart-lock | 2 | 0 |
| hold-workspaces | 6 | 0 |
| **hold total** | 15 | 0 |
| **Total** | 22 | 0 |

## Reading

- No reply invented a system, value, or name. No reply names a file or asks about code: there is none to read.
- Two wordings are scored as not invented because the earlier records scored the same wordings that way. dev-webhooks counts the 10 seconds "of the notification service sending that request", where the input gives no starting point; the coverage-gaps runs wrote "of the request". hold-workspaces writes "Only admins can delete notes" as a rejected request, as the baseline reply did; this reply did not ask what the refused user receives.
- What the code rule does where there is code is measured by the eval cases `code-facts` and `code-no-facts`, not here: see the [eval README](../README.md#questions-about-the-code).
