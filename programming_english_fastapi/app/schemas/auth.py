"""认证相关的Pydantic模型"""

from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str  # 可以是用户名或邮箱
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "admin123456"
            }
        }
    )


class Token(BaseModel):
    """Token响应模型"""
    access_token: str
    token_type: str = "bearer"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer"
            }
        }
    )


class TokenData(BaseModel):
    """Token数据模型"""
    username: Optional[str] = None
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: EmailStr
    full_name: str
    is_active: bool
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "Administrator",
                "is_active": True
            }
        }
    )


class PasswordChangeRequest(BaseModel):
    """密码修改请求模型"""
    current_password: str
    new_password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_password": "old_password",
                "new_password": "new_password"
            }
        }
    )


class PasswordResetRequest(BaseModel):
    """密码重置请求模型"""
    email: EmailStr
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com"
            }
        }
    )