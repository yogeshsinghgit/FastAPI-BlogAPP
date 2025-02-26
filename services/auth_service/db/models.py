from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLAEnum, func
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import uuid, enum

# class UserRole(Enum):
#     ADMIN = "ADMIN"    # Full access
#     USER = "USER"      # Can read/comment/like/dislike
#     AUTHOR = "AUTHOR"  # Can write/edit/delete own blogs
#     GUEST = "GUEST"    # Read-only access for a limited time

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    author = "author"
    guest = "guest"


# Explicitly declare the ENUM type in PostgreSQL
user_role_enum = SQLAEnum(UserRole, name="user_role_enum", create_type=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(user_role_enum, default=UserRole.guest, nullable=False)
    password = Column(String, nullable=True)  # Now password can be NULL for OAuth users
    is_oauth_user = Column(Boolean, default=False)  # Flag to check if user signed up with OAuth
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, is_oauth_user={self.is_oauth_user})>"

    def __str__(self):
        return f"User {self.name} ({self.email})"
