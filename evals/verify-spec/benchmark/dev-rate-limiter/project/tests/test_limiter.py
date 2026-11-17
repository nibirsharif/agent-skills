import unittest

from ratelimit.limiter import LIMIT, Limiter, RateLimited


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class Accepts(unittest.TestCase):
    def test_accepts_up_to_the_limit(self):
        limiter = Limiter(FakeClock())
        for _ in range(5):
            limiter.check("alice")

    def test_clients_are_counted_apart(self):
        limiter = Limiter(FakeClock())
        for _ in range(5):
            limiter.check("alice")
        limiter.check("bob")


class Rejects(unittest.TestCase):
    def test_sixth_request_is_rejected(self):
        limiter = Limiter(FakeClock())
        for _ in range(5):
            limiter.check("alice")
        with self.assertRaises(RateLimited):
            limiter.check("alice")


class Allowlist(unittest.TestCase):
    def test_allowlisted_client_is_accepted(self):
        limiter = Limiter(FakeClock())
        for _ in range(LIMIT):
            limiter.check("internal-service")
