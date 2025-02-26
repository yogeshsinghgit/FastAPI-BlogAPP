from fastapi import HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import get_settings
from core.crud import get_user_by_email
from core.utils import verify_password
from schemas.token import TokenData
from db.database import get_db

settings = get_settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS






## Since OAuth2PasswordRequestForm doesn't allow changing username to email, 
## the best approach is to create a custom form class.
class OAuth2EmailRequestForm:
    """Custom OAuth2 form to accept 'email' instead of 'username'"""
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password


# Jwt token generation methods
def create_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict):
    return create_token(data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data: dict):
    return create_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


# Jwt token verification methods
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    

async def get_current_user(token:str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email, role=payload.get("role"))

    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_email(db= db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
            

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email=email)
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user




