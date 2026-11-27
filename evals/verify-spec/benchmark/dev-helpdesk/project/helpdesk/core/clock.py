"""The time, which tests set and move."""

import datetime


class Clock:
    def __init__(self, now=None):
        self._now = now

    def now(self):
        return self._now or datetime.datetime.now()

    def set(self, now):
        self._now = now

    def advance(self, **delta):
        self._now = self.now() + datetime.timedelta(**delta)
