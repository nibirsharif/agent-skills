import unittest

from helpdesk.api import router
from helpdesk.api.handlers import Forbidden
from tests.helpers import ADA, BO, new_desk, ticket


class Queue(unittest.TestCase):
    def setUp(self):
        self.desk = new_desk()

    def queue(self):
        return [t.subject for t in router.dispatch(self.desk, "GET", "/queue", BO)]

    def test_escalated_tickets_come_first_in_order_of_escalation(self):
        ticket(self.desk, "normal one")
        first = ticket(self.desk, "first up", priority="urgent")
        self.desk.clock.advance(minutes=5)
        second = ticket(self.desk, "second up", priority="urgent")
        router.dispatch(self.desk, "POST", "/tickets/handoff", BO, ticket_id=first.id)
        self.desk.clock.advance(minutes=5)
        router.dispatch(self.desk, "POST", "/tickets/handoff", BO, ticket_id=second.id)
        self.assertEqual(self.queue(), ["first up", "second up", "normal one"])

    def test_more_pressing_tickets_come_before_older_ones(self):
        ticket(self.desk, "old and low", priority="low")
        self.desk.clock.advance(minutes=5)
        ticket(self.desk, "new and high", priority="high")
        self.assertEqual(self.queue(), ["new and high", "old and low"])

    def test_queue_is_for_agents(self):
        with self.assertRaises(Forbidden):
            router.dispatch(self.desk, "GET", "/queue", ADA)
