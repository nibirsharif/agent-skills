"""Word counts and reading time."""

import math

DEFAULT_WORDS_PER_MINUTE = 200


def word_count(text):
    """The number of whitespace-separated words in text."""
    return len(text.split())


def reading_time(text):
    """Whole minutes needed to read text at the default speed, rounded up."""
    return math.ceil(word_count(text) / DEFAULT_WORDS_PER_MINUTE)
