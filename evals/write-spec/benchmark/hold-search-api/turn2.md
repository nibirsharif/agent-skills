Earlier in this conversation I gave you this input:

> Public search endpoint for the catalogue API: GET /products?q= returns matching products, 20 per page, sorted by relevance. Clients page with a cursor. Anonymous clients are limited to 60 requests per minute; clients with an API key get more. Over the limit returns 429.

You replied:

FR-001: When a client sends a GET request to /products with the query parameter q, the catalogue API shall return at most 20 products in each page of results.

Q-001: What is the name of the request parameter that carries the cursor?

Q-002: What does the catalogue API return with each page so a client can request the next page?

Q-003: What identifies one anonymous client for the limit of 60 requests per minute: the IP address or something else?

Q-004: Does the anonymous limit count requests in a fixed window that starts at each minute boundary in UTC, or in any rolling 60 seconds?

Q-005: How many requests per minute does a client with an API key get?

Q-006: In which request header or parameter does a client send its API key?

Q-007: Which product fields does the catalogue API search for q, and how does it compare q to them?

Q-008: What defines the relevance order of the returned products?

Q-009: What does the catalogue API do when a request supplies a cursor that is invalid or expired?

Q-010: What does the catalogue API do when a request to /products has no q parameter or an empty q?

4 more open questions after these.


My answers:

Q-001: cursor. Q-002: a next_cursor field, which is absent on the last page. Q-003: the IP address. Q-004: a fixed window that starts at each minute boundary in UTC. Q-005: 600. Q-006: the X-API-Key header. Q-007: the product name and description, with a case-insensitive substring match. Q-008: products whose name matches come before products that match only in the description; within each group, by name from A to Z. Q-009: HTTP status 400. Q-010: HTTP status 400.
