"""Runs every rule over every open ticket. A scheduler calls run once a minute."""

from helpdesk.rules import builtin  # noqa: F401  (importing it registers the rules)
from helpdesk.rules.registry import RULES


def run(desk):
    """Returns the (rule name, ticket ID) pairs that acted."""
    acted = []
    for ticket in desk.store.open():
        for name, check in RULES:
            if check(desk, ticket):
                acted.append((name, ticket.id))
    return acted
