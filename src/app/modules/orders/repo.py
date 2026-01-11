from abc import ABC, abstractmethod
from decimal import Decimal

from django.db.models import Prefetch
from modules.common.values import Currency, Money
from modules.items.enitites import Item
from modules.items.values import ItemDescription, ItemName
from modules.orders.enitites import Discount, Order, OrderLine, Tax
from modules.orders.enums import OrderStatus
from modules.orders.models import Order as OrderModel
from modules.orders.models import OrderDiscount as OrderDiscountModel
from modules.orders.models import OrderLine as OrderLineModel
from modules.orders.models import OrderTax as OrderTaxModel
from modules.orders.values import (
    DiscountAmount,
    DiscountName,
    Quantity,
    TaxAmount,
    TaxName,
)


class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: int) -> Order: ...

    @abstractmethod
    def save(self, order: Order) -> None: ...


class DjangoOrmOrderRepository(OrderRepository):
    def get_by_id(self, order_id: int) -> Order:
        order_model = (
            OrderModel.objects.prefetch_related(
                Prefetch(
                    "lines",
                    OrderLineModel.objects.select_related("item"),
                )
            )
            .prefetch_related(
                Prefetch(
                    "tax",
                    OrderTaxModel.objects.select_related("tax"),
                )
            )
            .prefetch_related(
                Prefetch(
                    "discount",
                    OrderDiscountModel.objects.select_related("discount"),
                )
            )
            .get(id=order_id)
        )

        order = Order(
            id=order_model.id,
            status=OrderStatus(order_model.status.lower()),
        )

        if order_model.tax.first():
            order_tax_model = order_model.tax.first()
            tax = Tax(
                name=TaxName(order_tax_model.tax.name),
                amount=TaxAmount(order_tax_model.tax.amount),
            )
            order.apply_tax(tax)

        if order_model.discount.first():
            order_discount_model = order_model.discount.first()
            discount = Discount(
                name=DiscountName(order_discount_model.discount.name),
                amount=DiscountAmount(order_discount_model.discount.amount),
            )
            order.apply_discount(discount)

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
