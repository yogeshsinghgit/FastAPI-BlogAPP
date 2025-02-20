from pydantic import BaseModel, EmailStr, Field 
from typing import Optional, Literal
from datetime import datetime, date
from enum import Enum


# Enum for Gender
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    others = "others"


class RoleEnum(str, Enum):
    admin = "admin"
    author = 'author'
    reader = 'reader'


# User Model
## Stores user creation/registration information (email, username, password, is_active, etc.)
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: RoleEnum = RoleEnum.reader
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str



class UserResponse(UserBase):
    pass


# User Profile Model
## Stores user profile information (Bio, Profile Picture, etc.)
class UserProfile(BaseModel):
    user_id: str  # User ID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
    profile_picture: Optional[str] = None

    class Config:
        orm_mode = True



# Tokem Model/Schema
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: Literal["bearer"] = "bearer"  # Ensures only "bearer" is allowed
