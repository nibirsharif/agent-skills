"""The words of each message. Each function returns (subject, body)."""


def opened(ticket):
    return f"[#{ticket.id}] We have your request", f"We received: {ticket.subject}"


def escalated(ticket):
    return f"[#{ticket.id}] Passed to {ticket.team.lead.name}", f"{ticket.subject} is now with the team lead."


def closed(ticket):
    return f"[#{ticket.id}] Closed", f"We closed: {ticket.subject}"
