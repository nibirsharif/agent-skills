"""Outgoing mail. The transport is a function that takes (to, subject, body) and returns the server's reply code."""


class MailRefused(Exception):
    pass


class Mailer:
    def __init__(self, transport):
        self._transport = transport

    def send(self, to, subject, body):
        code = self._transport(to, subject, body)
        if code >= 500:
            raise MailRefused(f"{to}: {code}")
