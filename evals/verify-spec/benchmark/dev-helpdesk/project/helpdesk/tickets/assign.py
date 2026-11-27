"""Who holds a ticket."""


class NotAnAgent(ValueError):
    pass


def assign(desk, ticket, agent):
    if not agent.is_agent:
        raise NotAnAgent(agent.email)
    ticket.assignee = agent
    desk.store.save(ticket)
    return ticket


def unassign(desk, ticket):
    ticket.assignee = None
    desk.store.save(ticket)
    return ticket
