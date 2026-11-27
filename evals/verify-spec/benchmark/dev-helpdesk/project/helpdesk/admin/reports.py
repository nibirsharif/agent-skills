"""Counts for the admin page."""

import collections


def by_status(desk):
    return dict(collections.Counter(ticket.status for ticket in desk.store.all()))


def by_team(desk):
    return dict(collections.Counter(ticket.team.name for ticket in desk.store.open()))


def unassigned(desk):
    return [ticket for ticket in desk.store.open() if ticket.assignee is None]
