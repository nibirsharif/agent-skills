import unittest

from helpdesk.tickets import assign, priority, status
from tests.helpers import ADA, BO, NOW, new_desk, ticket


class Create(unittest.TestCase):
    def test_new_ticket_is_open(self):
        made = ticket(new_desk())
        self.assertEqual((made.status, made.created_at), ("open", NOW))

    def test_unknown_priority_is_refused(self):
        with self.assertRaises(priority.UnknownPriority):
            ticket(new_desk(), priority="yesterday")

    def test_requester_is_told(self):
        desk = new_desk()
        ticket(desk)
        self.assertEqual(desk.outbox.to(ADA.email)[0].subject, "[#1] We have your request")


class AssignAndStatus(unittest.TestCase):
    def test_only_an_agent_is_assigned(self):
        desk = new_desk()
        with self.assertRaises(assign.NotAnAgent):
            assign.assign(desk, ticket(desk), ADA)

    def test_assign_and_unassign(self):
        desk = new_desk()
        made = assign.assign(desk, ticket(desk), BO)
        self.assertEqual(made.assignee, BO)
        self.assertIsNone(assign.unassign(desk, made).assignee)

    def test_close_and_reopen(self):
        desk = new_desk()
        made = status.close(desk, ticket(desk))
        self.assertEqual((made.status, made.closed_at), ("closed", NOW))
        self.assertEqual(status.reopen(desk, made).status, "open")

    def test_set_priority(self):
        desk = new_desk()
        self.assertEqual(priority.set_priority(desk, ticket(desk), "high").priority, "high")
