from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User, UserRole
from sqlalchemy.future import select
from schemas.user import UserCreate
from core.utils import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    # user = result.scalars().first()
    user = result.scalar_one_or_none()
    return user


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = user.model_dump()
    user_data["password"] = hashed_password

    db_user = User(**user_data)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


