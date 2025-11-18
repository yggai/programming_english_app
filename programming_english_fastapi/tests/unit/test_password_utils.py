"""密码工具测试模块"""

import pytest
from app.utils.password_utils import hash_password, verify_password


class TestPasswordUtils:
    """密码工具测试类"""
    
    def test_hash_password_success(self):
        """测试成功哈希密码"""
        # Given: 明文密码
        password = "test_password_123"
        
        # When: 哈希密码
        hashed = hash_password(password)
        
        # Then: 验证哈希结果
        assert hashed is not None
        assert len(hashed) == 64  # SHA256 是32字节 = 64个十六进制字符
        assert hashed != password  # 哈希后与原密码不同
        assert all(c in '0123456789abcdef' for c in hashed)  # 只包含十六进制字符
    
    def test_hash_password_empty_string(self):
        """测试空密码哈希"""
        # Given: 空密码
        password = ""
        
        # When: 哈希密码
        hashed = hash_password(password)
        
        # Then: 应该成功哈希
        assert hashed is not None
        assert len(hashed) == 64
    
    def test_hash_password_consistency(self):
        """测试相同密码哈希一致性"""
        # Given: 相同密码
        password = "consistent_password"
        
        # When: 多次哈希相同密码
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Then: 哈希结果应该一致（不带盐的情况下）
        assert hash1 == hash2
    
    def test_hash_password_different_inputs(self):
        """测试不同密码哈希不同"""
        # Given: 不同密码
        password1 = "password1"
        password2 = "password2"
        
        # When: 哈希不同密码
        hash1 = hash_password(password1)
        hash2 = hash_password(password2)
        
        # Then: 哈希结果应该不同
        assert hash1 != hash2
    
    def test_verify_password_success(self):
        """测试密码验证成功"""
        # Given: 密码和其哈希
        password = "correct_password"
        hashed = hash_password(password)
        
        # When: 验证正确密码
        is_valid = verify_password(password, hashed)
        
        # Then: 验证应该成功
        assert is_valid is True
    
    def test_verify_password_failure(self):
        """测试密码验证失败"""
        # Given: 密码和错误密码
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        # When: 验证错误密码
        is_valid = verify_password(wrong_password, hashed)
        
        # Then: 验证应该失败
        assert is_valid is False
    
    def test_verify_password_empty_inputs(self):
        """测试空输入验证"""
        # Given: 空密码和其哈希
        password = ""
        hashed = hash_password(password)
        
        # When: 验证空密码
        is_valid = verify_password(password, hashed)
        
        # Then: 验证应该成功
        assert is_valid is True
    
    def test_verify_password_nonexistent_hash(self):
        """测试不存在的哈希验证"""
        # Given: 密码和无效哈希
        password = "test_password"
        invalid_hash = "invalid_hash_not_64_chars"
        
        # When: 验证无效哈希
        is_valid = verify_password(password, invalid_hash)
        
        # Then: 验证应该失败
        assert is_valid is False
    
    def test_hash_password_unicode_support(self):
        """测试Unicode密码支持"""
        # Given: 包含Unicode字符的密码
        password = "密码测试🔒123"
        
        # When: 哈希Unicode密码
        hashed = hash_password(password)
        
        # Then: 应该成功哈希
        assert hashed is not None
        assert len(hashed) == 64
        
        # And: 应该能正确验证
        is_valid = verify_password(password, hashed)
        assert is_valid is True
    
    def test_verify_password_case_sensitive(self):
        """测试密码大小写敏感"""
        # Given: 大小写不同的密码
        password_lower = "password"
        password_upper = "PASSWORD"
        hashed = hash_password(password_lower)
        
        # When: 验证不同大小写的密码
        is_valid_lower = verify_password(password_lower, hashed)
        is_valid_upper = verify_password(password_upper, hashed)
        
        # Then: 只有正确的密码应该验证成功
        assert is_valid_lower is True
        assert is_valid_upper is False