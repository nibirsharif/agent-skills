"""Booking and cancelling rooms."""

from bookings import policy
from bookings.gateway import GatewayError
from bookings.models import Booking


class RoomTaken(Exception):
    pass


class RefundFailed(Exception):
    pass


class BookingService:
    def __init__(self, store, gateway, notifier, clock):
        self.store = store
        self.gateway = gateway
        self.notifier = notifier
        self.clock = clock

    def book(self, room, user_email, start, end, price, payment_ref):
        for other in self.store.for_room(room):
            if other.overlaps(start, end):
                raise RoomTaken(room)
        booking = Booking(self.store.next_id(), room, user_email, start, end, price, payment_ref)
        return self.store.add(booking)

    def cancel(self, booking_id):
        booking = self.store.get(booking_id)
        notice = (booking.start - self.clock()).total_seconds() / 60
        refund = policy.refund_for(booking.price, policy.is_late(notice))
        try:
            self.gateway.refund(booking.payment_ref, refund)
        except GatewayError as error:
            raise RefundFailed(str(error)) from error
        booking.status = "cancelled"
        self.notifier.cancelled(booking, refund)
        return refund
