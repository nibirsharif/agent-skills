Set: dev. Domain: API. Form: bullet list.

Open decisions:
- R1: How many times, and at what intervals, a failed delivery is retried.
- R2: What the notification service does with a delivery that still fails after the last retry.
- R3: How a request is signed: the algorithm, the key, and where the signature is carried.
- R4: What "recent" means for the dashboard: how many deliveries or how far back.
- R5: Which system shows deliveries in the dashboard, and what it shows for each delivery.

Not given: a retry count or schedule, a signature algorithm or header name, a number of days or deliveries.
