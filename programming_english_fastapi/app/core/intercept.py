"""日志拦截器 - 将标准日志重定向到loguru"""

import logging
import sys
from loguru import logger
from pathlib import Path

class InterceptHandler(logging.Handler):
    """标准日志拦截器"""
    
    def emit(self, record):
        """发送日志记录到loguru"""
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


class UvicornLogger:
    """Uvicorn日志配置器"""
    
    @staticmethod
    def setup():
        """设置Uvicorn使用loguru"""
        # 移除所有现有处理器
        logging.getLogger().handlers = []
        logging.getLogger("uvicorn").handlers = []
        logging.getLogger("uvicorn.access").handlers = []
        logging.getLogger("uvicorn.error").handlers = []
        
        # 添加拦截处理器
        intercept_handler = InterceptHandler()
        logging.getLogger().addHandler(intercept_handler)
        logging.getLogger("uvicorn").addHandler(intercept_handler)
        logging.getLogger("uvicorn.access").addHandler(intercept_handler)
        logging.getLogger("uvicorn.error").addHandler(intercept_handler)
        
        # 设置日志级别
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("uvicorn.access").setLevel(logging.INFO)
        logging.getLogger("uvicorn.error").setLevel(logging.ERROR)
        
        # 禁用传播
        logging.getLogger("uvicorn").propagate = False
        logging.getLogger("uvicorn.access").propagate = False
        logging.getLogger("uvicorn.error").propagate = False


class FastAPILogger:
    """FastAPI日志配置器"""
    
    @staticmethod
    def setup():
        """设置FastAPI使用loguru"""
        # 拦截FastAPI日志
        logging.getLogger("fastapi").handlers = []
        
        intercept_handler = InterceptHandler()
        logging.getLogger("fastapi").addHandler(intercept_handler)
        
        logging.getLogger("fastapi").setLevel(logging.INFO)
        logging.getLogger("fastapi").propagate = False


def setup_loguru():
    """设置所有日志使用loguru"""
    from .config import config
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 从YAML配置获取日志设置
    logging_config = config.get('logging', {})
    log_files = config.get('log_files', {})
    
    log_level = logging_config.get('level', 'INFO')
    max_size = log_files.get('max_size', '10 MB')
    retention = log_files.get('retention', '30 days')
    compression = log_files.get('compression', 'zip')
    
    # 移除默认的logger
    logger.remove()
    
    # 控制台日志格式
    console_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # 添加控制台日志
    logger.add(
        sys.stdout,
        level=log_level,
        format=console_format,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # 普通日志文件
    app_log = log_files.get('app_log', 'logs/app.log')
    logger.add(
        app_log,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation=max_size,
        retention=retention,
        compression=compression,
        encoding="utf-8"
    )
    
    # 错误日志文件
    error_log = log_files.get('error_log', 'logs/error.log')
    logger.add(
        error_log,
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        rotation=max_size,
        retention=retention,
        compression=compression,
        encoding="utf-8",
        backtrace=True,
        diagnose=True
    )
    
    # 访问日志文件
    access_log = log_files.get('access_log', 'logs/access.log')
    logger.add(
        access_log,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        rotation=max_size,
        retention=retention,
        compression=compression,
        encoding="utf-8",
        filter=lambda record: record["extra"].get("type") == "access"
    )
    
    # 数据库日志文件
    database_log = log_files.get('database_log', 'logs/database.log')
    logger.add(
        database_log,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation=max_size,
        retention=retention,
        compression=compression,
        encoding="utf-8",
        filter=lambda record: record["extra"].get("type") == "database"
    )
    
    # 配置Uvicorn和FastAPI使用loguru
    UvicornLogger.setup()
    FastAPILogger.setup()
    
    return logger