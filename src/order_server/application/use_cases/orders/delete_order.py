from fastapi import HTTPException, status

from order_server.domain.ports.order_repository import OrderRepositoryPort


class DeleteOrderUseCase:
    def __init__(self, order_repo: OrderRepositoryPort) -> None:
        self.order_repo = order_repo

    def execute(self, order_id: int, user_id: int) -> None:
        order = self.order_repo.get_by_id(order_id, user_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La orden solicitada no existe o no "
                "tienes permiso para eliminarla",
            )

        self.order_repo.delete(order_id, user_id)
