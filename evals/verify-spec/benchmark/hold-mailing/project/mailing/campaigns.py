"""Sending one message to the list."""

import dataclasses

from mailing.mailer import MailRefused


@dataclasses.dataclass
class SendResult:
    sent: int = 0
    bounced: list = dataclasses.field(default_factory=list)


class Campaigns:
    def __init__(self, store, mailer):
        self.store = store
        self.mailer = mailer

    def recipients(self):
        return [subscriber.address for subscriber in self.store.active()]

    def send(self, subject, body):
        result = SendResult()
        for address in self.recipients():
            try:
                self.mailer.send(address, subject, body)
            except MailRefused:
                self.store.set_status(address, "bounced")
                result.bounced.append(address)
            else:
                result.sent += 1
        return result
