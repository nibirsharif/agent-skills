Set: dev. Domain: helpdesk, about 30 modules. Harder kinds: an implementation the requirement's words do not find, a fault across two modules, a second way in that skips a rule. Drift: a feature branch with one file no requirement covers.

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | The rule `stale_urgent` in `helpdesk/rules/builtin.py` calls `handoff.to_lead` after 30 minutes; neither is named for escalation, and `helpdesk/tickets/escalation.py` only names levels. `test_urgent_ticket_goes_to_the_lead_after_30_minutes` checks 29 and 30 minutes and passes. `unmet` here is a search that stopped at the file with the obvious name. |
| FR-002 | partial | Two modules. `handoff.to_lead` publishes the requester as `watchers`, and `notify/subscribers.py` mails `lead` and `cc`, so the requester gets nothing. `test_escalation_is_mailed` checks the lead's mail only. |
| FR-003 | unmet | Nothing pages. `settings.PAGE_AFTER_HOURS` is used nowhere, and no rule looks at `escalated_at`. `test_unanswered_escalation_pages_the_manager` passes because the test calls `desk.pager.page` itself. |
| FR-004 | untested | `replies.add_reply` discards the `escalated` flag for an agent's reply. No test replies to an escalated ticket. |
| FR-005 | partial | Two modules. `handlers.queue` sorts with `sorting.queue_key`, which puts escalated tickets first and then orders by priority and `created_at`, never `escalated_at`. `test_escalated_tickets_come_first_in_order_of_escalation` passes because its two tickets were created in the order they were escalated. |
| FR-006 | partial | The engine runs rules over open tickets only, and `test_closed_ticket_is_not_escalated` passes. `handlers.post_handoff`, routed at `POST /tickets/handoff`, calls `handoff.to_lead` with no check, so an agent can escalate a closed ticket. |
| FR-007 | skipped | `Blocked by Q-001`. |
| NFR-001 | met | `test_rules_run_over_1000_open_tickets_within_200_ms` measures the stated size against the stated limit and passes. |

Expected tally: `2 met, 3 partial, 1 unmet, 1 untested, 1 skipped`.

Expected drift: `helpdesk/admin/tags.py` (added on the branch, covered by no requirement). `tests/rules/test_speed.py` was also added on the branch and tests NFR-001, so it is not drift.

Faults a `met` would miss: FR-002, FR-003, FR-004, FR-005, FR-006. Anything but `met` on FR-001 or NFR-001 is a false alarm. A verdict other than `skipped` on FR-007 is a wrong verdict.
