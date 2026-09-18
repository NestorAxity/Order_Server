from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from order_server.config.settings import settings

# Contexto de hashing de contraseñas configurado con bcrypt
password_hash = PasswordHash((BcryptHasher(),))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(password_hash.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return str(password_hash.hash(password))


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    """Genera un token JWT firmado."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": now,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return str(encoded_jwt)
