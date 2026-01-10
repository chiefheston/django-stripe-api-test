from abc import ABC, abstractmethod
from decimal import Decimal

from django.db.models import Prefetch
from modules.common.values import Currency, Money
from modules.items.enitites import Item
from modules.items.values import ItemDescription, ItemName
from modules.orders.enitites import Order, OrderLine
from modules.orders.enums import OrderStatus
from modules.orders.models import Order as OrderModel
from modules.orders.models import OrderLine as OrderLineModel
from modules.orders.values import Quantity


class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: int) -> Order: ...

    @abstractmethod
    def save(self, order: Order) -> None: ...


class DjangoOrmOrderRepository(OrderRepository):
    def get_by_id(self, order_id: int) -> Order:
        order_model = OrderModel.objects.prefetch_related(
            Prefetch(
                "lines",
                OrderLineModel.objects.select_related("item"),
            )
        ).get(id=order_id)

        order = Order(
            id=order_model.id,
            status=OrderStatus(order_model.status.lower()),
        )

        order_lines_model = order_model.lines.all()

        for order_line_model in order_lines_model:
            item_model = order_line_model.item

            item = Item(
                id=item_model.id,
                name=ItemName(item_model.name),
                description=ItemDescription(item_model.description),
                price=Money(
                    Decimal(item_model.price),
                    Currency(item_model.currency.lower()),
                ),
            )

            order_line = OrderLine(
                id=order_line_model.id,
                item=item,
                quantity=Quantity(order_line_model.quantity),
            )

            order.append_line(order_line)

        return order

    def save(self):
        pass
