import datetime
import decimal
import unittest

from bookings.models import Booking
from bookings.notify import Notifier

START = datetime.datetime(2026, 12, 10, 9, 0)


class Cancelled(unittest.TestCase):
    def setUp(self):
        self.sent = []
        self.notifier = Notifier(lambda to, subject, body: self.sent.append((to, subject, body)))
        self.booking = Booking(
            1, "Elm", "ada@example.org", START, START + datetime.timedelta(hours=2),
            decimal.Decimal("100.00"), "pay-77", "cancelled",
        )

    def test_message_goes_to_the_user(self):
        self.notifier.cancelled(self.booking, decimal.Decimal("100.00"))
        self.assertEqual(self.sent[0][0], "ada@example.org")

    def test_message_states_the_refund(self):
        self.notifier.cancelled(self.booking, decimal.Decimal("100.00"))
        self.assertIn("refunded 100.00", self.sent[0][2])
