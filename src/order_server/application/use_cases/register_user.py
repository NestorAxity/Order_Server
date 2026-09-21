from fastapi import HTTPException, status

from order_server.domain.entities.user import User
from order_server.domain.ports.user_repository import UserRepositoryPort
from order_server.infrastructure.security.pwd_context import get_password_hash


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(
        self, email: str, password_raw: str, full_name: str | None = None
    ) -> User:
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado",
            )

        hashed_password = get_password_hash(password_raw)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
        )
        return self.user_repo.save(new_user)
