"""Removing what the helpdesk no longer needs to keep."""

import datetime

from helpdesk import settings


def purge_closed(desk):
    """Removes tickets closed longer ago than the purge limit. Returns their IDs."""
    limit = desk.clock.now() - datetime.timedelta(days=settings.PURGE_AFTER_DAYS)
    old = [t.id for t in desk.store.all() if t.status == "closed" and t.closed_at and t.closed_at < limit]
    for ticket_id in old:
        desk.store.remove(ticket_id)
    return old
