"""Passing a ticket to the people above the agent."""


def to_lead(desk, ticket):
    lead = ticket.team.lead
    ticket.assignee = lead
    ticket.flags.add("escalated")
    ticket.escalated_at = desk.clock.now()
    desk.store.save(ticket)
    desk.bus.publish("ticket.escalated", ticket=ticket, lead=lead, watchers=[ticket.requester])
    return ticket
