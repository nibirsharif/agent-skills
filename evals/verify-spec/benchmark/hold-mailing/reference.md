Set: hold. Domain: mailing list. Harder kinds: a fault across two modules, tests through mocks, a rule kept outside the system the requirement names. Drift: none to check (`main`, nothing uncommitted).

Expected rows:

| ID | Verdict | Planted state |
|----|---------|---------------|
| FR-001 | met | `SubscriptionService.subscribe` stores a `pending` subscriber; `test_new_address_is_stored_pending` passes. |
| FR-002 | partial | The named system. `addresses.validate` is called in `SubscriptionService.subscribe`, the only caller of `SubscriberStore.add`; the store the requirement names stores any address. `test_address_without_at_is_rejected` drives the service and passes. An open row, `met` or `partial`, until the rules decided it. |
| FR-003 | partial | Two modules. `subscribe` looks up the lower-cased address, and `SubscriberStore.add` keys the subscriber by the address as it was typed, so `Ada@Example.org` and then `ada@example.org` are both stored. `test_address_already_stored_is_rejected` passes because it subscribes the same lower-case address twice. |
| FR-004 | met | `confirm` sets `active`; `test_confirmation_makes_the_subscriber_active` passes. |
| FR-005 | met | `unsubscribe` sends one message to the address. `test_unsubscribe_sends_one_confirmation` checks the call on a mock mailer, which is the boundary: the service code runs. |
| FR-006 | partial | Two modules, behind a mock. `SubscriberStore.active` leaves out `unsubscribed` and `bounced` and keeps `pending`, so a campaign reaches addresses that never confirmed. `test_campaign_goes_to_active_subscribers_only` passes because the store is a mock, and `test_active_leaves_out_unsubscribed_and_bounced` because it has no `pending` subscriber. |
| FR-007 | untested | `Campaigns.send` sets `bounced` when the mailer raises `MailRefused`, which is right. `test_refused_message_is_reported_bounced` replaces `Campaigns.send` with a mock, so it checks only the report's text. No test makes the mailer refuse. |
| FR-008 | partial or unmet | Open row, a gap either way. `web.unsubscribe_page` unsubscribes the token's address, and `test_unsubscribe_link_unsubscribes_the_address` calls it directly; `ROUTES` has no `/unsubscribe/` entry, so `handle` answers 404. The rules do not say whether code the trigger cannot reach is `partial` or `unmet`. |
| NFR-001 | untested | `test_recipient_list_is_built_quickly` measures 500 subscribers, not 50,000: a threshold with no test that measures it. |

Expected tally: `3 met, 4 partial, 2 untested`, with FR-008 as `partial`, or `3 met, 3 partial, 1 unmet, 2 untested` with it as `unmet`.

Expected drift: `not checked (no feature branch)`.

Faults a `met` would miss: FR-002, FR-003, FR-006, FR-007, FR-008, NFR-001. Anything but `met` on FR-001, FR-004, or FR-005 is a false alarm.
