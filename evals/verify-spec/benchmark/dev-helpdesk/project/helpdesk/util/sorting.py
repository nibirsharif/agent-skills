"""The order of the agents' queue."""

from helpdesk.tickets.priority import PRIORITIES


def queue_key(ticket):
    """Tickets passed to a lead come first, then the most pressing, then the oldest."""
    passed_up = 0 if "escalated" in ticket.flags else 1
    return (passed_up, -PRIORITIES.index(ticket.priority), ticket.created_at)
