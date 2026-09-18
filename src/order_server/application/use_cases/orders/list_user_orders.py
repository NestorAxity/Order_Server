from order_server.domain.entities.order import Order
from order_server.domain.ports.order_repository import OrderRepositoryPort


class ListUserOrdersUseCase:
    def __init__(self, order_repo: OrderRepositoryPort) -> None:
        self.order_repo = order_repo

    def execute(self, user_id: int) -> list[Order]:
        return self.order_repo.get_all_by_user(user_id)
