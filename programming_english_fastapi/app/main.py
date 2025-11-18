"""FastAPI应用入口模块"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.core.app import create_app
from app.core.initialization import initialize_application
from app.api.v1.routes import api_router
from app.db.database import create_db_and_tables
from loguru import logger

# 创建应用实例
app = create_app()

# 包含API路由
app.include_router(api_router)

# 创建数据库表并初始化超级用户
create_db_and_tables()
initialize_application()

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件"""
    logger.info("🚀 Programming English API starting up...")
    logger.info("📊 Database URL: sqlite:///./programming_english.db")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件"""
    logger.info("🛑 Programming English API shutting down...")

# 中间件：记录访问日志
@app.middleware("http")
async def log_requests(request, call_next):
    """记录HTTP请求日志"""
    import time
    
    start_time = time.time()
    
    # 记录请求开始
    logger.bind(type="access").info(
        f"→ {request.method} {request.url.path} - {request.client.host}"
    )
    
    # 执行请求
    response = await call_next(request)
    
    # 计算处理时间
    process_time = time.time() - start_time
    
    # 记录请求完成
    logger.bind(type="access").info(
        f"← {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )
    
    return response

if __name__ == "__main__":
    # 设置日志
    import logging
    
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                from loguru import logger
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
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )