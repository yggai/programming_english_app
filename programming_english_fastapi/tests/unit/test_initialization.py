"""应用初始化测试模块"""

import pytest
from sqlmodel import Session
from unittest.mock import patch, MagicMock

from app.core.initialization import initialize_application
from app.services.user_service import UserService


class TestInitialization:
    """应用初始化测试类"""
    
    def test_initialize_application_success(self, superuser_config: dict):
        """测试成功初始化应用"""
        # Given: 超级用户配置完整
        assert superuser_config
        
        # When: 初始化应用
        result = initialize_application()
        
        # Then: 初始化应成功
        assert result is True
    
    @patch('app.core.initialization.SQLModel')
    def test_initialize_application_database_creation(self, mock_sqlmodel):
        """测试数据库表创建"""
        # When: 初始化应用
        initialize_application()
        
        # Then: 数据库表创建方法应被调用
        mock_sqlmodel.metadata.create_all.assert_called_once()
    
    @patch('app.core.initialization.UserService')
    def test_initialize_application_superuser_creation(self, mock_user_service_class):
        """测试超级用户创建"""
        # Given: 模拟用户服务
        mock_user_service = MagicMock()
        mock_user_service.initialize_superuser.return_value = True
        mock_user_service_class.return_value = mock_user_service
        
        # When: 初始化应用
        result = initialize_application()
        
        # Then: 超级用户初始化方法应被调用
        mock_user_service.initialize_superuser.assert_called_once()
        assert result is True
    
    @patch('app.core.initialization.UserService')
    def test_initialize_application_superuser_creation_failure(self, mock_user_service_class):
        """测试超级用户创建失败"""
        # Given: 模拟用户服务创建失败
        mock_user_service = MagicMock()
        mock_user_service.initialize_superuser.return_value = False
        mock_user_service_class.return_value = mock_user_service
        
        # When: 初始化应用
        result = initialize_application()
        
        # Then: 初始化应仍然成功（只是超级用户创建失败）
        assert result is True
    
    def test_initialize_application_logging(self):
        """测试初始化过程中的日志记录"""
        # Given: 模拟日志记录
        with patch('app.core.initialization.logger') as mock_logger:
            # When: 初始化应用
            initialize_application()
            
            # Then: 应记录相关日志
            mock_logger.info.assert_called_with("开始初始化应用...")
            mock_logger.success.assert_called_with("数据库表创建成功")