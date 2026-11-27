"""Sending purchase orders to suppliers. The transport posts a payload to an endpoint."""

from depot.procurement import payload


class TransportError(Exception):
    pass


def send(depot, order, transport):
    order.status = "sent"
    order.sent_at = depot.clock.now()
    try:
        transport.post(order.supplier.endpoint, payload.of(order))
    except TransportError as error:
        order.note = str(error)
        order.sent_at = None
        raise
    return order


def send_drafts(depot, transport):
    """Sends every draft. Returns the orders the suppliers took."""
    taken = []
    for order in depot.store.orders():
        if order.status != "draft":
            continue
        try:
            taken.append(send(depot, order, transport))
        except TransportError:
            continue
    return taken
