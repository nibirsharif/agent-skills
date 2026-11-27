"""What the depot does by itself when something happens."""

from depot.hooks import after_move  # noqa: F401  (importing it registers its hooks)
from depot.hooks.registry import HOOKS


def attach(depot):
    for event, hook in HOOKS:
        depot.bus.on(event, hook)
