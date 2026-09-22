from abc import ABC, abstractmethod
from typing import Optional

from order_server.domain.entities.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass
