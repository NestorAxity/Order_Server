from order_server.domain.entities.order import Order
from order_server.domain.ports.order_repository import OrderRepositoryPort


class FakeOrderRepository(OrderRepositoryPort):
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next_id: int = 1

    def save(self, order: Order) -> Order:
        order.id = self._next_id
        self._orders[self._next_id] = order
        self._next_id += 1
        return order

    def get_by_id(self, order_id: int, user_id: int) -> Order | None:
        order = self._orders.get(order_id)
        if order and order.user_id == user_id:
            return order
        return None

    def get_all_by_user(self, user_id: int) -> list[Order]:
        return [order for order in self._orders.values() if order.user_id == user_id]

    def update(self, order: Order) -> Order:
        if order.id is not None and order.id in self._orders:
            self._orders[order.id] = order
        return order

    def delete(self, order_id: int, user_id: int) -> None:
        order = self.get_by_id(order_id, user_id)
        if order and order.id is not None:
            del self._orders[order.id]
