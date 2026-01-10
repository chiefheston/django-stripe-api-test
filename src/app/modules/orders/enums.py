from enum import Enum


class OrderStatus(str, Enum):
    NEW = "new"
    PAID = "paid"
