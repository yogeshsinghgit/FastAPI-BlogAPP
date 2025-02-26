from pydantic import BaseModel
from .user import RoleEnum
from typing import Optional, Literal



# Tokem Model/Schema
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: Literal["bearer"] = "bearer"  # Ensures only "bearer" is allowed


class TokenData(BaseModel):
    email: str
    role: RoleEnum = RoleEnum.user
