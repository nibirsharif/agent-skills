"""One depot: its clock, records, and events, wired together."""

from depot import hooks
from depot.core.bus import Bus
from depot.core.clock import Clock
from depot.core.store import Store


class Depot:
    def __init__(self, clock=None):
        self.clock = clock or Clock()
        self.store = Store()
        self.bus = Bus()
        hooks.attach(self)
