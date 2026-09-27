REQ-001: When an admin clicks "Export CSV" on the Reports page, the export service shall email the report as a CSV file to the email address of that admin within 5 minutes of the click.

REQ-002: If a report has more than 100,000 rows, then the export service shall reject the export and display "Report too large to export".

REQ-003: Where the audit module is installed, the export service shall log every export with the user ID of the admin and the export time in UTC.

Q-001: What does the export service do when the report email cannot be delivered?
