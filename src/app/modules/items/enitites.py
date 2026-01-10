from dataclasses import dataclass

from modules.common.enitites import Entity
from modules.common.values import Money
from modules.items.values import ItemDescription, ItemName


@dataclass
class Item(Entity):
    name: ItemName
    description: ItemDescription
    price: Money
