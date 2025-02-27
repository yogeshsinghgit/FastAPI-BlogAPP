from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime


# Blog Status Enum
class BlogStatusEnum(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


# BlogCategory Schema (Admin Only)
class BlogCategoryBase(BaseModel):
    name: str


class BlogCategoryResponse(BlogCategoryBase):
    class Config:
        from_attributes = True


# BlogTag Schema (Created by Authors)
class BlogTagBase(BaseModel):
    name: str


class BlogTagCreate(BlogTagBase):
    pass


class BlogTagResponse(BlogTagBase):
    class Config:
        from_attributes = True


# Blog Schema
class BlogBase(BaseModel):
    title: str
    slug: str
    content: str
    author: str
    status: BlogStatusEnum = BlogStatusEnum.draft
    comments_enabled: bool = True
    category: str  # Category name instead of ID
    tags: List[str] = []  # List of tag names instead of IDs


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    status: Optional[BlogStatusEnum] = None
    comments_enabled: Optional[bool] = None
    category: Optional[str] = None  # Updated category name
    tags: Optional[List[str]] = None  # Updated list of tag names


class BlogResponse(BlogBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
