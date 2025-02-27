from fastapi import FastAPI
from db.database import engine, Base
from contextlib import asynccontextmanager
from domains.blog_management.routes import blog_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # create table if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    yield # continue the app running

app = FastAPI(title="BlogHub Blog Service", 
              version="1.0.0",
              description="BlogHub Blog Service",
              lifespan=lifespan)

app.include_router(blog_router)

