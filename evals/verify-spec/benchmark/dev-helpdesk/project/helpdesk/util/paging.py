"""One page of a list."""


def page(items, number, size):
    start = (max(number, 1) - 1) * size
    return items[start:start + size]


def pages(items, size):
    return max(1, -(-len(items) // size))
