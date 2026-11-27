"""Replies from the requester and from agents."""

from helpdesk.core.models import Reply


def add_reply(desk, ticket, author, body):
    reply = Reply(author, body, desk.clock.now())
    ticket.replies.append(reply)
    if author.is_agent:
        ticket.flags.discard("escalated")
        ticket.flags.add("waiting")
        if ticket.assignee is None:
            ticket.assignee = author
    else:
        ticket.flags.discard("waiting")
    desk.store.save(ticket)
    desk.bus.publish("ticket.replied", ticket=ticket, reply=reply)
    return reply
