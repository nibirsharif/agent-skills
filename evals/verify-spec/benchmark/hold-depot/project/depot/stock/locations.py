"""Where items are shelved. A location is aisle-bay-shelf, such as A-03-2."""


class BadLocation(ValueError):
    pass


def parse(location):
    parts = location.split("-")
    if len(parts) != 3 or not parts[0].isalpha() or not (parts[1].isdigit() and parts[2].isdigit()):
        raise BadLocation(location)
    return parts[0].upper(), int(parts[1]), int(parts[2])


def shelve(depot, sku, location):
    aisle, bay, shelf = parse(location)
    item = depot.store.item(sku)
    item.location = f"{aisle}-{bay:02d}-{shelf}"
    return item


def in_aisle(depot, aisle):
    return [item for item in depot.store.items() if item.location.startswith(aisle.upper() + "-")]
