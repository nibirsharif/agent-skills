"""Checks and the stored form of an email address."""


class InvalidAddress(ValueError):
    pass


def validate(address):
    if "@" not in address or address.startswith("@") or address.endswith("@"):
        raise InvalidAddress(address)


def normalize(address):
    """The form addresses are compared in: no surrounding spaces, lower case."""
    return address.strip().lower()
