"""loguru日志配置模块"""

import os
import sys
from pathlib import Path
from loguru import logger
from typing import Dict, Any

class LoguruConfig:
    """loguru日志配置器"""
    
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志配置"""
        # 移除默认的logger
        logger.remove()
        
        # 从YAML配置获取日志设置
        from .config import config
        logging_config = config.get('logging', {})
        log_files = config.get('log_files', {})
        
        log_level = logging_config.get('level', 'INFO')
        max_size = log_files.get('max_size', '10 MB')
        retention = log_files.get('retention', '30 days')
        compression = log_files.get('compression', 'zip')
        
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


# 创建全局日志配置实例
loguru_config = LoguruConfig()

# 导出logger供其他模块使用
__all__ = ['logger', 'loguru_config']