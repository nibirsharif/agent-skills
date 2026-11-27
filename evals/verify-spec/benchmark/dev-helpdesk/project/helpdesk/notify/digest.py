"""The morning mail to each team lead: the team's open tickets."""

from helpdesk import settings
from helpdesk.util.dates import age_in_words


def send_digests(desk):
    """Mails one digest per lead. Returns how many were sent; none outside the digest hour."""
    now = desk.clock.now()
    if now.hour != settings.DIGEST_HOUR:
        return 0
    by_lead = {}
    for ticket in desk.store.open():
        by_lead.setdefault(ticket.team.lead, []).append(ticket)
    for lead, tickets in by_lead.items():
        lines = [f"#{t.id} {t.subject} ({age_in_words(now - t.created_at)})" for t in tickets]
        desk.outbox.send(lead.email, f"{len(tickets)} open tickets", "\n".join(lines))
    return len(by_lead)
