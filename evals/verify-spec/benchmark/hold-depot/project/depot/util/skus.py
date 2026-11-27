"""Stock-keeping unit codes: three letters, a hyphen, four digits."""


class BadSku(ValueError):
    pass


def check(sku):
    head, _, tail = sku.partition("-")
    if not (len(head) == 3 and head.isalpha() and head.isupper() and len(tail) == 4 and tail.isdigit()):
        raise BadSku(sku)
    return sku
