from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderBase(BaseModel):
    item_name: str = Field(min_length=2, max_length=100)
    quantity: int = Field(gt=0, description="La cantidad debe ser mayor a 0")
    unit_price: float = Field(
        gt=0.0, description="El precio unitario debe ser un valor positivo"
    )


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    item_name: str | None = Field(default=None, min_length=2, max_length=100)
    quantity: int | None = Field(default=None, gt=0)
    unit_price: float | None = Field(default=None, gt=0.0)
    status: OrderStatus | None = None


class OrderResponse(OrderBase):
    id: int
    status: OrderStatus
    total_price: float
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
