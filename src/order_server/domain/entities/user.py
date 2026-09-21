from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    id: Optional[int] = None
    is_active: bool = True
