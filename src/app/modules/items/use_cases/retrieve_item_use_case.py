from dataclasses import dataclass
from decimal import Decimal

from modules.items.repo import ItemRepository


@dataclass(eq=False)
class RetrieveItemResponse:
    id: int
    name: str
    description: str
    price: Decimal
    currency: str


@dataclass(eq=False)
class RetrieveItemUseCase:
    item_repo: ItemRepository

    def execute(self, item_id: int) -> RetrieveItemResponse:
        item = self.item_repo.get_by_id(item_id)

        return RetrieveItemResponse(
            id=item.id,
            name=item.name.value,
            description=item.description.value,
            price=item.price.amount,
            currency=item.price.currency,
        )
