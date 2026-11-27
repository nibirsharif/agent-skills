"""Hooks by the event they follow."""

HOOKS = []


def on(event):
    def register(hook):
        HOOKS.append((event, hook))
        return hook
    return register
