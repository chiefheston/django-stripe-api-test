from django.db import models
from modules.orders.enums import OrderStatus


class Order(models.Model):
    status = models.CharField(
        verbose_name="Статус",
        choices=[(status.name, status.value) for status in OrderStatus],
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания заказа",
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f"Заказ №{self.id} от {self.created_at}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderLine(models.Model):
    order = models.ForeignKey(
        verbose_name="Заказ",
        to="Order",
        related_name="lines",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        verbose_name="Товар",
        to="items.Item",
        on_delete=models.PROTECT,
    )
    quantity = models.IntegerField(
        verbose_name="Количество",
    )

    def __str__(self) -> str:
        return f"Позиция заказа №{self.order.id}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"
