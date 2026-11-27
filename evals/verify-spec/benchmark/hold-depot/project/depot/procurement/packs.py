"""Suppliers sell in packs."""


def whole_packs(units, pack_size):
    """How many packs hold at least this many units."""
    return -(-units // pack_size)
