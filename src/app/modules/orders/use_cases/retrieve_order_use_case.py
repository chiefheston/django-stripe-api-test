from dataclasses import dataclass
from decimal import Decimal

from modules.orders.repo import OrderRepository


@dataclass(eq=False)
class RetrieveOrderResponse:
    id: int
    lines: list
    price: Decimal
    currency: str


@dataclass(eq=False)
class RetrieveOrderUseCase:
    order_repo: OrderRepository

    def execute(self, order_id: int) -> RetrieveOrderResponse:
        order = self.order_repo.get_by_id(order_id)

        return RetrieveOrderResponse(
            id=order.id,
            lines=order.lines,
            price=order.total_price.amount,
            currency=order.total_price.currency,
        )
