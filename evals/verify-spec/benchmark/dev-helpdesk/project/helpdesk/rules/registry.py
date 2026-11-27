"""The rules the engine runs. A rule takes (desk, ticket) and returns whether it acted."""

RULES = []


def rule(name):
    def register(check):
        RULES.append((name, check))
        return check
    return register
