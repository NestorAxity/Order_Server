import pytest
from fastapi import HTTPException

from order_server.application.use_cases.login_user import LoginUserUseCase
from order_server.application.use_cases.register_user import RegisterUserUseCase
from tests.unit.fakes.fake_user_repository import FakeUserRepository


def test_login_user_success() -> None:
    # Arrange
    fake_repo = FakeUserRepository()
    register_uc = RegisterUserUseCase(user_repo=fake_repo)
    login_uc = LoginUserUseCase(user_repo=fake_repo)

    register_uc.execute(
        email="user@example.com",
        password_raw="mypassword123",
    )

    # Act
    token_dto = login_uc.execute(
        email="user@example.com",
        password_raw="mypassword123",
    )

    # Assert
    assert token_dto.access_token is not None
    assert token_dto.token_type == "bearer"


def test_login_user_invalid_password_raises_exception() -> None:
    # Arrange
    fake_repo = FakeUserRepository()
    register_uc = RegisterUserUseCase(user_repo=fake_repo)
    login_uc = LoginUserUseCase(user_repo=fake_repo)

    register_uc.execute(
        email="user@example.com",
        password_raw="mypassword123",
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        login_uc.execute(
            email="user@example.com",
            password_raw="wrongpassword",
        )

    assert exc_info.value.status_code == 401
    assert "Correo electrónico o contraseña incorrectos" in exc_info.value.detail
