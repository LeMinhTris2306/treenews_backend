from API.articleAPI import router as article_router
from API.userAPI import router as user_router
from API.commentAPI import router as comment_router
from API.categoryAPI import router as category_router
from API.authentication import router as authentication_router

__all__ = ["article_router", "user_router", "comment_router", "category_router", "authentication_router"]