from fastapi import FastAPI
from domains.blog_management.routes import blog_router

app = FastAPI()

app.include_router(blog_router)

