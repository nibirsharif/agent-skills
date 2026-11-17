import unittest

from accounts.password import problems


class Length(unittest.TestCase):
    def test_short_password_is_rejected(self):
        self.assertIn("too short", problems("ab12"))

    def test_long_password_is_accepted(self):
        self.assertEqual(problems("correct horse 42 battery"), [])


class Digit(unittest.TestCase):
    def test_password_without_digit_is_rejected(self):
        self.assertIn("needs a digit", problems("correct horse battery"))


class Reuse(unittest.TestCase):
    def test_reused_password_is_rejected(self):
        old = "spring"
        self.assertTrue(problems(old))
