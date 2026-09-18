# tests/integration/test_order_repository.py
from collections.abc import Generator
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from order_server.config.database import Base
from order_server.domain.entities.order import Order as DomainOrder
from order_server.domain.entities.order import OrderStatus
from order_server.infrastructure.adapters.order_repository import (
    SQLAlchemyOrderRepository,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    yield session
    session.close()


def test_sqlalchemy_order_repository_crud(db_session: Session) -> None:
    repo = SQLAlchemyOrderRepository(db_session)
    now = datetime.now(timezone.utc)

    # 1. Save / Create
    new_order = DomainOrder(
        item_name="Laptop",
        quantity=1,
        unit_price=1200.0,
        total_price=1200.0,
        status=OrderStatus.PENDING,
        user_id=1,
        created_at=now,
    )
    saved_order = repo.save(new_order)
    assert saved_order.id is not None

    # 2. Get by ID
    found_order = repo.get_by_id(saved_order.id, user_id=1)
    assert found_order is not None
    assert found_order.item_name == "Laptop"

    # 3. Get All by User
    user_orders = repo.get_all_by_user(user_id=1)
    assert len(user_orders) == 1

    # 4. Update
    saved_order.item_name = "Laptop Pro"
    updated_order = repo.update(saved_order)
    assert updated_order.item_name == "Laptop Pro"

    # 5. Delete
    repo.delete(saved_order.id, user_id=1)
    assert repo.get_by_id(saved_order.id, user_id=1) is None
