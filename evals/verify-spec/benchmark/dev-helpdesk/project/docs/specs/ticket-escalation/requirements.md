# Requirements: Ticket Escalation

**Version:** 1.0
**Date:** 2026-11-22
**Status:** Draft

## 1. Functional Requirements

FR-001: When an open ticket of priority `urgent` has had no agent reply for 30 minutes, the helpdesk shall escalate the ticket to its team's lead.

FR-002: When a ticket is escalated, the helpdesk shall email the team's lead and the ticket's requester.

FR-003: If an escalated ticket has had no agent reply 2 hours after it was escalated, then the helpdesk shall page the team's on-call manager.

FR-004: When an agent replies to an escalated ticket, the helpdesk shall remove the ticket's escalated mark.

FR-005: When an agent opens the queue, the helpdesk shall list escalated tickets first, ordered by the time of escalation, earliest first.

FR-006: If a ticket is closed, then the helpdesk shall not escalate it.

FR-007: Where a team has a deputy lead, the helpdesk shall escalate the ticket to the deputy when the lead is away. Blocked by Q-001.

## 2. Non-Functional Requirements

NFR-001: The helpdesk shall evaluate its rules for 1,000 open tickets within 200 milliseconds.

## 3. Open Questions

Q-001: How does the helpdesk know that a lead is away?
