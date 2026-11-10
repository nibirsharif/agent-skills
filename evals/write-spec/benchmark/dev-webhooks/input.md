Webhook delivery for the notification service.

- When an order changes status, the notification service POSTs the event to each webhook URL the merchant registered.
- A delivery counts as successful when the endpoint answers with a 2xx status within 10 seconds.
- Failed deliveries are retried.
- Each request is signed so the merchant can verify it.
- Merchants can see recent deliveries in the dashboard.
