from dataclasses import dataclass

from modules.common.exceptions import DomainTypeException
from modules.common.values import ValueObject


@dataclass(frozen=True, slots=True)
class Quantity(ValueObject):
    value: int

    def _validate(self) -> None:
        if self.value <= 0:
            raise DomainTypeException("Количество не может быть отрицательным или равно 0")
