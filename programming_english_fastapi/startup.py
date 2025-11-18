"""Uvicorn启动脚本"""
import uvicorn
from app.core.config import settings
from app.core.app import create_app
from app.api.v1.routes import api_router
from app.db.database import create_db_and_tables

# 创建应用实例
app = create_app()

# 包含API路由
app.include_router(api_router)

# 创建数据库表
create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run(
        "startup:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )