"""用户服务模块"""

from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from loguru import logger

from ..models.user import User, UserCreate
from ..core.config import config
from ..utils.password_utils import hash_password, verify_password


class UserService:
    """用户服务类"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_user(self, user_create: UserCreate) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        existing_user = self.get_user_by_username(user_create.username)
        if existing_user:
            raise ValueError(f"用户名 {user_create.username} 已存在")
        
        # 检查邮箱是否已存在
        existing_email = self.get_user_by_email(user_create.email)
        if existing_email:
            raise ValueError(f"邮箱 {user_create.email} 已存在")
        
        # 创建用户，使用SHA256哈希密码
        hashed_password = hash_password(user_create.password)
        
        user = User(
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        logger.info(f"用户创建成功: {user.username}")
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        statement = select(User).where(User.username == username)
        result = self.session.exec(statement)
        return result.first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement)
        return result.first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        statement = select(User).where(User.id == user_id)
        result = self.session.exec(statement)
        return result.first()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return verify_password(plain_password, hashed_password)
    
    def initialize_superuser(self) -> bool:
        """初始化超级用户"""
        try:
            # 获取超级用户配置
            superuser_config = config.get('superuser', {})
            if not superuser_config:
                logger.warning("超级用户配置不存在")
                return False
            
            username = superuser_config.get('username')
            email = superuser_config.get('email')
            password = superuser_config.get('password')
            full_name = superuser_config.get('full_name', 'Administrator')
            
            if not all([username, email, password]):
                logger.warning("超级用户配置不完整")
                return False
            
            # 检查超级用户是否已存在
            existing_user = self.get_user_by_username(username)
            if existing_user:
                logger.info(f"超级用户 {username} 已存在，跳过创建")
                return True
            
            # 创建超级用户
            user_create = UserCreate(
                username=username,
                email=email,
                password=password,
                full_name=full_name
            )
            
            superuser = self.create_user(user_create)
            logger.success(f"超级用户 {username} 创建成功")
            return True
            
        except IntegrityError as e:
            logger.error(f"创建超级用户失败 - 数据库约束错误: {e}")
            return False
        except Exception as e:
            logger.error(f"创建超级用户失败: {e}")
            return False