from dataclasses import dataclass

from modules.common.exceptions import ApplicationException
from modules.common.payments.payment_gateway import PaymentGateway
from modules.orders.repo import OrderRepository


@dataclass(eq=False)
class BuyOrderResponse:
    client_secret: str


@dataclass(eq=False)
class BuyOrderUseCase:
    order_repo: OrderRepository
    payment_gateway: PaymentGateway

    def execute(self, item_id: int) -> BuyOrderResponse:
        order = self.order_repo.get_by_id(item_id)

        if order.total == 0:
            raise ApplicationException("Сумма заказа равноа 0")

        amount = order.total.to_minor_units()
        currency = order.currency.value

        client_secret = self.payment_gateway.create_payment(
            amount=amount,
            currency=currency,
        )

        return BuyOrderResponse(client_secret=client_secret)
