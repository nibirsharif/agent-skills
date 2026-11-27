"""What each request does. A handler takes the helpdesk, the user who asked, and the request's fields."""

from helpdesk import settings
from helpdesk.tickets import create, handoff, replies, status
from helpdesk.util import paging, sorting


class Forbidden(Exception):
    pass


def _agents_only(user):
    if not user.is_agent:
        raise Forbidden(user.email)


def queue(desk, user, page=1):
    _agents_only(user)
    tickets = sorted(desk.store.open(), key=sorting.queue_key)
    return paging.page(tickets, page, settings.QUEUE_PAGE_SIZE)


def post_ticket(desk, user, subject, team, priority="normal"):
    return create.open_ticket(desk, subject, user, team, priority)


def post_reply(desk, user, ticket_id, body):
    return replies.add_reply(desk, desk.store.get(ticket_id), user, body)


def post_close(desk, user, ticket_id):
    _agents_only(user)
    return status.close(desk, desk.store.get(ticket_id))


def post_handoff(desk, user, ticket_id):
    """An agent passes a ticket to the team lead by hand."""
    _agents_only(user)
    return handoff.to_lead(desk, desk.store.get(ticket_id))
