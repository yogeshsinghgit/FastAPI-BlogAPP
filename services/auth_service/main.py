from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import connect_db, close_db
from core.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Set up MongoDB connection on startup and close it on shutdown."""
    await connect_db()
    try:
        yield
    finally:
        await close_db()

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

# app.include_router(auth_route, prefix="/auth")
