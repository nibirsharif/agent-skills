Earlier in this conversation I gave you this input:

> Webhook delivery for the notification service.
> 
> - When an order changes status, the notification service POSTs the event to each webhook URL the merchant registered.
> - A delivery counts as successful when the endpoint answers with a 2xx status within 10 seconds.
> - Failed deliveries are retried.
> - Each request is signed so the merchant can verify it.
> - Merchants can see recent deliveries in the dashboard.

You replied:

FR-001: When the status of an order changes, the notification service shall send the event in an HTTP POST request to each webhook URL that the merchant registered.

Q-001: How many times does the notification service retry a failed delivery, at most?

Q-002: How long does the notification service wait before each retry?

Q-003: What does the notification service do when the last retry also fails?

Q-004: Which signature algorithm signs each request?

Q-005: Which key signs the requests: one key per merchant, or another scheme?

Q-006: In which request header does the notification service send the signature?

Q-007: Which system shows the recent deliveries to merchants in the dashboard?

Q-008: How many recent deliveries does the dashboard show?

Q-009: Which details of each delivery does the dashboard show?

Q-010: What fields does the event in the POST request body contain?

2 more open questions after these.


My answers:

Q-001: 5 times. Q-002: 1 minute, then 5 minutes, 30 minutes, 2 hours, and 12 hours. Q-003: mark the delivery as failed and send no more requests for that event to that URL. Q-004: HMAC-SHA256 over the request body. Q-005: one secret per webhook URL, created when the URL is registered. Q-006: X-Signature. Q-007: the merchant dashboard web app. Q-008: the 100 most recent deliveries of each webhook URL. Q-009: event type, time sent, response status, and number of attempts. Q-010: event ID, order ID, old status, new status, and the time of the change in UTC.
