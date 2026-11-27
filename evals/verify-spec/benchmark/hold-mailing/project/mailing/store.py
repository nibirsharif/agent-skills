"""Subscribers held in memory, by address."""


class SubscriberStore:
    def __init__(self):
        self._rows = {}

    def add(self, subscriber):
        self._rows[subscriber.address] = subscriber
        return subscriber

    def has(self, address):
        return address in self._rows

    def get(self, address):
        return self._rows[address]

    def set_status(self, address, status):
        self._rows[address].status = status

    def active(self):
        """The subscribers a campaign may be sent to."""
        return [s for s in self._rows.values() if s.status not in ("unsubscribed", "bounced")]

    def count(self):
        return len(self._rows)
