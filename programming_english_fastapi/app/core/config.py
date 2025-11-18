"""
应用启动配置模块
"""

import uvicorn
from typing import Optional

from .settings import settings


def get_uvicorn_config(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = True,
    workers: Optional[int] = None
) -> dict:
    """
    获取Uvicorn配置
    
    Args:
        host: 服务器主机地址
        port: 服务器端口
        reload: 是否启用热重载
        workers: 工作进程数量
        
    Returns:
        dict: Uvicorn配置字典
    """
    config = {
        "host": host,
        "port": port,
        "reload": reload and settings.environment == "development",
        "log_level": "info" if settings.environment == "production" else "debug",
    }
    
    if workers:
        config["workers"] = workers
        
    return config


def run_server():
    """启动服务器"""
    config = get_uvicorn_config()
    uvicorn.run("app.main:app", **config)