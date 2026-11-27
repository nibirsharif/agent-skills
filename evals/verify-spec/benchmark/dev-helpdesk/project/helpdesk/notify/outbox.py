"""Mail waiting to go out."""

import dataclasses


@dataclasses.dataclass(frozen=True)
class Mail:
    to: str
    subject: str
    body: str


class Outbox:
    def __init__(self):
        self.mails = []

    def send(self, to, subject, body):
        self.mails.append(Mail(to, subject, body))

    def to(self, address):
        return [mail for mail in self.mails if mail.to == address]
