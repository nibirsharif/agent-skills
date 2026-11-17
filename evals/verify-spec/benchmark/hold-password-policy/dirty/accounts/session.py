"""Session tokens."""

import secrets

LIFETIME_SECONDS = 3600


def new_token():
    return secrets.token_urlsafe(32)


def expired(issued_at, now):
    return now - issued_at >= LIFETIME_SECONDS
