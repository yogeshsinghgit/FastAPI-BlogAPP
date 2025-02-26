
from core.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


settings = get_settings()

Base = declarative_base()

from db.models import User


DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db  
