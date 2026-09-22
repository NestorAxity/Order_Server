from typing import Optional

from sqlalchemy.orm import Session

from order_server.domain.entities.user import User
from order_server.domain.ports.user_repository import UserRepositoryPort
from order_server.infrastructure.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not model:
            return None
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            is_active=model.is_active,
        )

    def save(self, user: User) -> User:
        model = UserModel(
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        user.id = model.id
        return user
