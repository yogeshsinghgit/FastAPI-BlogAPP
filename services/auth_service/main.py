from fastapi import FastAPI # type: ignore
from contextlib import asynccontextmanager
from core.config import get_settings
from db.database import Base, engine
from routes.auth_route import auth_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # create table if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    yield # continue the app running


app = FastAPI(
              title=settings.APP_NAME, 
              version=settings.APP_VERSION, 
              description=settings.APP_DESCRIPTION,
              lifespan=lifespan
              )


# Just Checking Routes
@app.get("/", tags=['Index Page'])
async def read_root():
    return {"Checking Route": "Working Fine", "Status": "OK"}

# checking config/env file is loaded or not
@app.get("/about", tags=['About Page'])
async def read_about():
    return {"App Name": settings.APP_NAME, 
            "App Desciption":settings.APP_DESCRIPTION,
            "App Version": settings.APP_VERSION}

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
