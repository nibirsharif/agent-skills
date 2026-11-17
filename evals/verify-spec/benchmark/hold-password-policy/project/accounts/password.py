"""The rules a new password must pass."""

MIN_LENGTH = 8
COMMON = {"password1234", "qwertyuiop12", "letmein12345"}


def problems(password):
    """The reasons password is rejected; an empty list when it is accepted."""
    found = []
    if len(password) < MIN_LENGTH:
        found.append("too short")
    if not any(c.isdigit() for c in password):
        found.append("needs a digit")
    if password.lower() in COMMON:
        found.append("too common")
    return found
