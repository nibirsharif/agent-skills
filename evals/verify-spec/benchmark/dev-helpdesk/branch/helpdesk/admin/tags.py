"""Free-form tags on tickets, for the admin page's filters."""


def add_tag(desk, ticket, tag):
    ticket.flags.add(f"tag:{tag.strip().lower()}")
    desk.store.save(ticket)
    return ticket


def tagged(desk, tag):
    return [ticket for ticket in desk.store.all() if f"tag:{tag.strip().lower()}" in ticket.flags]
