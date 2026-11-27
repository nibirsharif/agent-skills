"""The records the depot keeps. Quantities are in units unless a name says otherwise."""

import dataclasses
import decimal


@dataclasses.dataclass(frozen=True)
class Supplier:
    name: str
    endpoint: str
    pack_size: int = 1


@dataclasses.dataclass
class Item:
    sku: str
    name: str
    supplier: Supplier
    stock: int = 0
    floor: int = 0
    batch: int = 0
    unit_cost: decimal.Decimal = decimal.Decimal("0.00")
    location: str = ""
    discontinued: bool = False


@dataclasses.dataclass
class Order:
    id: int
    sku: str
    supplier: Supplier
    qty: int
    status: str = "draft"
    sent_at: object = None
    received_at: object = None
    overdue: bool = False
    note: str = ""


@dataclasses.dataclass(frozen=True)
class Move:
    sku: str
    delta: int
    reason: str
    at: object
