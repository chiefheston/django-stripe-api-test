from django.db import models
from modules.common.enums import Currency


class Item(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=255,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=10,
        decimal_places=2,
    )
    currency = models.CharField(
        max_length=3,
        choices=[(currency.name, currency.value) for currency in Currency],
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
