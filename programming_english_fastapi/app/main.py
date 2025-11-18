"""FastAPI应用入口模块"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.core.app import create_app
from app.api.v1.routes import api_router
from app.db.database import create_db_and_tables

# 创建应用实例
app = create_app()

# 包含API路由
app.include_router(api_router)

# 创建数据库表
create_db_and_tables()

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件"""
    from loguru import logger
    logger.info("🚀 Programming English API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件"""
    from loguru import logger
    logger.info("🛑 Programming English API shutting down...")

if __name__ == "__main__":
    # 设置日志
    import sys
    from loguru import logger
    
    # 移除默认logger
    logger.remove()
    
    # 控制台日志
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # 普通日志文件
    logger.add(
        "logs/app.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8"
    )
    
    # 错误日志文件
    logger.add(
        "logs/error.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True
    )
    
    # 访问日志文件
    logger.add(
        "logs/access.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        filter=lambda record: record["extra"].get("type") == "access"
    )
    
    # 配置Uvicorn日志
    import logging
    
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
    
    # 配置标准日志到loguru
    logging.getLogger().handlers = [InterceptHandler()]
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("fastapi").handlers = [InterceptHandler()]
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )