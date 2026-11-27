import unittest

from helpdesk.admin import cleanup, reports
from helpdesk.tickets import status
from tests.helpers import new_desk, ticket


class Admin(unittest.TestCase):
    def test_counts_by_status_and_team(self):
        desk = new_desk()
        ticket(desk)
        status.close(desk, ticket(desk))
        self.assertEqual(reports.by_status(desk), {"open": 1, "closed": 1})
        self.assertEqual(reports.by_team(desk), {"support": 1})
        self.assertEqual(len(reports.unassigned(desk)), 1)

    def test_old_closed_tickets_are_purged(self):
        desk = new_desk()
        old = status.close(desk, ticket(desk))
        kept = ticket(desk)
        desk.clock.advance(days=366)
        self.assertEqual(cleanup.purge_closed(desk), [old.id])
        self.assertEqual(desk.store.all(), [kept])
