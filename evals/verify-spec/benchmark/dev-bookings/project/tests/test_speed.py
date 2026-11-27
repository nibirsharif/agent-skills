import datetime
import decimal
import time
import unittest

from bookings.models import Booking
from bookings.store import BookingStore

START = datetime.datetime(2026, 12, 10, 9, 0)


class RoomLookup(unittest.TestCase):
    def test_room_lookup_is_fast(self):
        store = BookingStore()
        for n in range(100):
            start = START + datetime.timedelta(hours=3 * n)
            store.add(Booking(n + 1, f"room-{n % 10}", "ada@example.org", start,
                              start + datetime.timedelta(hours=2), decimal.Decimal("40.00"), f"pay-{n}"))
        started = time.perf_counter()
        found = store.for_room("room-3")
        self.assertLess(time.perf_counter() - started, 0.05)
        self.assertEqual(len(found), 10)
