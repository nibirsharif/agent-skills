"""One person on the list."""

import dataclasses
import datetime

STATUSES = ("pending", "active", "unsubscribed", "bounced")


@dataclasses.dataclass
class Subscriber:
    address: str
    status: str
    since: datetime.datetime
