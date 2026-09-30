REQ-001: When 5 minutes have passed since the inverter gateway sent the previous production reading, the inverter gateway shall send a production reading to the monitoring service.

REQ-002: If the monitoring service does not acknowledge a production reading within 30 seconds of the inverter gateway sending the reading, then the inverter gateway shall store the reading and resend the reading with the next production reading.

REQ-003: The inverter gateway shall timestamp each production reading in UTC.

REQ-004: When a production reading arrives, the monitoring service shall store the reading with the gateway ID.

REQ-005: If a production reading has a production value more than the rated capacity of the solar system, then the monitoring service shall discard the reading and log the gateway ID.

REQ-006: While the time at the location of a solar system is after sunrise and before sunset, if 60 minutes pass with no production reading from the inverter gateway of that solar system, then the monitoring service shall set the status of that solar system to "Offline".

REQ-007: When the monitoring service sets the status of a solar system to "Offline", the alert service shall send the homeowner of that solar system a push notification and an email.

REQ-008: While quiet hours are on for a homeowner, when an alert other than an Offline alert is due for that homeowner, the alert service shall hold the alert until the quiet hours end.

REQ-009: The mobile app shall display the production of the current day in kWh on the home screen.

REQ-010: Where the battery add-on is installed, the mobile app shall display the battery charge level as a percentage.

REQ-011: When a homeowner requests an export of the production history, the mobile app shall export the production history of that homeowner as a CSV file.

REQ-012: The installer portal shall display to each installer every solar system that installer installed.

REQ-013: While a homeowner has not granted an installer access to the phone number of the homeowner, the installer portal shall not display the phone number of the homeowner to that installer.

NFR-001: The mobile app shall comply with WCAG 2.2 level AA.

Q-001: Which system archives production readings older than 5 years?

Q-002: How long must the inverter gateway keep buffered readings while it cannot reach the monitoring service?

Q-003: What decides whether the alert service sends a low-production alert by push notification or by email?

Q-004: FR-3.3 says alert emails are sent within 5 minutes of the triggering event and FR-3.4 says within 15 minutes: which limit applies?

Q-005: What is the rate limit for alerts to one homeowner: how many alerts in what time window?

Q-006: What exact text does the mobile app display when a solar system is offline?

Q-007: In which time zone is the Monday 08:00 installer summary email sent?

Q-008: Is storing readings in TimescaleDB a constraint the monitoring service must meet?

Q-009: What is the maximum delay, in seconds, from the arrival of a production reading at the monitoring service to its display in the mobile app?

Q-010: What does the alert service do when an Offline alert cannot be delivered?

11 more open questions after these.
