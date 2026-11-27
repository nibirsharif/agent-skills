import unittest

from depot.core.models import Order
from tests.helpers import ACME, BOLT, new_depot, item


class Records(unittest.TestCase):
    def test_item_is_found_by_sku(self):
        depot = new_depot()
        made = item(depot)
        self.assertIs(depot.store.item(BOLT), made)

    def test_orders_are_listed_by_sku(self):
        depot = new_depot()
        depot.store.put_order(Order(1, BOLT, ACME, 24))
        depot.store.put_order(Order(2, "NUT-0002", ACME, 50))
        self.assertEqual([o.id for o in depot.store.orders(BOLT)], [1])
        self.assertEqual(len(depot.store.orders()), 2)

    def test_events_reach_their_handlers(self):
        depot, seen = new_depot(), []
        depot.bus.on("thing.happened", lambda value: seen.append(value))
        depot.bus.publish("thing.happened", value=3)
        self.assertEqual(seen, [3])
