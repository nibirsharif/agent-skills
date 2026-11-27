import unittest

from tests.helpers import new_desk, ticket


class Store(unittest.TestCase):
    def test_saved_ticket_is_found(self):
        desk = new_desk()
        made = ticket(desk)
        self.assertIs(desk.store.get(made.id), made)

    def test_open_leaves_out_closed(self):
        desk = new_desk()
        ticket(desk).status = "closed"
        kept = ticket(desk)
        self.assertEqual(desk.store.open(), [kept])

    def test_events_reach_their_handlers(self):
        desk, seen = new_desk(), []
        desk.bus.on("thing.happened", seen.append)
        desk.bus.publish("thing.happened", value=3)
        self.assertEqual(seen, [{"value": 3}])
