"""Bookings held in memory, by ID and by room."""


class BookingStore:
    def __init__(self):
        self._bookings = {}
        self._by_room = {}

    def next_id(self):
        return len(self._bookings) + 1

    def add(self, booking):
        self._bookings[booking.id] = booking
        self._by_room.setdefault(booking.room, []).append(booking)
        return booking

    def get(self, booking_id):
        return self._bookings[booking_id]

    def for_room(self, room):
        return [b for b in self._by_room.get(room, []) if b.status == "active"]

    def all(self):
        return list(self._bookings.values())
