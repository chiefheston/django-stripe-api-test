from dataclasses import dataclass
from typing import ClassVar, Final

from modules.common.exceptions import DomainTypeException
from modules.common.values import ValueObject


@dataclass(frozen=True, slots=True)
class ItemName(ValueObject):
    value: str

    MAX_LEN: ClassVar[Final[int]] = 255

    def _validate(self) -> None:
        if len(self.value) > self.MAX_LEN:
            raise DomainTypeException(
                f"Названиие товара не может превышать {self.MAX_LEN} символов: {self.value[:self.MAX_LEN]}"
            )


@dataclass(frozen=True, slots=True)
class ItemDescription(ValueObject):
    value: str

    MAX_LEN: ClassVar[Final[int]] = 255

    def _validate(self) -> None:
        if len(self.value) > self.MAX_LEN:
            raise DomainTypeException(
                f"Описание товара не может превышать {self.MAX_LEN} символов: {self.value[:self.MAX_LEN]}"
            )
