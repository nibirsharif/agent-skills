"""Turns helpdesk events into mail."""

from helpdesk.notify import templates


def register(bus, outbox):
    bus.on("ticket.opened", lambda event: _opened(outbox, event))
    bus.on("ticket.escalated", lambda event: _escalated(outbox, event))
    bus.on("ticket.closed", lambda event: _closed(outbox, event))


def _opened(outbox, event):
    ticket = event["ticket"]
    outbox.send(ticket.requester.email, *templates.opened(ticket))


def _escalated(outbox, event):
    subject, body = templates.escalated(event["ticket"])
    for person in [event["lead"], *event.get("cc", [])]:
        outbox.send(person.email, subject, body)


def _closed(outbox, event):
    ticket = event["ticket"]
    outbox.send(ticket.requester.email, *templates.closed(ticket))
