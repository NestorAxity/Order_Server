import pytest
from fastapi import HTTPException

from order_server.application.use_cases.register_user import RegisterUserUseCase
from tests.unit.fakes.fake_user_repository import FakeUserRepository


def test_register_user_success() -> None:
    # Arrange
    fake_repo = FakeUserRepository()
    use_case = RegisterUserUseCase(user_repo=fake_repo)

    # Act
    created_user = use_case.execute(
        email="test@example.com",
        password_raw="securepassword123",
        full_name="John Doe",
    )

    # Assert
    assert created_user.id is not None
    assert created_user.email == "test@example.com"
    assert created_user.full_name == "John Doe"
    assert created_user.hashed_password != "securepassword123"  # Debe estar encriptado


def test_register_user_duplicate_email_raises_exception() -> None:
    # Arrange
    fake_repo = FakeUserRepository()
    use_case = RegisterUserUseCase(user_repo=fake_repo)

    use_case.execute(
        email="duplicate@example.com",
        password_raw="password123",
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        use_case.execute(
            email="duplicate@example.com",
            password_raw="password123",
        )

    assert exc_info.value.status_code == 400
    assert "correo electrónico ya se encuentra registrado" in exc_info.value.detail