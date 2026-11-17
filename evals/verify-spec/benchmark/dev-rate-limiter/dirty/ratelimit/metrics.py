"""Counters for a dashboard."""

accepted = 0
rejected = 0


def record(was_accepted):
    global accepted, rejected
    if was_accepted:
        accepted += 1
    else:
        rejected += 1
