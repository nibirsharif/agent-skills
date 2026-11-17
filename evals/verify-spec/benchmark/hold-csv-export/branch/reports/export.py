"""Write report rows as CSV text."""

import datetime


def field(value):
    if value is None:
        return ""
    if isinstance(value, datetime.date):
        return value.strftime("%d/%m/%Y")
    return str(value)


def export(columns, rows):
    lines = [",".join(columns)]
    for row in rows:
        lines.append(",".join(field(row.get(c)) for c in columns))
    return "\n".join(lines) + "\n"
