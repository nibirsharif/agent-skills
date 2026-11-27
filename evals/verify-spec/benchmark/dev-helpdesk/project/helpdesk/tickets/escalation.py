"""Names for how far up a ticket has been passed."""

LEVELS = ("agent", "lead", "manager")


def level_of(ticket):
    """The level of whoever holds the ticket now."""
    if ticket.assignee == ticket.team.lead:
        return "lead"
    if ticket.assignee == ticket.team.on_call_manager:
        return "manager"
    return "agent"


def next_level(level):
    """The level above, or None at the top."""
    index = LEVELS.index(level) + 1
    return LEVELS[index] if index < len(LEVELS) else None
