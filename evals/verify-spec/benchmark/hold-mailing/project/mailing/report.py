"""What the sender sees after a campaign."""


def after_send(campaigns, subject, body):
    result = campaigns.send(subject, body)
    lines = [f"{subject}: {result.sent} sent"]
    if result.bounced:
        lines.append(f"{len(result.bounced)} bounced: {', '.join(result.bounced)}")
    return "\n".join(lines) + "\n"
