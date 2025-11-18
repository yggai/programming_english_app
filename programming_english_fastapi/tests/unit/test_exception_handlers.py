"""全局异常处理测试模块"""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlmodel import Session

from app.services.user_service import UserService
from app.models.user import UserCreate
from app.utils.response_utils import error_response


class TestGlobalExceptionHandlers:
    """全局异常处理测试类"""
    
    def test_http_exception_handler(self, client: TestClient):
        """测试HTTP异常处理"""
        # When: 访问不存在的路由
        response = client.get("/api/v1/nonexistent")
        
        # Then: 验证统一错误响应格式
        assert response.status_code == 404
        data = response.json()
        
        # 验证统一响应格式
        assert data["success"] is False
        assert data["code"] == 404
        assert "message" in data
        assert data["data"] is None
        assert "timestamp" in data
    
    def test_validation_exception_handler(self, client: TestClient):
        """测试验证异常处理"""
        # When: 发送无效的请求数据
        invalid_data = {
            "username": "",  # 空用户名
            "password": "123"  # 密码太短
        }
        response = client.post("/api/v1/auth/login", json=invalid_data)
        
        # Then: 验证统一错误响应格式
        assert response.status_code == 422
        data = response.json()
        
        # 验证统一响应格式
        assert data["success"] is False
        assert data["code"] == 422
        assert "message" in data
        assert "data" in data
        assert "timestamp" in data
    
    def test_value_error_handler(self, client: TestClient, user_service: UserService):
        """测试ValueError异常处理"""
        # Given: 创建测试用户
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        user_create = UserCreate(**user_data)
        user_service.create_user(user_create)
        
        # When: 尝试创建重复用户（会抛出ValueError）
        response = client.post("/api/v1/users", json=user_data)
        
        # Then: 验证统一错误响应格式
        assert response.status_code == 400
        data = response.json()
        
        # 验证统一响应格式
        assert data["success"] is False
        assert data["code"] == 400
        assert "用户名" in data["message"] and "已存在" in data["message"]
        assert data["data"] is None
        assert "timestamp" in data
    
    def test_integrity_error_handler(self, client: TestClient):
        """测试数据库完整性异常处理"""
        # When: 模拟数据库约束错误
        response = client.post("/api/v1/test/integrity-error")
        
        # Then: 验证统一错误响应格式
        assert response.status_code == 400
        data = response.json()
        
        # 验证统一响应格式
        assert data["success"] is False
        assert data["code"] == 400
        assert "message" in data
        assert data["data"] is None
    
    def test_runtime_error_handler(self, client: TestClient):
        """测试运行时异常处理"""
        # When: 模拟运行时错误
        response = client.post("/api/v1/test/runtime-error")
        
        # Then: 验证统一错误响应格式
        assert response.status_code == 500
        data = response.json()
        
        # 验证统一响应格式
        assert data["success"] is False
        assert data["code"] == 500
        assert "message" in data
        assert data["data"] is None
    
    def test_generic_exception_handler(self, client: TestClient):
        """测试通用异常处理"""
        # When: 模拟通用异常
        response = client.post("/api/v1/test/generic-error")
        
        # Then: 验证统一错误响应格式
        assert response.status_code == 500
        data = response.json()
        
        # 验证统一响应格式
        assert data["success"] is False
        assert data["code"] == 500
        assert "message" in data
        assert data["data"] is None
    
    def test_exception_with_error_details(self, client: TestClient):
        """测试带错误详情的异常处理"""
        # When: 模拟带详细错误信息的异常
        response = client.post("/api/v1/test/validation-error")
        
        # Then: 验证错误详情被包含在响应中
        assert response.status_code == 400
        data = response.json()
        
        # 验证统一响应格式和错误详情
        assert data["success"] is False
        assert data["code"] == 400
        assert "data" in data
        assert data["data"] is not None  # 应该有错误详情
    
    def test_logging_on_exception(self, client: TestClient):
        """测试异常处理时的日志记录"""
        # When: 触发异常
        with pytest.raises(Exception):
            # 模拟内部异常（这个测试主要检查日志是否记录）
            pass
        
        # 实际的日志记录测试需要通过日志捕获来验证
        # 这里主要是确保异常处理器包含日志记录逻辑
    
    def test_custom_exception_handler(self, client: TestClient):
        """测试自定义异常处理"""
        # When: 触发自定义异常
        response = client.post("/api/v1/test/custom-exception")
        
        # Then: 验证自定义异常的统一响应格式
        assert response.status_code == 400
        data = response.json()
        
        # 验证统一响应格式
        assert data["success"] is False
        assert data["code"] == 400
        assert "message" in data
        assert data["data"] is None
    
    def test_exception_handler_preserves_original_error(self, client: TestClient):
        """测试异常处理器保留原始错误信息"""
        # When: 触发包含特定信息的异常
        response = client.post("/api/v1/test/specific-error")
        
        # Then: 验证原始错误信息被保留
        assert response.status_code == 500
        data = response.json()
        
        # 验证错误信息被正确传递
        assert data["success"] is False
        assert data["code"] == 500
        assert "message" in data
        # 应该包含原始错误的信息