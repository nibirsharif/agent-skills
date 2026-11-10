Earlier in this conversation I gave you this input:

> Notes from 12 May sync: nightly invoice export
> 
> Finance wants the invoices in their SFTP by morning. Export runs at 02:00, takes all invoices finalised the previous day, one CSV per day. If SFTP is down we retry. Priya: file name must have the date. Tom: do we need to alert someone if it fails? Yes, the finance on-call.

You replied:

Q-001: Which component performs the nightly invoice export?

Q-002: Which time zone applies to the 02:00 start and to the day boundaries of "the previous day"?

Q-003: Which invoice status or timestamp marks an invoice as finalised?

Q-004: What is the exact file name format, including the position and format of the date? Proposed: the date in ISO 8601 format (YYYY-MM-DD).

Q-005: Which SFTP server and directory does the export upload the CSV file to?

Q-006: How does the export detect that the SFTP server is down: a refused connection, or no response within how many seconds?

Q-007: How many times does the export retry the upload?

Q-008: By what time of day, in which time zone, must the CSV file be in the SFTP directory?

Q-009: At which event does the export alert the finance on-call: after each failed attempt, or after the last retry fails?

Q-010: Through which channel does the export alert the finance on-call?

3 more open questions after these.


My answers:

Q-001: the billing service. Q-002: UTC. Q-003: an invoice is finalised when its status is set to "final"; the time the status was set counts. Q-004: invoices-YYYY-MM-DD.csv, with the date of the previous day. Q-005: host sftp.finance.example, directory /incoming/invoices. Q-006: a refused connection, or no response within 30 seconds. Q-007: 3 times, 10 minutes apart. Q-008: 06:00 UTC. Q-009: after the last retry fails. Q-010: a PagerDuty page.
