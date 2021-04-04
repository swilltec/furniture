from dataclasses import dataclass
from typing import Optional, NamedTuple, NewType
from collections import namedtuple
from datetime import date


Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)
Line = namedtuple('Line', ['sku', 'qty'])


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Money(NamedTuple):
    currency: str
    value: int


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: Reference, sku: Sku,
                 qty: Quantity, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
           return self.sku == line.sku and self.available_quantity >= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


class Person:
    def __init__(self, name: Name):
        self.name = name


