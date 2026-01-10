from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from modules.common.enitites import Entity
from modules.common.enums import Currency
from modules.common.exceptions import DomainException
from modules.common.values import Money
from modules.items.enitites import Item
from modules.orders.enums import OrderStatus
from modules.orders.values import Quantity


@dataclass
class OrderLine(Entity):
    item: Item
    quantity: Quantity

    @property
    def total_price(self) -> Money:
        return self.item.price * self.quantity.value


@dataclass
class Order(Entity):
    status: OrderStatus = OrderStatus.NEW
    lines: List[OrderLine] = field(default_factory=list)

    @property
    def currency(self) -> Currency | None:
        if not self.lines:
            return None
        return self.lines[0].item.price.currency

    @property
    def total_price(self) -> Money | None:
        if not self.currency:
            return None

        total = Money(Decimal("0"), self.currency)

        for line in self.lines:
            total += line.total_price

        return total

    def append_line(self, line: OrderLine) -> None:
        if self.currency and self.currency != line.item.price.currency:
            raise DomainException(
                f"Невозможно добавить {line.item.name.value} — несовпадение валют"
            )

        self.lines.append(line)

    def mark_as_paid(self):
        if self.status == OrderStatus.PAID:
            raise DomainException(f"Невозможно оплатить. Заказ {self.id} уже оплачен")

        self.status = OrderStatus.PAID
