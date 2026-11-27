"""Folding a duplicate ticket into the one that is kept."""

from helpdesk.tickets import status


def merge(desk, keep, duplicate):
    keep.replies.extend(duplicate.replies)
    keep.replies.sort(key=lambda reply: reply.at)
    duplicate.flags.add("merged")
    status.close(desk, duplicate)
    desk.store.save(keep)
    return keep
