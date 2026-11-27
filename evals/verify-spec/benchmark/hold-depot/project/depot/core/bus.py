"""A small in-process event bus. A handler gets the event's fields as keyword arguments."""


class Bus:
    def __init__(self):
        self._handlers = {}

    def on(self, name, handler):
        self._handlers.setdefault(name, []).append(handler)

    def publish(self, name, **fields):
        for handler in self._handlers.get(name, []):
            handler(**fields)
