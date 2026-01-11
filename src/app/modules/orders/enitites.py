from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from modules.common.enitites import Entity
from modules.common.enums import Currency
from modules.common.exceptions import DomainException
from modules.common.values import Money
from modules.items.enitites import Item
from modules.orders.enums import OrderStatus
from modules.orders.values import (
    DiscountAmount,
    DiscountName,
    Quantity,
    TaxAmount,
    TaxName,
)


@dataclass
class Discount(Entity):
    name: DiscountName
    amount: DiscountAmount


@dataclass
class Tax(Entity):
    name: TaxName
    amount: TaxAmount


@dataclass
class OrderLine(Entity):
    item: Item
    quantity: Quantity

    @property
    def total(self) -> Money:
        return self.item.price * self.quantity.value


@dataclass
class Order(Entity):
    status: OrderStatus = OrderStatus.NEW
    lines: List[OrderLine] = field(default_factory=list)
    discount: Discount | None = None
    tax: Tax | None = None

    @property
    def currency(self) -> Currency:
        if not self.lines:
            return Currency.USD

        return self.lines[0].item.price.currency

    @property
    def total(self) -> Money:
        return self.subtotal - (self.discount_total + self.tax_total)

    @property
    def subtotal(self) -> Money:
        subtotal = Money(Decimal("0"), self.currency)

        for line in self.lines:
            subtotal += line.total

        return subtotal

    @property
    def discount_total(self) -> Money:
        if not self.discount:
            return Money(Decimal("0"), self.currency)

        return self.subtotal * (self.discount.amount.value / 100)

    @property
    def tax_total(self) -> Money:
        if not self.tax:
            return Money(Decimal("0"), self.currency)

        discounted = self.subtotal - self.discount_total

        return discounted * (self.tax.amount.value / 100)

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

    def apply_discount(self, discount: Discount) -> None:
        self.discount = discount

    def apply_tax(self, tax: Tax) -> None:
        self.tax = tax
