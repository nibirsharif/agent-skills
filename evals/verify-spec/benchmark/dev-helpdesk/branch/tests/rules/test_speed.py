import time
import unittest

from helpdesk.rules import engine
from tests.helpers import new_desk, ticket


class Speed(unittest.TestCase):
    def test_rules_run_over_1000_open_tickets_within_200_ms(self):
        desk = new_desk()
        for n in range(1000):
            ticket(desk, f"ticket {n}", priority=("urgent", "high", "normal", "low")[n % 4])
        desk.clock.advance(minutes=10)
        started = time.perf_counter()
        engine.run(desk)
        self.assertLess(time.perf_counter() - started, 0.2)
        self.assertEqual(len(desk.store.open()), 1000)
