from functools import lru_cache

from django.conf import settings
from modules.common.payments.payment_gateway import PaymentGateway
from modules.common.payments.stripe_payment_gateway import StripePaymentGateway
from modules.items.repo import (
    DjangoOrmItemRepository,
    ItemRepository,
)
from modules.items.use_cases.buy_item_use_case import BuyItemUseCase
from modules.items.use_cases.retrieve_item_use_case import RetrieveItemUseCase
from modules.orders.repo import DjangoOrmOrderRepository, OrderRepository
from modules.orders.use_cases.buy_order_use_case import BuyOrderUseCase
from modules.orders.use_cases.retrieve_order_use_case import RetrieveOrderUseCase
from punq import Container


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    def build_stripe_payment_gateway():
        return StripePaymentGateway(api_key=settings.STRIPE_API_KEY)

    # infra
    container.register(
        ItemRepository,
        DjangoOrmItemRepository,
    )
    container.register(
        OrderRepository,
        DjangoOrmOrderRepository,
    )

    container.register(
        PaymentGateway,
        factory=build_stripe_payment_gateway,
    )

    # use cases
    container.register(BuyItemUseCase)
    container.register(RetrieveItemUseCase)
    container.register(BuyOrderUseCase)
    container.register(RetrieveOrderUseCase)

    return container
