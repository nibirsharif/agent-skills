"""The payment provider. Refunds go out over HTTP in production; tests pass their own gateway."""


class GatewayError(Exception):
    pass


class PaymentGateway:
    def __init__(self, post):
        self._post = post

    def refund(self, payment_ref, amount):
        reply = self._post("/refunds", {"payment": payment_ref, "amount": str(amount)})
        if reply.get("status") != "ok":
            raise GatewayError(reply.get("reason", "refund rejected"))
