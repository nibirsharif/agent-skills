import unittest

from accounts.session import expired, new_token


class Session(unittest.TestCase):
    def test_tokens_differ(self):
        self.assertNotEqual(new_token(), new_token())

    def test_expires_after_an_hour(self):
        self.assertTrue(expired(0, 3600))
        self.assertFalse(expired(0, 3599))
