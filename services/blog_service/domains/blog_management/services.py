from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import Depends, HTTPException
from db.database import get_db
from domains.blog_management.models import Blog, BlogCategory, BlogTag
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from .schema import BlogCreate, BlogUpdate  # Assuming these are in `schemas.py`


class BlogService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    #  Get All Blogs
    async def get_blogs(self):
        result = await self.db.execute(
            select(Blog).options(selectinload(Blog.category), selectinload(Blog.tags))
        )
        return result.scalars().all()
    
    # Get Blog by ID
    async def get_blog_by_id(self, blog_id: UUID):
        result = await self.db.execute(
            select(Blog).options(selectinload(Blog.category), selectinload(Blog.tags)).where(Blog.id == blog_id)
        )
        blog = result.scalars().first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog
    
    # Create a Blog
    async def create_blog(self, blog_data: BlogCreate):
        # Get Category by Name
        category_result = await self.db.execute(
            select(BlogCategory).where(BlogCategory.name == blog_data.category)
        )
        category = category_result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")

        # Get Existing Tags or Create New Ones
        existing_tags_result = await self.db.execute(
            select(BlogTag).where(BlogTag.name.in_(blog_data.tags))
        )
        existing_tags = {tag.name: tag for tag in existing_tags_result.scalars().all()}

        new_tags = []
        for tag_name in blog_data.tags:
            if tag_name not in existing_tags:
                new_tag = BlogTag(name=tag_name)
                self.db.add(new_tag)
                new_tags.append(new_tag)

        await self.db.commit()  # Commit new tags first

        all_tags = list(existing_tags.values()) + new_tags

        # Create Blog
        new_blog = Blog(
            title=blog_data.title,
            slug=blog_data.slug,
            content=blog_data.content,
            author=blog_data.author,
            author_id=UUID(blog_data.author_id),
            status=blog_data.status,
            comments_enabled=blog_data.comments_enabled,
            category=category,
            tags=all_tags
        )

        self.db.add(new_blog)
        await self.db.commit()
        await self.db.refresh(new_blog)
        return new_blog

    # Update a Blog
    async def update_blog(self, blog_id: UUID, blog_data: BlogUpdate):
        blog = await self.get_blog_by_id(blog_id)

        if blog_data.title:
            blog.title = blog_data.title
        if blog_data.slug:
            blog.slug = blog_data.slug
        if blog_data.content:
            blog.content = blog_data.content
        if blog_data.status:
            blog.status = blog_data.status
        if blog_data.comments_enabled is not None:
            blog.comments_enabled = blog_data.comments_enabled

        # Update Category if provided
        if blog_data.category:
            category_result = await self.db.execute(
                select(BlogCategory).where(BlogCategory.name == blog_data.category)
            )
            category = category_result.scalar_one_or_none()
            if not category:
                raise HTTPException(status_code=400, detail="Category does not exist")
            blog.category = category

        # Update Tags if provided
        if blog_data.tags:
            existing_tags_result = await self.db.execute(
                select(BlogTag).where(BlogTag.name.in_(blog_data.tags))
            )
            existing_tags = {tag.name: tag for tag in existing_tags_result.scalars().all()}

            new_tags = []
            for tag_name in blog_data.tags:
                if tag_name not in existing_tags:
                    new_tag = BlogTag(name=tag_name)
                    self.db.add(new_tag)
                    new_tags.append(new_tag)

            await self.db.commit()  # Commit new tags before linking

            blog.tags = list(existing_tags.values()) + new_tags

        await self.db.commit()
        await self.db.refresh(blog)
        return blog

    # Delete a Blog
    async def delete_blog(self, blog_id: UUID):
        blog = await self.get_blog_by_id(blog_id)
        await self.db.delete(blog)
        await self.db.commit()
        return {"message": "Blog deleted successfully"}
