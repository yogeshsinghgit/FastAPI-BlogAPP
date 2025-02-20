from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import get_settings

settings = get_settings()

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

async def connect_db():
    """Initialize MongoDB connection."""
    global client, db
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.DATABASE_NAME]

async def close_db():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()

async def get_db() -> AsyncIOMotorDatabase:
    """Dependency function to get the database."""
    return db
