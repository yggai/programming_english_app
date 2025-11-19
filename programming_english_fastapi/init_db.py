#!/usr/bin/env python
"""数据库初始化脚本"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from app.db.database import create_db_and_tables
from app.services.user_service import UserService
from app.db.database import get_session
from loguru import logger

def init_database():
    """初始化数据库和超级用户"""
    try:
        logger.info("🔄 开始初始化数据库...")
        
        # 创建数据库表
        create_db_and_tables()
        logger.info("✅ 数据库表创建成功")
        
        # 创建超级用户
        with next(get_session()) as session:
            user_service = UserService(session)
            
            # 检查admin用户是否已存在
            admin = user_service.get_user_by_username('admin')
            if admin:
                logger.info(f"✅ 管理员用户已存在: {admin.username}")
            else:
                # 创建超级用户
                admin_user = user_service.create_user(
                    username="admin",
                    email="admin@programming-english.com",
                    password="admin123",  # 默认密码
                    is_superuser=True,
                    is_active=True
                )
                logger.info(f"✅ 超级用户创建成功: {admin_user.username}")
        
        logger.info("🎉 数据库初始化完成！")
        
    except Exception as e:
        logger.error(f"❌ 初始化失败: {e}")
        raise

if __name__ == "__main__":
    init_database()