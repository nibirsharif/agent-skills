"""Small text helpers."""

from helpdesk import settings


def shorten(text, limit=settings.SUBJECT_LIMIT):
    """The text on one line, cut at the limit with an ellipsis."""
    line = " ".join(text.split())
    return line if len(line) <= limit else line[: limit - 1] + "…"


def slug(text):
    return "-".join("".join(c if c.isalnum() else " " for c in text.lower()).split())
