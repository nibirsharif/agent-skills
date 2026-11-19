"""The tests share the project's cache server, which must be running on 127.0.0.1:6399."""

import socket

try:
    socket.create_connection(("127.0.0.1", 6399), timeout=1).close()
except OSError as error:
    raise RuntimeError(f"cache server at 127.0.0.1:6399 is not reachable: {error}") from error
