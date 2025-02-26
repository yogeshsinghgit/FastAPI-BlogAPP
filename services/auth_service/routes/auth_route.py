# Auth Services
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserResponse
from schemas.token import Token, TokenData
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import create_user, get_user_by_email
from core.auth import authenticate_user, create_access_token, create_refresh_token
from core.config import get_settings
from core.auth import OAuth2EmailRequestForm, get_current_user
settings = get_settings()


auth_router = APIRouter()

## user creation routes
@auth_router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return await create_user(db, user)



@auth_router.post('/login', response_model=Token)
async def login(form_data: OAuth2EmailRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Handles User Login & Token Generation"""
    user = await authenticate_user(email=form_data.email, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    return Token(
        access_token=create_access_token(data={"sub": user.email, "role": user.role}),
        refresh_token=create_refresh_token(data={"sub": user.email, "role": user.role}),
    )


@auth_router.get('/user/me', response_model=UserResponse)
async def get_me(user: dict = Depends(get_current_user)):
    return user

