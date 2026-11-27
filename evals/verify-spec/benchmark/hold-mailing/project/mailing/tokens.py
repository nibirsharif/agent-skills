"""The token in a confirmation or unsubscribe link names the address it was made for."""


class BadToken(ValueError):
    pass


def make(address):
    return address.encode().hex()


def read(token):
    try:
        return bytes.fromhex(token).decode()
    except ValueError as error:
        raise BadToken(token) from error
