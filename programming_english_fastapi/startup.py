"""Uvicorn启动脚本"""
import uvicorn
from app.core.config import SERVER_HOST, SERVER_PORT, SERVER_RELOAD, SERVER_LOG_LEVEL
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=SERVER_RELOAD,
        log_level=SERVER_LOG_LEVEL
    )