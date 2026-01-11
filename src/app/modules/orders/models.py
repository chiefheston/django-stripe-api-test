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


class Discount(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=255,
    )
    amount = models.DecimalField(
        verbose_name="Процент скидки",
        max_digits=5,
        decimal_places=2,
    )

    def __str__(self) -> str:
        return f"Скидка {self.name}"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Tax(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=255,
    )
    amount = models.DecimalField(
        verbose_name="Процент налога",
        max_digits=5,
        decimal_places=2,
    )

    def __str__(self) -> str:
        return f"Налог {self.name}"

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"


class OrderDiscount(models.Model):
    order = models.ForeignKey(
        verbose_name="Заказ",
        to="Order",
        related_name="discount",
        on_delete=models.CASCADE,
    )
    discount = models.ForeignKey(
        verbose_name="Скидка",
        to="Discount",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"Скидка на заказ №{self.order.id}"

    class Meta:
        verbose_name = "Скидка заказа"
        verbose_name_plural = "Скидки заказов"


class OrderTax(models.Model):
    order = models.ForeignKey(
        verbose_name="Заказ",
        to="Order",
        related_name="tax",
        on_delete=models.CASCADE,
    )
    tax = models.ForeignKey(
        verbose_name="Скидка",
        to="Tax",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"Налог на заказ №{self.order.id}"

    class Meta:
        verbose_name = "Налог заказа"
        verbose_name_plural = "Налоги заказов"
