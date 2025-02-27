from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Text, func, Enum as SQLAEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  # Import PostgreSQL's UUID type
from db.database import Base
from uuid import uuid4
from enum import Enum



# Many-to-Many association table for Blog <-> Tag
if "blog_tags" not in Base.metadata.tables:
    blog_tags_association = Table(
        "blog_tags_association",
        Base.metadata,
        Column("blog_id", UUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True),
        Column("tag_id", UUID(as_uuid=True), ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True),
        extend_existing=True,
    )

# # Many-to-Many association table for Blog <-> Tag
# blog_tags_association = Table(
#     "blog_tags",
#     Base.metadata,
#     Column("blog_id", UUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True),
#     Column("tag_id", UUID(as_uuid=True), ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True),
#     extend_existing=True,  
# )



class BlogStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class BlogCategory(Base):
    __tablename__ = "blog_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    # Relationship: A category has multiple blogs
    blogs = relationship("Blog", back_populates="category", cascade="all, delete-orphan")


class BlogTag(Base):
    __tablename__ = "blog_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    # Many-to-Many relationship with Blog
    blogs = relationship("Blog", secondary=blog_tags_association, back_populates="tags")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    title = Column(String, nullable=False, unique=True)  # Titles should be unique
    slug = Column(String, nullable=False, unique=True)   # Ensure unique slugs
    content = Column(Text, nullable=False)

    author = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)  # Only store the user ID
    
    status = Column(SQLAEnum(BlogStatus, name="blog_status_enum"), default=BlogStatus.draft, nullable=False)  # Assign default status
    comments_enabled = Column(Boolean, default=True)  # Allow/disallow comments

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Foreign Key to Category
    category_id = Column(UUID(as_uuid=True), ForeignKey("blog_categories.id"), nullable=True)

    # Relationships
    category = relationship("BlogCategory", back_populates="blogs")  # One-to-Many
    tags = relationship("BlogTag", secondary=blog_tags_association, back_populates="blogs")  # Many-to-Many

    def __repr__(self):
        return f"<Blog {self.title}>"
    
    def __str__(self):
        return f"{self.title}"
