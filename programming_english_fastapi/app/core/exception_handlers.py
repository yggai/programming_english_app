"""全局异常处理器模块"""

from typing import Union
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from loguru import logger

from app.utils.response_utils import (
    error_response, bad_request_response,
    not_found_response, unauthorized_response,
    forbidden_response, internal_error_response
)


class BaseCustomException(Exception):
    """自定义异常基类"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        data: Union[dict, list, None] = None
    ):
        self.message = message
        self.status_code = status_code
        self.data = data
        super().__init__(self.message)


class BusinessException(BaseCustomException):
    """业务异常"""
    pass


class ValidationException(BaseCustomException):
    """验证异常"""
    def __init__(self, message: str, data: Union[dict, list, None] = None):
        super().__init__(message, 400, data)


class AuthenticationException(BaseCustomException):
    """认证异常"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 401)


class AuthorizationException(BaseCustomException):
    """授权异常"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, 403)


class NotFoundException(BaseCustomException):
    """未找到异常"""
    def __init__(self, message: str = "数据不存在"):
        super().__init__(message, 404)


class InternalServerException(BaseCustomException):
    """内部服务器异常"""
    def __init__(self, message: str = "服务器内部错误"):
        super().__init__(message, 500)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    logger.warning(f"HTTP异常: {exc.status_code} - {exc.detail}")
    
    # 根据状态码选择响应
    if exc.status_code == 404:
        response_data = not_found_response(exc.detail)
    elif exc.status_code == 401:
        response_data = unauthorized_response(exc.detail)
    elif exc.status_code == 403:
        response_data = forbidden_response(exc.detail)
    elif exc.status_code == 422:
        response_data = bad_request_response(exc.detail, exc.detail)
    else:
        response_data = error_response(exc.detail, exc.status_code)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """请求验证异常处理器"""
    logger.warning(f"请求验证异常: {exc.errors()}")
    
    # 提取验证错误详情
    error_details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        error_details.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    response_data = bad_request_response(
        "请求参数验证失败",
        error_details
    )
    
    return JSONResponse(
        status_code=422,
        content=response_data
    )


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """值异常处理器"""
    logger.warning(f"值异常: {str(exc)}")
    
    response_data = bad_request_response(str(exc))
    
    return JSONResponse(
        status_code=400,
        content=response_data
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """数据库完整性异常处理器"""
    logger.error(f"数据库完整性异常: {str(exc)}")
    
    # 尝试提取具体的错误信息
    error_message = "数据完整性约束错误"
    if "UNIQUE constraint" in str(exc):
        error_message = "数据已存在，违反唯一性约束"
    elif "FOREIGN KEY constraint" in str(exc):
        error_message = "外键约束错误"
    elif "NOT NULL constraint" in str(exc):
        error_message = "字段不能为空"
    
    response_data = bad_request_response(error_message)
    
    return JSONResponse(
        status_code=400,
        content=response_data
    )


async def runtime_error_handler(request: Request, exc: RuntimeError) -> JSONResponse:
    """运行时异常处理器"""
    logger.error(f"运行时异常: {str(exc)}")
    
    response_data = internal_error_response("运行时错误")
    
    return JSONResponse(
        status_code=500,
        content=response_data
    )


async def custom_exception_handler(request: Request, exc: BaseCustomException) -> JSONResponse:
    """自定义异常处理器"""
    logger.warning(f"自定义异常: {exc.message}")
    
    response_data = error_response(exc.message, exc.status_code, exc.data)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    logger.error(f"未处理的异常: {type(exc).__name__}: {str(exc)}")
    
    # 在开发环境中返回详细错误信息，生产环境中返回通用错误信息
    import os
    is_development = os.getenv("DEBUG", "false").lower() == "true"
    
    if is_development:
        error_message = f"{type(exc).__name__}: {str(exc)}"
        error_data = {
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "args": list(map(str, exc.args)) if exc.args else None
        }
    else:
        error_message = "服务器内部错误"
        error_data = None
    
    response_data = internal_error_response(error_message, error_data)
    
    return JSONResponse(
        status_code=500,
        content=response_data
    )


def setup_exception_handlers(app):
    """设置异常处理器"""
    
    # 注册内置异常处理器
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(RuntimeError, runtime_error_handler)
    
    # 注册自定义异常处理器
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    
    # 注册通用异常处理器（必须放在最后）
    app.add_exception_handler(Exception, generic_exception_handler)
    
    logger.info("全局异常处理器已设置完成")