"""Tasks with due dates. A task is a dict: title, due (a date or None), done."""

import datetime


def parse_due(value):
    """The date value names, or None when it is not YYYY-MM-DD."""
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def add(tasks, title, due=None):
    tasks.append({"title": title, "due": due, "done": False})


def overdue(tasks, today):
    return [t for t in tasks if t["due"] and t["due"] <= today and not t["done"]]


def listing(tasks):
    return sorted(tasks, key=lambda t: (t["due"] is None, t["due"] or datetime.date.min))
