import argparse
import datetime
import decimal
import io
import unittest
from unittest import mock

from bookings.cli import cancel_command, main
from bookings.service import BookingService, RefundFailed
from bookings.store import BookingStore

NOW = datetime.datetime(2026, 12, 1, 12, 0)


def new_service():
    return BookingService(BookingStore(), mock.Mock(), mock.Mock(), lambda: NOW)


BOOK = ["book", "Elm", "ada@example.org", "2026-12-10T09:00", "2", "100.00", "pay-77"]


class Book(unittest.TestCase):
    def test_book_prints_the_booking(self):
        out = io.StringIO()
        self.assertEqual(main(BOOK, new_service(), out), 0)
        self.assertEqual(out.getvalue(), "Booked Elm: booking 1.\n")

    def test_taken_room_is_reported(self):
        service, out = new_service(), io.StringIO()
        main(BOOK, service, io.StringIO())
        self.assertEqual(main(BOOK, service, out), 1)
        self.assertEqual(out.getvalue(), "Elm is taken at that time.\n")

    def test_list_shows_the_room(self):
        service, out = new_service(), io.StringIO()
        main(BOOK, service, io.StringIO())
        main(["list", "Elm"], service, out)
        self.assertEqual(out.getvalue(), "1  2026-12-10 09:00  ada@example.org\n")


class Cancel(unittest.TestCase):
    def setUp(self):
        self.service = new_service()
        main(BOOK, self.service, io.StringIO())
        self.out = io.StringIO()

    def test_cancel_prints_the_refund(self):
        code = cancel_command(argparse.Namespace(id=1), self.service, self.out)
        self.assertEqual(code, 0)
        self.assertEqual(self.out.getvalue(), "Cancelled booking 1. Refunded 100.00.\n")
        self.assertEqual(self.service.store.get(1).status, "cancelled")

    def test_rejected_refund_leaves_the_booking_active(self):
        with mock.patch.object(BookingService, "cancel", side_effect=RefundFailed("card closed")):
            code = cancel_command(argparse.Namespace(id=1), self.service, self.out)
        self.assertEqual(code, 1)
        self.assertEqual(self.out.getvalue(), "Not cancelled: card closed\n")
        self.assertEqual(self.service.store.get(1).status, "active")
