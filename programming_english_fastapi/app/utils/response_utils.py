"""统一响应工具模块"""

import math
from datetime import datetime
from typing import Any, Optional, List, Dict, Union
from pydantic import BaseModel, ConfigDict


class ResponseStatus:
    """响应状态消息常量"""
    SUCCESS = "操作成功"
    CREATED = "创建成功"
    UPDATED = "更新成功"
    DELETED = "删除成功"
    NOT_FOUND = "数据不存在"
    UNAUTHORIZED = "未授权"
    FORBIDDEN = "权限不足"
    BAD_REQUEST = "请求参数错误"
    INTERNAL_ERROR = "服务器内部错误"


class PaginationData(BaseModel):
    """分页数据模型"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [{"id": 1}, {"id": 2}],
                "total": 10,
                "page": 1,
                "size": 2,
                "pages": 5,
                "has_next": True,
                "has_prev": False
            }
        }
    )


class StandardResponse(BaseModel):
    """标准响应模型"""
    success: bool
    code: int
    message: str
    data: Optional[Any] = None
    timestamp: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "code": 200,
                "message": "操作成功",
                "data": {"id": 1},
                "timestamp": "2025-11-18T21:27:13.000Z"
            }
        }
    )


class PaginationResponse(BaseModel):
    """分页响应模型"""
    success: bool
    code: int
    message: str
    data: PaginationData
    timestamp: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "code": 200,
                "message": "获取数据成功",
                "data": {
                    "items": [{"id": 1}, {"id": 2}],
                    "total": 10,
                    "page": 1,
                    "size": 2,
                    "pages": 5,
                    "has_next": True,
                    "has_prev": False
                },
                "timestamp": "2025-11-18T21:27:13.000Z"
            }
        }
    )


def create_response(
    success: bool,
    code: int,
    message: str,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    创建标准响应
    
    Args:
        success: 操作是否成功
        code: 响应状态码
        message: 响应消息
        data: 响应数据
        
    Returns:
        Dict: 标准响应格式
    """
    return {
        "success": success,
        "code": code,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def success_response(
    data: Optional[Any] = None,
    message: str = ResponseStatus.SUCCESS,
    code: int = 200
) -> Dict[str, Any]:
    """
    创建成功响应
    
    Args:
        data: 响应数据
        message: 成功消息
        code: 成功状态码
        
    Returns:
        Dict: 成功响应格式
    """
    return create_response(True, code, message, data)


def error_response(
    message: str,
    code: int = 400,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    创建错误响应
    
    Args:
        message: 错误消息
        code: 错误状态码
        data: 错误详情数据
        
    Returns:
        Dict: 错误响应格式
    """
    return create_response(False, code, message, data)


def pagination_response(
    items: List[Any],
    total: int,
    page: int,
    size: int,
    message: str = "获取数据成功",
    code: int = 200
) -> Dict[str, Any]:
    """
    创建分页响应
    
    Args:
        items: 数据项列表
        total: 总记录数
        page: 当前页码
        size: 每页大小
        message: 成功消息
        code: 成功状态码
        
    Returns:
        Dict: 分页响应格式
    """
    # 计算总页数
    pages = math.ceil(total / size) if size > 0 else 0
    
    # 计算分页状态
    has_next = page < pages
    has_prev = page > 1
    
    # 创建分页数据
    pagination_data = {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "has_next": has_next,
        "has_prev": has_prev
    }
    
    return create_response(True, code, message, pagination_data)


def created_response(data: Optional[Any] = None, message: str = ResponseStatus.CREATED) -> Dict[str, Any]:
    """
    创建成功响应 (201)
    
    Args:
        data: 响应数据
        message: 成功消息
        
    Returns:
        Dict: 创建成功响应格式
    """
    return success_response(data, message, 201)


def updated_response(data: Optional[Any] = None, message: str = ResponseStatus.UPDATED) -> Dict[str, Any]:
    """
    创建更新响应
    
    Args:
        data: 响应数据
        message: 成功消息
        
    Returns:
        Dict: 更新成功响应格式
    """
    return success_response(data, message)


def deleted_response(message: str = ResponseStatus.DELETED) -> Dict[str, Any]:
    """
    创建删除响应
    
    Args:
        message: 成功消息
        
    Returns:
        Dict: 删除成功响应格式
    """
    return success_response(None, message)


def not_found_response(message: str = ResponseStatus.NOT_FOUND) -> Dict[str, Any]:
    """
    创建未找到响应
    
    Args:
        message: 错误消息
        
    Returns:
        Dict: 未找到响应格式
    """
    return error_response(message, 404)


def unauthorized_response(message: str = ResponseStatus.UNAUTHORIZED) -> Dict[str, Any]:
    """
    创建未授权响应
    
    Args:
        message: 错误消息
        
    Returns:
        Dict: 未授权响应格式
    """
    return error_response(message, 401)


def forbidden_response(message: str = ResponseStatus.FORBIDDEN) -> Dict[str, Any]:
    """
    创建禁止访问响应
    
    Args:
        message: 错误消息
        
    Returns:
        Dict: 禁止访问响应格式
    """
    return error_response(message, 403)


def bad_request_response(
    message: str = ResponseStatus.BAD_REQUEST,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    创建错误请求响应
    
    Args:
        message: 错误消息
        data: 错误详情
        
    Returns:
        Dict: 错误请求响应格式
    """
    return error_response(message, 400, data)


def internal_error_response(
    message: str = ResponseStatus.INTERNAL_ERROR,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    创建内部错误响应
    
    Args:
        message: 错误消息
        data: 错误详情
        
    Returns:
        Dict: 内部错误响应格式
    """
    return error_response(message, 500, data)