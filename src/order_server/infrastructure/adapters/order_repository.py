from typing import Optional

from sqlalchemy.orm import Session

from order_server.domain.entities.order import Order, OrderStatus
from order_server.domain.ports.order_repository import OrderRepositoryPort
from order_server.infrastructure.models.order_model import OrderModel


class SQLAlchemyOrderRepository(OrderRepositoryPort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            item_name=model.item_name,
            quantity=model.quantity,
            unit_price=model.unit_price,
            user_id=model.user_id,
            status=OrderStatus(model.status),
            total_price=model.total_price,
            created_at=model.created_at,
        )

    def save(self, order: Order) -> Order:
        db_order = OrderModel(
            item_name=order.item_name,
            quantity=order.quantity,
            unit_price=order.unit_price,
            total_price=order.total_price,
            status=order.status.value,
            user_id=order.user_id,
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return self._to_entity(db_order)

    def get_by_id(self, order_id: int, user_id: int) -> Optional[Order]:
        db_order = (
            self.db.query(OrderModel)
            .filter(
                OrderModel.id == order_id,
                OrderModel.user_id == user_id,
            )
            .first()
        )
        return self._to_entity(db_order) if db_order else None

    def get_all_by_user(self, user_id: int) -> list[Order]:
        orders = self.db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
        return [self._to_entity(o) for o in orders]

    def update(self, order: Order) -> Order:
        db_order = (
            self.db.query(OrderModel)
            .filter(
                OrderModel.id == order.id,
                OrderModel.user_id == order.user_id,
            )
            .first()
        )
        if db_order:
            db_order.item_name = order.item_name
            db_order.quantity = order.quantity
            db_order.unit_price = order.unit_price
            db_order.total_price = order.total_price
            db_order.status = order.status.value
            self.db.commit()
            self.db.refresh(db_order)
            return self._to_entity(db_order)
        raise ValueError("Orden no encontrada para actualizar")

    def delete(self, order_id: int, user_id: int) -> None:
        db_order = (
            self.db.query(OrderModel)
            .filter(
                OrderModel.id == order_id,
                OrderModel.user_id == user_id,
            )
            .first()
        )
        if db_order:
            self.db.delete(db_order)
            self.db.commit()
