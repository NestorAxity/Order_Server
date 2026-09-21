from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from order_server.application.use_cases.orders.create_order import (
    CreateOrderUseCase,
)
from order_server.application.use_cases.orders.delete_order import (
    DeleteOrderUseCase,
)
from order_server.application.use_cases.orders.get_order import (
    GetOrderUseCase,
)
from order_server.application.use_cases.orders.list_user_orders import (
    ListUserOrdersUseCase,
)
from order_server.application.use_cases.orders.update_order import (
    UpdateOrderUseCase,
)
from order_server.domain.entities.order import Order, OrderStatus
from tests.unit.fakes.fake_order_repository import FakeOrderRepository


@pytest.fixture
def order_repo() -> FakeOrderRepository:
    """Fixture anotada para evitar el error 'Untyped decorator'."""
    return FakeOrderRepository()


def test_create_order_use_case(order_repo: FakeOrderRepository) -> None:
    use_case = CreateOrderUseCase(order_repo)
    order = use_case.execute(
        item_name="Papitas",
        quantity=2,
        unit_price=16.0,
        user_id=1,
    )

    assert order.id == 1
    assert order.item_name == "Papitas"
    assert order.total_price == 32.0
    assert order.status == OrderStatus.PENDING
    assert order.user_id == 1


def test_get_order_use_case_success(order_repo: FakeOrderRepository) -> None:
    # Setup
    existing_order = Order(
        item_name="Refresco",
        quantity=1,
        unit_price=20.0,
        total_price=20.0,
        status=OrderStatus.PENDING,
        user_id=1,
        created_at=datetime.now(timezone.utc),
    )
    saved_order = order_repo.save(existing_order)

    use_case = GetOrderUseCase(order_repo)
    assert saved_order.id is not None
    result = use_case.execute(order_id=saved_order.id, user_id=1)

    assert result.id == saved_order.id
    assert result.item_name == "Refresco"


def test_get_order_use_case_not_found(order_repo: FakeOrderRepository) -> None:
    use_case = GetOrderUseCase(order_repo)

    with pytest.raises(HTTPException) as exc_info:
        use_case.execute(order_id=999, user_id=1)

    assert exc_info.value.status_code == 404


def test_list_user_orders_use_case(order_repo: FakeOrderRepository) -> None:
    now = datetime.now(timezone.utc)
    order_repo.save(
        Order(
            item_name="A",
            quantity=1,
            unit_price=10.0,
            total_price=10.0,
            status=OrderStatus.PENDING,
            user_id=1,
            created_at=now,
        )
    )
    order_repo.save(
        Order(
            item_name="B",
            quantity=2,
            unit_price=5.0,
            total_price=10.0,
            status=OrderStatus.PENDING,
            user_id=1,
            created_at=now,
        )
    )
    # Orden perteneciente a otro usuario
    order_repo.save(
        Order(
            item_name="C",
            quantity=1,
            unit_price=15.0,
            total_price=15.0,
            status=OrderStatus.PENDING,
            user_id=2,
            created_at=now,
        )
    )

    use_case = ListUserOrdersUseCase(order_repo)
    orders = use_case.execute(user_id=1)

    assert len(orders) == 2
    assert all(o.user_id == 1 for o in orders)


def test_update_order_use_case_recalculates_total(
    order_repo: FakeOrderRepository,
) -> None:
    saved_order = order_repo.save(
        Order(
            item_name="Café",
            quantity=2,
            unit_price=25.0,
            total_price=50.0,
            status=OrderStatus.PENDING,
            user_id=1,
            created_at=datetime.now(timezone.utc),
        )
    )

    use_case = UpdateOrderUseCase(order_repo)
    assert saved_order.id is not None
    updated_order = use_case.execute(
        order_id=saved_order.id,
        user_id=1,
        quantity=4,  # Cambia la cantidad de 2 a 4
        status_val=OrderStatus.COMPLETED,
    )

    assert updated_order.quantity == 4
    assert updated_order.total_price == 100.0  # 4 * 25.0
    assert updated_order.status == OrderStatus.COMPLETED


def test_delete_order_use_case_success(order_repo: FakeOrderRepository) -> None:
    saved_order = order_repo.save(
        Order(
            item_name="Agua",
            quantity=1,
            unit_price=12.0,
            total_price=12.0,
            status=OrderStatus.PENDING,
            user_id=1,
            created_at=datetime.now(timezone.utc),
        )
    )
    assert saved_order.id is not None
    use_case = DeleteOrderUseCase(order_repo)
    use_case.execute(order_id=saved_order.id, user_id=1)

    assert order_repo.get_by_id(saved_order.id, user_id=1) is None


def test_delete_order_use_case_not_found(order_repo: FakeOrderRepository) -> None:
    """Cubre la línea 13 de delete_order.py cuando la orden no existe."""
    use_case = DeleteOrderUseCase(order_repo)

    with pytest.raises(HTTPException) as exc_info:
        use_case.execute(order_id=999, user_id=1)

    assert exc_info.value.status_code == 404
    assert "no existe" in exc_info.value.detail


# --- Cobertura faltante en UpdateOrderUseCase ---


def test_update_order_use_case_not_found(order_repo: FakeOrderRepository) -> None:
    """Cubre la línea 22 de update_order.py cuando la orden no existe."""
    use_case = UpdateOrderUseCase(order_repo)

    with pytest.raises(HTTPException) as exc_info:
        use_case.execute(order_id=999, user_id=1, item_name="Nuevo")

    assert exc_info.value.status_code == 404


def test_update_order_use_case_partial_updates(
    order_repo: FakeOrderRepository,
) -> None:
    """Cubre las ramas de actualización individual de item_name y
    unit_price (líneas 30-39)."""
    saved_order = order_repo.save(
        Order(
            item_name="Tacos",
            quantity=3,
            unit_price=15.0,
            total_price=45.0,
            status=OrderStatus.PENDING,
            user_id=1,
            created_at=datetime.now(timezone.utc),
        )
    )

    use_case = UpdateOrderUseCase(order_repo)
    assert saved_order.id is not None
    # 1. Actualizar solo el nombre del ítem
    updated_1 = use_case.execute(
        order_id=saved_order.id,
        user_id=1,
        item_name="Tacos al Pastor",
    )
    assert updated_1.item_name == "Tacos al Pastor"
    assert updated_1.quantity == 3  # Se mantiene intacto

    # 2. Actualizar solo el precio unitario (recalcula total)
    updated_2 = use_case.execute(
        order_id=saved_order.id,
        user_id=1,
        unit_price=20.0,
    )
    assert updated_2.unit_price == 20.0
    assert updated_2.total_price == 60.0  # 3 * 20.0

    # 3. Actualizar solo el estado pasando Enum o str
    updated_3 = use_case.execute(
        order_id=saved_order.id,
        user_id=1,
        status_val=OrderStatus.CANCELLED,
    )
    assert updated_3.status == OrderStatus.CANCELLED
