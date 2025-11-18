"""应用初始化模块"""

from loguru import logger
from sqlalchemy.exc import IntegrityError
from ..db.database import engine
from ..models.user import User, UserCreate
from ..services.user_service import UserService
from ..core.config import config
from sqlmodel import SQLModel
from sqlmodel import Session


def initialize_application():
    """初始化应用"""
    logger.info("开始初始化应用...")
    
    # 创建数据库表
    SQLModel.metadata.create_all(engine)
    logger.success("数据库表创建成功")
    
    # 初始化超级用户
    with Session(engine) as session:
        user_service = UserService(session)
        success = user_service.initialize_superuser()
        
        if success:
            logger.success("应用初始化完成")
        else:
            logger.warning("应用初始化完成，但超级用户创建失败")
    
    return True