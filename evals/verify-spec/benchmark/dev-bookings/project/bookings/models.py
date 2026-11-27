"""A booking of one room for one stretch of time."""

import dataclasses
import datetime
import decimal


@dataclasses.dataclass
class Booking:
    id: int
    room: str
    user_email: str
    start: datetime.datetime
    end: datetime.datetime
    price: decimal.Decimal
    payment_ref: str
    status: str = "active"

    def overlaps(self, start, end):
        return self.start < end and start < self.end
