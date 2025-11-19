"""用户认证API测试模块"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.services.user_service import UserService
from app.models.user import UserCreate


class TestAuthAPI:
    """用户认证API测试类"""
    
    def test_login_success(self, client: TestClient, user_service: UserService, test_user_data: dict):
        """测试登录成功"""
        # Given: 创建测试用户
        user_create = UserCreate(**test_user_data)
        user_service.create_user(user_create)
        
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录成功
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0  # JWT token不为空
    
    def test_login_with_username_success(self, client: TestClient, user_service: UserService, test_user_data: dict):
        """测试使用用户名登录成功"""
        # Given: 创建测试用户
        user_create = UserCreate(**test_user_data)
        user_service.create_user(user_create)
        
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录成功
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
    
    def test_login_with_email_success(self, client: TestClient, user_service: UserService, test_user_data: dict):
        """测试使用邮箱登录成功"""
        # Given: 创建测试用户
        user_create = UserCreate(**test_user_data)
        user_service.create_user(user_create)
        
        login_data = {
            "username": test_user_data["email"],  # 使用邮箱作为用户名
            "password": test_user_data["password"]
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录成功
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
    
    def test_login_wrong_password(self, client: TestClient, user_service: UserService, test_user_data: dict):
        """测试密码错误"""
        # Given: 创建测试用户
        user_create = UserCreate(**test_user_data)
        user_service.create_user(user_create)
        
        login_data = {
            "username": test_user_data["username"],
            "password": "wrong_password"
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录失败
        assert response.status_code == 401
        data = response.json()
        assert data.get("code") == 401
        assert "用户名或密码错误" in data.get("message", "")
    
    def test_login_nonexistent_user(self, client: TestClient):
        """测试不存在的用户登录"""
        # Given: 不存在的用户数据
        login_data = {
            "username": "nonexistent_user",
            "password": "some_password"
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录失败
        assert response.status_code == 401
        data = response.json()
        assert data.get("code") == 401
        assert "用户名或密码错误" in data.get("message", "")
    
    def test_login_missing_username(self, client: TestClient):
        """测试缺少用户名"""
        # Given: 缺少用户名的登录数据
        login_data = {
            "password": "some_password"
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证请求失败
        assert response.status_code == 422  # 验证错误
    
    def test_login_missing_password(self, client: TestClient):
        """测试缺少密码"""
        # Given: 缺少密码的登录数据
        login_data = {
            "username": "some_user"
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证请求失败
        assert response.status_code == 422  # 验证错误
    
    def test_login_empty_credentials(self, client: TestClient):
        """测试空凭据"""
        # Given: 空的登录数据
        login_data = {
            "username": "",
            "password": ""
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录失败
        assert response.status_code == 401
        data = response.json()
        assert data.get("code") == 401
        assert "用户名或密码错误" in data.get("message", "")
    
    def test_login_inactive_user(self, client: TestClient, user_service: UserService, test_user_data: dict):
        """测试非活跃用户登录"""
        # Given: 创建非活跃用户
        user_create = UserCreate(**test_user_data)
        user = user_service.create_user(user_create)
        # 手动设置为非活跃
        user.is_active = False
        user_service.session.commit()
        
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录失败
        assert response.status_code == 401
        data = response.json()
        assert data.get("code") == 401
        assert "用户已被禁用" in data.get("message", "")
    
    def test_login_unicode_password(self, client: TestClient, user_service: Session):
        """测试Unicode密码登录"""
        # Given: 创建Unicode密码的用户
        unicode_data = {
            "username": "unicode_user",
            "email": "unicode@example.com",
            "password": "密码测试🔒123",
            "full_name": "Unicode User"
        }
        user_create = UserCreate(**unicode_data)
        user_service.create_user(user_create)
        
        login_data = {
            "username": unicode_data["username"],
            "password": unicode_data["password"]
        }
        
        # When: 发送登录请求
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Then: 验证登录成功
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data