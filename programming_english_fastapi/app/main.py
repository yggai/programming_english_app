"""FastAPI应用入口模块"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import api_router
from app.db.database import create_db_and_tables

# 创建应用实例
app = FastAPI(
    title="Programming English API",
    description="A FastAPI application for learning programming English",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router)

# 创建数据库表
create_db_and_tables()

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件"""
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件"""
    pass