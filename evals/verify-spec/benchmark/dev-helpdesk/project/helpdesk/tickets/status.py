"""Closing and reopening."""


def close(desk, ticket):
    ticket.status = "closed"
    ticket.closed_at = desk.clock.now()
    ticket.flags.discard("waiting")
    desk.store.save(ticket)
    desk.bus.publish("ticket.closed", ticket=ticket)
    return ticket


def reopen(desk, ticket):
    ticket.status = "open"
    ticket.closed_at = None
    desk.store.save(ticket)
    return ticket
