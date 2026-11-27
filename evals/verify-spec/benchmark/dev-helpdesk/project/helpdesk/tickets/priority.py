"""How pressing a ticket is."""

PRIORITIES = ("low", "normal", "high", "urgent")


class UnknownPriority(ValueError):
    pass


def check(priority):
    if priority not in PRIORITIES:
        raise UnknownPriority(priority)


def set_priority(desk, ticket, priority):
    check(priority)
    ticket.priority = priority
    desk.store.save(ticket)
    return ticket
