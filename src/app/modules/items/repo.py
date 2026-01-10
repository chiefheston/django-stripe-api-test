from abc import ABC, abstractmethod
from decimal import Decimal

from modules.common.enums import Currency
from modules.common.values import Money
from modules.items.enitites import Item
from modules.items.models import Item as ItemModel
from modules.items.values import ItemDescription, ItemName


class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, item_id: int) -> Item: ...

    def save(self, item: Item) -> None: ...


class DjangoOrmItemRepository(ItemRepository):
    def get_by_id(self, item_id: int) -> Item:
        item_model = ItemModel.objects.get(id=item_id)

        item_id = item_model.id  # type: ignore
        item_name = ItemName(item_model.name)
        item_description = ItemDescription(item_model.description)
        item_price = Money(Decimal(item_model.price), Currency(item_model.currency.lower()))

        item = Item(
            id=item_id,
            name=item_name,
            description=item_description,
            price=item_price,
        )

        return item

    def save(self, item: Item) -> None:
        item_model_id = item.id
        item_model_name = item.name.value
        item_model_description = item.description.value
        item_model_price = item.price.amount
        item_model_currency = item.price.currency

        ItemModel.objects.update_or_create(
            id=item_model_id,
            defaults={
                "name": item_model_name,
                "description": item_model_description,
                "price": item_model_price,
                "currency": item_model_currency,
            },
        )


class FakeItemRepository(ItemRepository):

    db = {}

    def get_by_id(self, item_id: int) -> Item:
        item_name = ItemName("Тестовый товар")
        item_description = ItemDescription("Описание для тестового товара")
        item_price = Money(Decimal(100), Currency.USD)

        return Item(
            id=item_id,
            name=item_name,
            description=item_description,
            price=item_price,
        )

    def save(self, item: Item) -> None:
        self.db[item.id] = item
        return None
