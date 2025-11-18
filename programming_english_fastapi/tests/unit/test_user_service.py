"""用户服务测试模块"""

import pytest
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from app.services.user_service import UserService
from app.models.user import UserCreate, User


class TestUserService:
    """用户服务测试类"""
    
    def test_create_user_success(self, user_service: UserService, test_user_data: dict):
        """测试成功创建用户"""
        # Given: 用户创建数据
        user_create = UserCreate(**test_user_data)
        
        # When: 创建用户
        user = user_service.create_user(user_create)
        
        # Then: 验证用户创建成功
        assert user.username == test_user_data["username"]
        assert user.email == test_user_data["email"]
        assert user.full_name == test_user_data["full_name"]
        assert user.is_active is True
        assert user.id is not None
        assert user.hashed_password is not None
        assert user.hashed_password != test_user_data["password"]  # 密码已哈希
    
    def test_create_user_duplicate_username(self, user_service: UserService, test_user_data: dict):
        """测试创建重复用户名的用户"""
        # Given: 已存在用户
        user_create = UserCreate(**test_user_data)
        user_service.create_user(user_create)
        
        # When & Then: 创建相同用户名的用户应抛出异常
        with pytest.raises(ValueError, match="用户名 .* 已存在"):
            user_service.create_user(user_create)
    
    def test_create_user_duplicate_email(self, user_service: UserService, test_user_data: dict):
        """测试创建重复邮箱的用户"""
        # Given: 已存在用户
        user_create = UserCreate(**test_user_data)
        user_service.create_user(user_create)
        
        # When & Then: 创建相同邮箱的用户应抛出异常
        duplicate_data = test_user_data.copy()
        duplicate_data["username"] = "different_username"
        with pytest.raises(ValueError, match="邮箱 .* 已存在"):
            user_service.create_user(UserCreate(**duplicate_data))
    
    def test_get_user_by_username(self, user_service: UserService, test_user_data: dict):
        """测试根据用户名获取用户"""
        # Given: 创建用户
        user_create = UserCreate(**test_user_data)
        created_user = user_service.create_user(user_create)
        
        # When: 根据用户名获取用户
        found_user = user_service.get_user_by_username(test_user_data["username"])
        
        # Then: 验证用户信息正确
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.username == test_user_data["username"]
    
    def test_get_user_by_username_not_found(self, user_service: UserService):
        """测试获取不存在的用户"""
        # When: 获取不存在的用户
        user = user_service.get_user_by_username("nonexistent_user")
        
        # Then: 应返回None
        assert user is None
    
    def test_verify_password_success(self, user_service: UserService, test_user_data: dict):
        """测试密码验证成功"""
        # Given: 创建用户
        user_create = UserCreate(**test_user_data)
        user = user_service.create_user(user_create)
        
        # When: 验证密码
        is_valid = user_service.verify_password(
            test_user_data["password"], 
            user.hashed_password
        )
        
        # Then: 密码验证应成功
        assert is_valid is True
    
    def test_verify_password_failure(self, user_service: UserService, test_user_data: dict):
        """测试密码验证失败"""
        # Given: 创建用户
        user_create = UserCreate(**test_user_data)
        user = user_service.create_user(user_create)
        
        # When: 验证错误密码
        is_valid = user_service.verify_password(
            "wrong_password", 
            user.hashed_password
        )
        
        # Then: 密码验证应失败
        assert is_valid is False
    
    def test_initialize_superuser_success(self, user_service: UserService, superuser_config: dict):
        """测试成功初始化超级用户"""
        # Given: 超级用户配置完整
        assert superuser_config
        
        # When: 初始化超级用户
        result = user_service.initialize_superuser()
        
        # Then: 初始化应成功
        assert result is True
        
        # And: 验证超级用户已创建
        superuser = user_service.get_user_by_username(superuser_config["username"])
        assert superuser is not None
        assert superuser.email == superuser_config["email"]
    
    def test_initialize_superuser_already_exists(self, user_service: UserService, superuser_config: dict):
        """测试超级用户已存在时初始化"""
        # Given: 已存在超级用户
        user_service.initialize_superuser()
        
        # When: 再次初始化超级用户
        result = user_service.initialize_superuser()
        
        # Then: 初始化应成功，但不会重复创建
        assert result is True
    
    def test_initialize_superuser_no_config(self, user_service: UserService):
        """测试没有超级用户配置时的初始化"""
        # Given: 覆盖配置为空
        from app.core.config import config
        original_config = config._config_data
        config._config_data = {"superuser": {}}
        
        try:
            # When: 初始化超级用户
            result = user_service.initialize_superuser()
            
            # Then: 初始化应失败
            assert result is False
        finally:
            # Restore original config
            config._config_data = original_config