# Auth Services
from fastapi import APIRouter, Depends, HTTPException, status
from db.models import UserCreate, UserResponse, Token
from db.database import get_db

auth_router = APIRouter()

## user creation routes
@auth_router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate):
    ...


@auth_router.post('/login', response_model=Token)
async def login_user(user_email: str, user_password: str):
    ...



@auth_router.get('/user/me', response_model=UserResponse)
async def get_me():
    ...



# user update routes
@auth_router.put('/user/me', response_model=UserResponse)
async def update_user(user_id: str ,user: dict):
    ...

