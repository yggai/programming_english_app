"""JWT工具模块"""

import jwt
from datetime import datetime, timedelta
from typing import Optional
from ..core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码的数据字典
        expires_delta: 过期时间增量，如果为None则使用默认时间
        
    Returns:
        str: JWT访问令牌
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    验证并解码JWT令牌
    
    Args:
        token: JWT令牌字符串
        
    Returns:
        Optional[dict]: 解码后的payload，验证失败返回None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


def extract_token_from_authorization(authorization: str) -> Optional[str]:
    """
    从Authorization头部提取JWT令牌
    
    Args:
        authorization: Authorization头部值
        
    Returns:
        Optional[str]: JWT令牌，格式不正确返回None
    """
    if not authorization:
        return None
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        return token
    except ValueError:
        return None


def create_user_token(user_id: int, username: str) -> str:
    """
    为用户创建JWT令牌
    
    Args:
        user_id: 用户ID
        username: 用户名
        
    Returns:
        str: JWT访问令牌
    """
    data = {
        "sub": username,
        "user_id": user_id,
        "type": "access"
    }
    return create_access_token(data)


def get_current_user_from_token(token: str) -> Optional[dict]:
    """
    从JWT令牌获取当前用户信息
    
    Args:
        token: JWT令牌
        
    Returns:
        Optional[dict]: 用户信息，验证失败返回None
    """
    payload = verify_token(token)
    if payload is None:
        return None
    
    # 验证令牌类型
    if payload.get("type") != "access":
        return None
    
    return {
        "user_id": payload.get("user_id"),
        "username": payload.get("sub")
    }


def is_token_expired(token: str) -> bool:
    """
    检查令牌是否过期
    
    Args:
        token: JWT令牌
        
    Returns:
        bool: 是否过期
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp is None:
            return True
        
        return datetime.utcnow().timestamp() > exp
    except jwt.ExpiredSignatureError:
        return True
    except jwt.JWTError:
        return True