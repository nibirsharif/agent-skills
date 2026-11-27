"""What runs every night: the day's drafts go out, and the buyer gets the numbers."""

from depot.procurement.send import send_drafts
from depot.reports import overdue, valuation


def run(depot, transport):
    sent = send_drafts(depot, transport)
    return [f"{len(sent)} orders sent", valuation.line(depot), *overdue.lines(depot)]
