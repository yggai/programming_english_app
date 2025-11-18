"""API路由汇总"""

from fastapi import APIRouter
from .auth import router as auth_router
from .words import router as words_router

api_router = APIRouter()

# 包含认证路由
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["认证"]
)

# 包含单词路由
api_router.include_router(
    words_router,
    prefix="/words",
    tags=["单词"]
)