"""健康检查端点"""

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str = "1.0.0"

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    return HealthResponse(
        status="healthy",
        message="Programming English API is running"
    )

@router.get("/", response_model=HealthResponse)
async def root():
    """根路径健康检查"""
    return HealthResponse(
        status="healthy",
        message="Programming English API is running"
    )