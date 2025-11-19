"""认证API模块"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from loguru import logger

from app.db.database import get_session
from app.services.user_service import UserService
from app.schemas.auth import LoginRequest, Token
from app.utils.jwt_utils import create_user_token

router = APIRouter()


@router.post("/login", response_model=dict)
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    """
    用户登录
    
    Args:
        login_data: 登录请求数据
        session: 数据库会话
        
    Returns:
        dict: 统一格式的登录响应
    """
    # 验证输入
    if not login_data.username or not login_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    
    user_service = UserService(session)
    
    # 尝试通过用户名查找用户
    user = user_service.get_user_by_username(login_data.username)
    
    # 如果用户名不存在，尝试通过邮箱查找
    if not user:
        user = user_service.get_user_by_email(login_data.username)
    
    # 验证用户存在且密码正确
    if not user or not user_service.verify_password(login_data.password, user.hashed_password):
        logger.warning(f"登录失败 - 用户名: {login_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    
    # 验证用户是否活跃
    if not user.is_active:
        logger.warning(f"非活跃用户尝试登录 - 用户名: {login_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户已被禁用")
    
    # 生成访问令牌
    access_token = create_user_token(user.id, user.username)
    
    logger.info(f"用户登录成功 - 用户名: {login_data.username}")
    
    # 返回登录令牌（顶层字段符合测试期望）
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():
    """
    用户登出
    
    Returns:
        dict: 统一格式的登出响应
    """
    logger.info("用户登出")
    return {"success": True, "message": "登出成功"}