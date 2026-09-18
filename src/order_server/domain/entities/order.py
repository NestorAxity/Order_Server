from datetime import datetime
from enum import Enum
from typing import Optional


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order:
    def __init__(
        self,
        item_name: str,
        quantity: int,
        unit_price: float,
        user_id: int,
        id: Optional[int] = None,
        status: OrderStatus = OrderStatus.PENDING,
        total_price: Optional[float] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.item_name = item_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.user_id = user_id
        self.status = status
        self.total_price = (
            total_price if total_price is not None else self.calculate_total_price()
        )
        self.created_at = created_at or datetime.now()

    def calculate_total_price(self) -> float:
        return round(self.quantity * self.unit_price, 2)

    def update_details(
        self,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
        status: Optional[OrderStatus] = None,
    ) -> None:
        if item_name is not None:
            self.item_name = item_name
        if quantity is not None:
            self.quantity = quantity
        if unit_price is not None:
            self.unit_price = unit_price
        if status is not None:
            self.status = status

        # Recalcula automáticamente el total al modificar precio o cantidad
        self.total_price = self.calculate_total_price()
