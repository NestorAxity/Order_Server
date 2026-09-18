from abc import ABC, abstractmethod
from typing import Optional

from order_server.domain.entities.order import Order


class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int, user_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def get_all_by_user(self, user_id: int) -> list[Order]:
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    def delete(self, order_id: int, user_id: int) -> None:
        pass
