"""A small in-process event bus. Handlers are registered by event name and get the event's payload as a dict."""


class Bus:
    def __init__(self):
        self._handlers = {}

    def on(self, name, handler):
        self._handlers.setdefault(name, []).append(handler)

    def publish(self, name, **payload):
        for handler in self._handlers.get(name, []):
            handler(payload)
