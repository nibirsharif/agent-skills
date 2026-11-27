"""Emails to the person who booked."""


class Notifier:
    def __init__(self, send):
        self._send = send

    def cancelled(self, booking, refund):
        body = (
            f"Your booking of {booking.room} on {booking.start:%Y-%m-%d} is cancelled.\n"
            f"We have refunded {booking.price:.2f} to your card.\n"
        )
        self._send(booking.user_email, "Booking cancelled", body)
