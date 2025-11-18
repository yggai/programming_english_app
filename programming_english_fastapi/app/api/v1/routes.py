"""
API路由汇总模块
"""

from fastapi import APIRouter
from .words import router as words_router
from .legacy_words import router as legacy_router
from .root import router as root_router

# 创建主路由器
api_router = APIRouter()

# 包含各个子路由
api_router.include_router(root_router)
api_router.include_router(words_router, prefix="/api/v1")
api_router.include_router(legacy_router, prefix="/api")