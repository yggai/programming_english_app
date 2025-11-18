"""密码工具模块 - 使用SHA256实现密码哈希"""

import hashlib
from typing import Optional


def hash_password(password: str) -> str:
    """
    使用SHA256哈希密码
    
    Args:
        password: 明文密码
        
    Returns:
        str: 哈希后的密码（64位十六进制字符串）
        
    Raises:
        ValueError: 当密码为None时
    """
    if password is None:
        raise ValueError("密码不能为None")
    
    # 将密码编码为UTF-8字节，然后计算SHA256哈希
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    hashed_password = hash_object.hexdigest()
    
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
        
    Returns:
        bool: 密码是否正确
        
    Notes:
        - 如果任一参数为None，返回False
        - 如果哈希密码长度不是64位，返回False
        - 如果哈希密码包含非十六进制字符，返回False
    """
    # 参数验证
    if plain_password is None or hashed_password is None:
        return False
    
    # 验证哈希密码格式
    if len(hashed_password) != 64:
        return False
    
    # 验证哈希密码只包含十六进制字符
    if not all(c in '0123456789abcdef' for c in hashed_password.lower()):
        return False
    
    # 计算明文密码的哈希并比较
    computed_hash = hash_password(plain_password)
    return computed_hash.lower() == hashed_password.lower()


def is_strong_password(password: str) -> bool:
    """
    检查密码强度
    
    Args:
        password: 要检查的密码
        
    Returns:
        bool: 密码是否足够强
        
    Notes:
        - 至少8个字符
        - 包含大小写字母
        - 包含数字
    """
    if password is None or len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit


def generate_password_hash_with_salt(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """
    生成带盐的密码哈希
    
    Args:
        password: 明文密码
        salt: 盐值，如果不提供则生成随机盐
        
    Returns:
        tuple: (salt, hashed_password)
        
    Notes:
        盐值长度为32个字符
        哈希结果为盐+密码的组合哈希
    """
    if password is None:
        raise ValueError("密码不能为None")
    
    if salt is None:
        # 生成32字符的随机盐
        import random
        import string
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    # 组合盐和密码
    salted_password = salt + password
    
    # 哈希组合
    hash_object = hashlib.sha256(salted_password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()
    
    return salt, hashed_password


def verify_password_with_salt(plain_password: str, salt: str, hashed_password: str) -> bool:
    """
    验证带盐的密码
    
    Args:
        plain_password: 明文密码
        salt: 盐值
        hashed_password: 哈希密码
        
    Returns:
        bool: 密码是否正确
    """
    if not all([plain_password, salt, hashed_password]):
        return False
    
    # 使用相同的盐计算哈希
    _, computed_hash = generate_password_hash_with_salt(plain_password, salt)
    return computed_hash == hashed_password