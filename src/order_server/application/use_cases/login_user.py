from fastapi import HTTPException, status

from order_server.domain.ports.user_repository import UserRepositoryPort
from order_server.infrastructure.dtos.auth_schema import Token
from order_server.infrastructure.security.pwd_context import (
    create_access_token,
    verify_password,
)


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort) -> None:
        self.user_repo = user_repo

    def execute(self, email: str, password_raw: str) -> Token:
        # 1. Obtener usuario del repositorio
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password_raw, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo electrónico o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 2. Validar que la cuenta esté activa
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo en el sistema",
            )

        # 3. Generar Token JWT
        access_token = create_access_token(subject=user.email)
        return Token(access_token=access_token, token_type="bearer")
