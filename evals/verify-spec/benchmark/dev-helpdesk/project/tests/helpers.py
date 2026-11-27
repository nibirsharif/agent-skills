"""People, a team, and a helpdesk with a set clock, for the tests."""

import datetime

from helpdesk.app import Helpdesk
from helpdesk.core.clock import Clock
from helpdesk.core.models import Team, User
from helpdesk.tickets.create import open_ticket

NOW = datetime.datetime(2026, 11, 23, 9, 0)
ADA = User("ada@example.org", "Ada")
BO = User("bo@helpdesk.example", "Bo", is_agent=True)
LEE = User("lee@helpdesk.example", "Lee", is_agent=True)
MAX = User("max@helpdesk.example", "Max", is_agent=True)
SUPPORT = Team("support", lead=LEE, on_call_manager=MAX)


def new_desk():
    return Helpdesk(Clock(NOW))


def ticket(desk, subject="Printer is on fire", priority="normal"):
    return open_ticket(desk, subject, ADA, SUPPORT, priority)
