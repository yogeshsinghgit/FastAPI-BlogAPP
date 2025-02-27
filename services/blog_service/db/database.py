from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql+asyncpg://postgres:software@localhost/BlogHubBlogsdb" # BlogHubBlogsdb


Base = declarative_base()

from domains.blog_management.models import Blog, BlogCategory, BlogTag

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db  





