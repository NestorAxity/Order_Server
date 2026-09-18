from fastapi import HTTPException, status

from order_server.domain.entities.order import Order, OrderStatus
from order_server.domain.ports.order_repository import OrderRepositoryPort


class UpdateOrderUseCase:
    def __init__(self, order_repo: OrderRepositoryPort) -> None:
        self.order_repo = order_repo

    def execute(
        self,
        order_id: int,
        user_id: int,
        item_name: str | None = None,
        quantity: int | None = None,
        unit_price: float | None = None,
        status_val: str | None = None,
    ) -> Order:
        order = self.order_repo.get_by_id(order_id, user_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La orden solicitada no existe o "
                "no tienes permiso para modificarla",
            )

        # Actualizamos atributos de la entidad si provienen en la petición
        if item_name is not None:
            order.item_name = item_name
        if quantity is not None:
            order.quantity = quantity
        if unit_price is not None:
            order.unit_price = unit_price
        if status_val is not None:
            order.status = OrderStatus(status_val)

        # Recalcular total si varió precio o cantidad
        if quantity is not None or unit_price is not None:
            order.total_price = order.quantity * order.unit_price

        return self.order_repo.update(order)
