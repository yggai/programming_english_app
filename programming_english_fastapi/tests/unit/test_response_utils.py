"""统一响应工具测试模块"""

import pytest
from datetime import datetime
from app.utils.response_utils import (
    success_response, error_response, 
    pagination_response, create_response,
    ResponseStatus
)


class TestResponseUtils:
    """统一响应工具测试类"""
    
    def test_success_response_basic(self):
        """测试基础成功响应"""
        # Given: 响应数据
        data = {"message": "操作成功"}
        
        # When: 创建成功响应
        response = success_response(data)
        
        # Then: 验证响应结构
        assert response["success"] is True
        assert response["code"] == 200
        assert response["message"] == "操作成功"
        assert response["data"] == data
        assert "timestamp" in response
        assert isinstance(response["timestamp"], str)
    
    def test_success_response_custom_message(self):
        """测试自定义消息的成功响应"""
        # Given: 响应数据和自定义消息
        data = {"id": 1}
        message = "用户创建成功"
        
        # When: 创建自定义消息的成功响应
        response = success_response(data, message)
        
        # Then: 验证响应
        assert response["success"] is True
        assert response["code"] == 200
        assert response["message"] == message
        assert response["data"] == data
    
    def test_error_response_basic(self):
        """测试基础错误响应"""
        # Given: 错误信息
        message = "用户名不存在"
        
        # When: 创建错误响应
        response = error_response(message)
        
        # Then: 验证响应结构
        assert response["success"] is False
        assert response["code"] == 400
        assert response["message"] == message
        assert response["data"] is None
        assert "timestamp" in response
    
    def test_error_response_custom_code(self):
        """测试自定义状态码的错误响应"""
        # Given: 错误信息和自定义状态码
        message = "权限不足"
        code = 403
        
        # When: 创建自定义状态码的错误响应
        response = error_response(message, code)
        
        # Then: 验证响应
        assert response["success"] is False
        assert response["code"] == code
        assert response["message"] == message
        assert response["data"] is None
    
    def test_error_response_with_data(self):
        """测试带数据的错误响应"""
        # Given: 错误信息和错误详情
        message = "验证失败"
        error_data = {"field": "username", "error": "用户名已存在"}
        
        # When: 创建带数据的错误响应
        response = error_response(message, 400, error_data)
        
        # Then: 验证响应
        assert response["success"] is False
        assert response["code"] == 400
        assert response["message"] == message
        assert response["data"] == error_data
    
    def test_pagination_response_basic(self):
        """测试基础分页响应"""
        # Given: 分页数据
        items = [{"id": 1}, {"id": 2}]
        total = 10
        page = 1
        size = 2
        
        # When: 创建分页响应
        response = pagination_response(items, total, page, size)
        
        # Then: 验证响应结构
        assert response["success"] is True
        assert response["code"] == 200
        assert response["message"] == "获取数据成功"
        
        # 验证分页信息
        pagination = response["data"]
        assert pagination["items"] == items
        assert pagination["total"] == total
        assert pagination["page"] == page
        assert pagination["size"] == size
        assert pagination["pages"] == 5  # ceil(10/2) = 5
        assert "has_next" in pagination
        assert "has_prev" in pagination
    
    def test_pagination_response_last_page(self):
        """测试最后一页分页响应"""
        # Given: 最后一页数据
        items = [{"id": 9}, {"id": 10}]
        total = 10
        page = 5
        size = 2
        
        # When: 创建最后一页响应
        response = pagination_response(items, total, page, size)
        
        # Then: 验证分页状态
        pagination = response["data"]
        assert pagination["has_next"] is False
        assert pagination["has_prev"] is True
    
    def test_pagination_response_first_page(self):
        """测试第一页分页响应"""
        # Given: 第一页数据
        items = [{"id": 1}, {"id": 2}]
        total = 10
        page = 1
        size = 2
        
        # When: 创建第一页响应
        response = pagination_response(items, total, page, size)
        
        # Then: 验证分页状态
        pagination = response["data"]
        assert pagination["has_next"] is True
        assert pagination["has_prev"] is False
    
    def test_create_response_custom(self):
        """测试自定义响应"""
        # Given: 自定义响应参数
        success = False
        code = 500
        message = "服务器内部错误"
        data = {"error_code": "INTERNAL_ERROR"}
        
        # When: 创建自定义响应
        response = create_response(success, code, message, data)
        
        # Then: 验证响应
        assert response["success"] == success
        assert response["code"] == code
        assert response["message"] == message
        assert response["data"] == data
    
    def test_response_status_constants(self):
        """测试响应状态常量"""
        # Given: 响应状态常量
        
        # Then: 验证常量值
        assert ResponseStatus.SUCCESS == "操作成功"
        assert ResponseStatus.CREATED == "创建成功"
        assert ResponseStatus.UPDATED == "更新成功"
        assert ResponseStatus.DELETED == "删除成功"
        assert ResponseStatus.NOT_FOUND == "数据不存在"
        assert ResponseStatus.UNAUTHORIZED == "未授权"
        assert ResponseStatus.FORBIDDEN == "权限不足"
        assert ResponseStatus.BAD_REQUEST == "请求参数错误"
        assert ResponseStatus.INTERNAL_ERROR == "服务器内部错误"
    
    def test_empty_data_response(self):
        """测试空数据响应"""
        # Given: 空数据
        data = None
        
        # When: 创建成功响应
        response = success_response(data)
        
        # Then: 验证响应
        assert response["success"] is True
        assert response["data"] is None
        assert response["code"] == 200
    
    def test_list_data_response(self):
        """测试列表数据响应"""
        # Given: 列表数据
        data = [{"id": 1}, {"id": 2}]
        
        # When: 创建成功响应
        response = success_response(data)
        
        # Then: 验证响应
        assert response["success"] is True
        assert response["data"] == data
        assert len(response["data"]) == 2