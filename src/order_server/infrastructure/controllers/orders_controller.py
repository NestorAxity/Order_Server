from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from order_server.application.use_cases.orders.create_order import CreateOrderUseCase
from order_server.application.use_cases.orders.delete_order import DeleteOrderUseCase
from order_server.application.use_cases.orders.get_order import GetOrderUseCase
from order_server.application.use_cases.orders.list_user_orders import (
    ListUserOrdersUseCase,
)
from order_server.application.use_cases.orders.update_order import UpdateOrderUseCase
from order_server.config.database import get_db
from order_server.domain.entities.user import User
from order_server.infrastructure.adapters.order_repository import (
    SQLAlchemyOrderRepository,
)
from order_server.infrastructure.dtos.order_schema import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)
from order_server.infrastructure.security.deps import get_current_user


# Inyectores de dependencias específicos
def get_create_order_uc(db: Session = Depends(get_db)) -> CreateOrderUseCase:
    return CreateOrderUseCase(SQLAlchemyOrderRepository(db))


def get_get_order_uc(db: Session = Depends(get_db)) -> GetOrderUseCase:
    return GetOrderUseCase(SQLAlchemyOrderRepository(db))


def get_list_orders_uc(db: Session = Depends(get_db)) -> ListUserOrdersUseCase:
    return ListUserOrdersUseCase(SQLAlchemyOrderRepository(db))


def get_update_order_uc(db: Session = Depends(get_db)) -> UpdateOrderUseCase:
    return UpdateOrderUseCase(SQLAlchemyOrderRepository(db))


def get_delete_order_uc(db: Session = Depends(get_db)) -> DeleteOrderUseCase:
    return DeleteOrderUseCase(SQLAlchemyOrderRepository(db))


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderCreate, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
    use_case: CreateOrderUseCase = Depends(get_create_order_uc),
) -> Any:
    return use_case.execute(
        item_name=order_in.item_name,
        quantity=order_in.quantity,
        unit_price=order_in.unit_price,
        user_id=current_user.id,  # type: ignore[arg-type]
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    use_case: GetOrderUseCase = Depends(get_get_order_uc),
) -> Any:
    return use_case.execute(order_id=order_id, user_id=current_user.id)  # type: ignore[arg-type]


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    current_user: User = Depends(get_current_user),
    use_case: ListUserOrdersUseCase = Depends(get_list_orders_uc),
) -> Any:
    return use_case.execute(user_id=current_user.id)  # type: ignore[arg-type]


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_in: OrderUpdate,
    current_user: User = Depends(get_current_user),
    use_case: UpdateOrderUseCase = Depends(get_update_order_uc),
) -> Any:
    return use_case.execute(
        order_id=order_id,
        user_id=current_user.id,  # type: ignore[arg-type]
        item_name=order_in.item_name,
        quantity=order_in.quantity,
        unit_price=order_in.unit_price,
        status_val=order_in.status.value if order_in.status else None,
    )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    use_case: DeleteOrderUseCase = Depends(get_delete_order_uc),
) -> None:
    use_case.execute(order_id=order_id, user_id=current_user.id)  # type: ignore[arg-type]
