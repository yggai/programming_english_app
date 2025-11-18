"""
根路径和系统相关API路由
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session
from datetime import datetime

from ...db.database import get_session

router = APIRouter(tags=["root"])


@router.get("/")
async def root():
    """
    根端点 - API欢迎信息
    
    Returns:
        Dict: 包含API基本信息的字典
    """
    return {
        "message": "Welcome to Programming English API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@router.get("/health", tags=["health"])
async def health_check(session: Session = Depends(get_session)):
    """
    健康检查端点
    
    Args:
        session: 数据库会话
        
    Returns:
        Dict: 健康状态信息
    """
    try:
        # 简单的数据库连接测试
        session.execute("SELECT 1")
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "disconnected",
            "error": str(e)
        }