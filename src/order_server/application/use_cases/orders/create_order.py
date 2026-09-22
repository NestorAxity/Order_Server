from order_server.domain.entities.order import Order
from order_server.domain.ports.order_repository import OrderRepositoryPort


class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepositoryPort) -> None:
        self.order_repo = order_repo

    def execute(
        self, item_name: str, quantity: int, unit_price: float, user_id: int
    ) -> Order:
        order = Order(
            item_name=item_name,
            quantity=quantity,
            unit_price=unit_price,
            user_id=user_id,
        )
        return self.order_repo.save(order)
