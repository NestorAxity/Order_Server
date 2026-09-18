from typing import cast

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

# Contexto de hashing de contraseñas configurado con bcrypt
password_hash = PasswordHash((BcryptHasher(),))


def get_password_hash(password: str) -> str:
    return cast(str, password_hash.hash(password))
