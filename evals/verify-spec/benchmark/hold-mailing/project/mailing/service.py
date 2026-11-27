"""Joining and leaving the list."""

from mailing import addresses, tokens
from mailing.models import Subscriber


class AlreadySubscribed(Exception):
    pass


class SubscriptionService:
    def __init__(self, store, mailer, clock):
        self.store = store
        self.mailer = mailer
        self.clock = clock

    def subscribe(self, address):
        addresses.validate(address)
        if self.store.has(addresses.normalize(address)):
            raise AlreadySubscribed(address)
        subscriber = self.store.add(Subscriber(address, "pending", self.clock()))
        self.mailer.send(address, "Confirm your subscription", f"/confirm/{tokens.make(address)}")
        return subscriber

    def confirm(self, token):
        address = tokens.read(token)
        self.store.set_status(address, "active")
        return self.store.get(address)

    def unsubscribe(self, address):
        self.store.set_status(address, "unsubscribed")
        self.mailer.send(address, "You are unsubscribed", "You will get no more mail from us.")
