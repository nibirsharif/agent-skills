import unittest

from mailing import addresses, tokens


class Validate(unittest.TestCase):
    def test_address_without_at_is_invalid(self):
        with self.assertRaises(addresses.InvalidAddress):
            addresses.validate("ada.example.org")

    def test_address_with_at_is_valid(self):
        addresses.validate("ada@example.org")


class Normalize(unittest.TestCase):
    def test_normalize_lowers_and_strips(self):
        self.assertEqual(addresses.normalize("  Ada@Example.ORG "), "ada@example.org")


class Tokens(unittest.TestCase):
    def test_token_names_its_address(self):
        self.assertEqual(tokens.read(tokens.make("ada@example.org")), "ada@example.org")

    def test_bad_token_is_refused(self):
        with self.assertRaises(tokens.BadToken):
            tokens.read("not-hex")
