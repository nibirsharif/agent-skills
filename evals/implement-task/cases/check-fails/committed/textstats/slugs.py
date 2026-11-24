"""Slugs for headings."""

import re


def slug(text):
    """A lowercase, hyphen-separated form of text, for use in a URL."""
    if not text.strip():
        raise ValueError("text has nothing to make a slug from")
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
