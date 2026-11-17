"""Write report rows as CSV text."""


def export(columns, rows):
    lines = [",".join(columns)]
    for row in rows:
        lines.append(",".join(str(row.get(c)) for c in columns))
    return "\n".join(lines) + "\n"
