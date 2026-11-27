"""Items, orders, and movements held in memory."""


class Store:
    def __init__(self):
        self._items = {}
        self._orders = {}
        self.moves = []

    def put_item(self, item):
        self._items[item.sku] = item
        return item

    def item(self, sku):
        return self._items[sku]

    def items(self):
        return list(self._items.values())

    def next_order_id(self):
        return len(self._orders) + 1

    def put_order(self, order):
        self._orders[order.id] = order
        return order

    def order(self, order_id):
        return self._orders[order_id]

    def orders(self, sku=None):
        return [o for o in self._orders.values() if sku is None or o.sku == sku]
