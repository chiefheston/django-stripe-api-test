from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from modules.common.enums import Currency
from modules.common.exceptions import DomainTypeException


@dataclass(frozen=True, slots=True)
class ValueObject(ABC):

    def __post_init__(self):
        self._validate()

    @abstractmethod
    def _validate(self): ...


@dataclass(frozen=True, slots=True)
class Money(ValueObject):
    amount: Decimal
    currency: Currency

    def __add__(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, multiplier: int | Decimal) -> "Money":
        return Money(self.amount * multiplier, self.currency)

    def to_minor_units(self) -> int:
        """Перевод суммы в минимальные единицы для Stripe."""
        return int(self.amount * 100)

    def _validate(self) -> None:
        if self.amount < Decimal("0"):
            raise DomainTypeException("Значение не может быть отрицательным")

        rounded = self.amount.quantize(Decimal("0.01"), ROUND_HALF_UP)
        object.__setattr__(self, "amount", rounded)

    def _assert_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise DomainTypeException(f"Несовпадение валют: {self.currency} != {other.currency}")
