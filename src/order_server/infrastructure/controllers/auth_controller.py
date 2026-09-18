from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from order_server.application.use_cases.login_user import LoginUserUseCase
from order_server.application.use_cases.register_user import RegisterUserUseCase
from order_server.config.database import get_db
from order_server.infrastructure.adapters.user_repository import (
    SQLAlchemyUserRepository,
)
from order_server.infrastructure.dtos.auth_schema import (
    Token,
    UserCreate,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    repository = SQLAlchemyUserRepository(db=db)
    use_case = RegisterUserUseCase(user_repo=repository)
    return use_case.execute(
        email=user_in.email,
        password_raw=user_in.password,
        full_name=user_in.full_name,
    )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    repository = SQLAlchemyUserRepository(db=db)
    use_case = LoginUserUseCase(user_repo=repository)
    return use_case.execute(
        email=form_data.username,
        password_raw=form_data.password,
    )
