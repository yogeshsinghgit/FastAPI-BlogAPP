from fastapi import APIRouter, Depends
from common.dependency import get_authenticated_user, require_role

blog_router = APIRouter(prefix="/blog", tags=["blog"])

@blog_router.get("/")
async def get_blogs(user=Depends(get_authenticated_user)):
    return {
        "message": "Hello, World!",
        "user": user,
    }


@blog_router.get("/author")
async def author_only(
    user = Depends(require_role(["author"]))  # Only AUTHOR can access this route
):
    return {"message": "Hello, Author!",
            "user": user}

