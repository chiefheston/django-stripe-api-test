from dataclasses import dataclass

from modules.common.payments.payment_gateway import PaymentGateway
from modules.items.repo import ItemRepository


@dataclass(eq=False)
class BuyItemResponse:
    client_secret: str


@dataclass(eq=False)
class BuyItemUseCase:
    item_repo: ItemRepository
    payment_gateway: PaymentGateway

    def execute(self, item_id: int) -> BuyItemResponse:
        item = self.item_repo.get_by_id(item_id)

        amount = item.price.to_minor_units()
        currency = item.price.currency.value

        client_secret = self.payment_gateway.create_payment(
            amount=amount,
            currency=currency,
        )

        return BuyItemResponse(client_secret=client_secret)
