"""One helpdesk: its clock, tickets, events, and outgoing messages, wired together."""

from helpdesk.core.clock import Clock
from helpdesk.core.events import Bus
from helpdesk.core.store import TicketStore
from helpdesk.notify import subscribers
from helpdesk.notify.outbox import Outbox
from helpdesk.notify.pager import Pager


class Helpdesk:
    def __init__(self, clock=None):
        self.clock = clock or Clock()
        self.store = TicketStore()
        self.bus = Bus()
        self.outbox = Outbox()
        self.pager = Pager()
        subscribers.register(self.bus, self.outbox)
