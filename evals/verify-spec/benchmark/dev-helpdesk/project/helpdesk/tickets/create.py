"""Opening a ticket."""

from helpdesk.core.models import Ticket
from helpdesk.tickets import priority as priorities
from helpdesk.util.text import shorten


def open_ticket(desk, subject, requester, team, priority="normal"):
    priorities.check(priority)
    ticket = Ticket(desk.store.next_id(), shorten(subject), requester, team, desk.clock.now(), priority)
    desk.store.save(ticket)
    desk.bus.publish("ticket.opened", ticket=ticket)
    return ticket
