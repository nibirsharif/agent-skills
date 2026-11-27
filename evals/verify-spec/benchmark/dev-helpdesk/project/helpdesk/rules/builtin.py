"""The rules every helpdesk starts with."""

import datetime

from helpdesk import settings
from helpdesk.rules.registry import rule
from helpdesk.tickets import handoff, status


@rule("stale-urgent")
def stale_urgent(desk, ticket):
    """An urgent ticket that no agent has answered goes up a level."""
    if ticket.priority != "urgent" or "escalated" in ticket.flags:
        return False
    since = ticket.last_agent_reply() or ticket.created_at
    if desk.clock.now() - since < datetime.timedelta(minutes=settings.URGENT_REPLY_MINUTES):
        return False
    handoff.to_lead(desk, ticket)
    return True


@rule("auto-close")
def auto_close(desk, ticket):
    """A ticket that has waited on its requester for two weeks is closed."""
    if "waiting" not in ticket.flags or not ticket.replies:
        return False
    if desk.clock.now() - ticket.replies[-1].at < datetime.timedelta(days=settings.AUTO_CLOSE_DAYS):
        return False
    status.close(desk, ticket)
    return True
