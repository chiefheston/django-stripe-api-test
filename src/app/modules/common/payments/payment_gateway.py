from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict


@dataclass
class PaymentGateway(ABC):
    @abstractmethod
    def create_payment(
        self,
        amount: int,
        currency: str,
        metadata: Dict[str, str] | None = None,
    ) -> str: ...
