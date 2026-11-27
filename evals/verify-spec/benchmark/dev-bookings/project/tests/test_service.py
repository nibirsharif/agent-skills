import datetime
import decimal
import unittest
from unittest import mock

from bookings.service import BookingService, RoomTaken
from bookings.store import BookingStore

START = datetime.datetime(2026, 12, 10, 9, 0)
PRICE = decimal.Decimal("100.00")


def service_at(now):
    return BookingService(BookingStore(), mock.Mock(), mock.Mock(), lambda: now)


def booked(service, room="Elm", start=START):
    return service.book(room, "ada@example.org", start, start + datetime.timedelta(hours=2), PRICE, "pay-77")


class Book(unittest.TestCase):
    def setUp(self):
        self.service = service_at(START - datetime.timedelta(days=7))

    def test_free_room_is_booked_active(self):
        booking = booked(self.service)
        self.assertEqual(booking.status, "active")
        self.assertIs(self.service.store.get(booking.id), booking)

    def test_overlapping_booking_is_rejected(self):
        booked(self.service)
        with self.assertRaises(RoomTaken):
            booked(self.service, start=START + datetime.timedelta(hours=1))
        self.assertEqual(len(self.service.store.for_room("Elm")), 1)

    def test_booking_that_starts_as_another_ends_is_stored(self):
        booked(self.service)
        booked(self.service, start=START + datetime.timedelta(hours=2))
        self.assertEqual(len(self.service.store.for_room("Elm")), 2)

    def test_other_room_at_the_same_time_is_stored(self):
        booked(self.service)
        self.assertEqual(booked(self.service, room="Oak").status, "active")


class Cancel(unittest.TestCase):
    def test_early_cancellation_refunds_the_price(self):
        service = service_at(START - datetime.timedelta(days=3))
        booking = booked(service)
        self.assertEqual(service.cancel(booking.id), PRICE)
        self.assertEqual(booking.status, "cancelled")

    def test_late_cancellation_keeps_the_fee(self):
        service = service_at(START - datetime.timedelta(minutes=10))
        booking = booked(service)
        self.assertEqual(service.cancel(booking.id), decimal.Decimal("80.00"))

    def test_refund_request_goes_to_the_gateway(self):
        service = service_at(START - datetime.timedelta(days=3))
        booking = booked(service)
        service.cancel(booking.id)
        service.gateway.refund.assert_called_once_with("pay-77", PRICE)

    def test_user_is_told_the_refund(self):
        service = service_at(START - datetime.timedelta(minutes=10))
        booking = booked(service)
        refund = service.cancel(booking.id)
        service.notifier.cancelled.assert_called_once_with(booking, refund)

    def test_cancelled_booking_frees_the_room(self):
        service = service_at(START - datetime.timedelta(days=3))
        service.cancel(booked(service).id)
        self.assertEqual(booked(service).status, "active")
