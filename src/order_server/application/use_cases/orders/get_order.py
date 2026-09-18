from fastapi import HTTPException, status

from order_server.domain.entities.order import Order
from order_server.domain.ports.order_repository import OrderRepositoryPort


class GetOrderUseCase:
    def __init__(self, order_repo: OrderRepositoryPort) -> None:
        self.order_repo = order_repo

    def execute(self, order_id: int, user_id: int) -> Order:
        order = self.order_repo.get_by_id(order_id, user_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La orden solicitada no existe o no tienes acceso a ella",
            )
        return order
