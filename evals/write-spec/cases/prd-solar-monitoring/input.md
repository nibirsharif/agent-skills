Write EARS requirements for this PRD.

# Rooftop Solar Monitoring: Product Requirements

**Version:** 0.9 (draft for review)

## 1. Overview

Rooftop Solar Monitoring lets homeowners with a rooftop solar system see how much power their panels produce and get alerts when something goes wrong. Installers use a portal to see the systems they installed. The goal is to cut support calls that ask "is my system working?".

## 2. Users

- Homeowner: owns one solar system with one inverter gateway.
- Installer: installs systems and supports the homeowners who bought them.

## 3. Scope

In scope: production monitoring, alerts (push and email), the mobile app, the installer portal, and a monthly report.

Out of scope: billing, battery control, selling power back to the grid, and languages other than English.

## 4. Functional requirements

### 4.1 Inverter gateway

- FR-1.1: Every 5 minutes, the inverter gateway sends a production reading to the monitoring service.
- FR-1.2: If the monitoring service does not acknowledge a reading within 30 seconds of the gateway sending it, the gateway stores the reading and resends it with the next reading.
- FR-1.3: The gateway should buffer readings while offline for a reasonable period.
- FR-1.4: Readings are timestamped in UTC by the gateway.

### 4.2 Monitoring service

- FR-2.1: When a reading arrives, the monitoring service stores it with the gateway ID.
- FR-2.2: When a gateway sends a reading whose production value is more than the system's rated capacity, the monitoring service discards the reading and logs the gateway ID.
- FR-2.3: During daylight (from sunrise to sunset at the system's location), if 60 minutes pass with no reading from a system's gateway, the monitoring service sets that system's status to "Offline".
- FR-2.4: The monitoring service must show production data in real time.
- FR-2.5: Store readings in TimescaleDB.
- FR-2.6: The system archives readings older than 5 years.

### 4.3 Alerts

- FR-3.1: When the monitoring service sets a system's status to "Offline", the alert service sends the homeowner a push notification and an email.
- FR-3.2: When a day's production is less than 50% of the forecast for that day, the alert service notifies the homeowner by push or email.
- FR-3.3: Alert emails are sent within 5 minutes of the event that triggers them.
- FR-3.4: Alert emails are sent within 15 minutes of the event that triggers them.
- FR-3.5: Where a homeowner has turned on quiet hours (a start and end time the homeowner sets in the mobile app), the alert service holds every alert except Offline alerts until quiet hours end.
- FR-3.6: Homeowners can change their alert preferences.
- FR-3.7: The alert service limits alerts so homeowners are not spammed.

### 4.4 Mobile app

- FR-4.1: The mobile app shows today's production, in kWh, on the home screen.
- FR-4.2: The home screen should feel clean and modern.
- FR-4.3: When a system is offline, the app displays a friendly message explaining the problem.
- FR-4.4: Where the battery add-on is installed, the mobile app shows the battery charge level as a percentage.
- FR-4.5: As a homeowner, I want to export my production history as a CSV file from the mobile app so that I can share it with my accountant.

### 4.5 Installer portal

- FR-5.1: The installer portal shows each installer every system that installer installed.
- FR-5.2: The portal supports exporting fleet data.
- FR-5.3: The installer portal shows an installer a homeowner's phone number only after the homeowner grants that installer access to it.
- FR-5.4: Installers get a weekly summary email on Mondays at 08:00.

### 4.6 Monthly report

- FR-6.1: On the 1st of each month, the monitoring service emails each homeowner a report of the previous month's production.
- FR-6.2: The report compares production with the same month last year where applicable.

## 5. Non-functional requirements

- NFR-1: The home screen loads in under 2 seconds.
- NFR-2: 99.9% availability.
- NFR-3: The mobile app meets WCAG 2.2 level AA.
- NFR-4: The platform must be secure.
- NFR-5: The monitoring service handles up to 50,000 gateways.

## 6. Timeline

Beta in Q3, launch in Q4.
