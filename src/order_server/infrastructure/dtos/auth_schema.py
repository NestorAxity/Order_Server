from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=100)


# DTO de entrada para registro de usuario (body)
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=64)


# DTO de salida (excluye el password) (response)
class UserResponse(UserBase):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


# DTO para respuesta de autenticación JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# DTO para la carga útil (payload) extraída del Token
class TokenData(BaseModel):
    email: str | None = None
