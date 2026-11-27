"""Tickets held in memory, by ID."""


class TicketStore:
    def __init__(self):
        self._tickets = {}

    def next_id(self):
        return len(self._tickets) + 1

    def save(self, ticket):
        self._tickets[ticket.id] = ticket
        return ticket

    def get(self, ticket_id):
        return self._tickets[ticket_id]

    def remove(self, ticket_id):
        del self._tickets[ticket_id]

    def open(self):
        return [t for t in self._tickets.values() if t.status == "open"]

    def all(self):
        return list(self._tickets.values())
