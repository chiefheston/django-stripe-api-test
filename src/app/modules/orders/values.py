from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import ClassVar, Final

from modules.common.exceptions import DomainTypeException
from modules.common.values import ValueObject


@dataclass(frozen=True, slots=True)
class Quantity(ValueObject):
    value: int

    def _validate(self) -> None:
        if self.value <= 0:
            raise DomainTypeException("Количество не может быть отрицательным или равно 0")


@dataclass(frozen=True, slots=True)
class DiscountName(ValueObject):
    value: str

    MAX_LEN: ClassVar[Final[int]] = 255

    def _validate(self) -> None:
        if len(self.value) > self.MAX_LEN:
            raise DomainTypeException(
                f"Названиие скидки не может превышать {self.MAX_LEN} символов: {self.value[:self.MAX_LEN]}"
            )


@dataclass(frozen=True, slots=True)
class DiscountAmount(ValueObject):
    value: Decimal

    def _validate(self) -> None:
        if Decimal("100") < self.value <= Decimal("0"):
            raise DomainTypeException("Неправильно указана скидка")

        rounded = self.value.quantize(Decimal("0.01"), ROUND_HALF_UP)
        object.__setattr__(self, "value", rounded)


@dataclass(frozen=True, slots=True)
class TaxName(ValueObject):
    value: str

    MAX_LEN: ClassVar[Final[int]] = 255

    def _validate(self) -> None:
        if len(self.value) > self.MAX_LEN:
            raise DomainTypeException(
                f"Названиие налога не может превышать {self.MAX_LEN} символов: {self.value[:self.MAX_LEN]}"
            )


@dataclass(frozen=True, slots=True)
class TaxAmount(ValueObject):
    value: Decimal

    def _validate(self) -> None:
        if Decimal("100") < self.value <= Decimal("0"):
            raise DomainTypeException("Неправильно указан налог")

        rounded = self.value.quantize(Decimal("0.01"), ROUND_HALF_UP)
        object.__setattr__(self, "value", rounded)
