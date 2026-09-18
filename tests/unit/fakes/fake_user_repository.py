from typing import Optional

from order_server.domain.entities.user import User
from order_server.domain.ports.user_repository import UserRepositoryPort


class FakeUserRepository(UserRepositoryPort):

    def __init__(self) -> None:
        self.users: dict[str, User] = {}
        self._next_id = 1

    def get_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email)

    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self.users[user.email] = user
        return user