"""FastAPI应用创建模块"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .config import config
from .exception_handlers import setup_exception_handlers


def create_app() -> FastAPI:
    """创建FastAPI应用实例"""
    
    # 创建应用
    app = FastAPI(
        title=config.get('app.name', 'Programming English API'),
        version=config.get('app.version', '1.0.0'),
        description=config.get('app.description', 'A FastAPI application'),
        debug=config.get('app.debug', False)
    )
    
    # 配置CORS
    cors_config = config.get('cors', {})
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_config.get('allow_origins', ["*"]),
        allow_credentials=cors_config.get('allow_credentials', True),
        allow_methods=cors_config.get('allow_methods', ["*"]),
        allow_headers=cors_config.get('allow_headers', ["*"])
    )
    
    # 设置异常处理器
    setup_exception_handlers(app)
    
    logger.info("FastAPI应用创建完成")
    
    return app