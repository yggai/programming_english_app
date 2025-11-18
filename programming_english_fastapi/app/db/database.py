from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from ..core.config import settings

# 同步数据库引擎（用于Alembic迁移）
engine = create_engine(settings.database_url, echo=settings.debug)

# 异步数据库引擎
async_engine = create_async_engine(
    settings.database_url.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=settings.debug
)


async def get_session() -> AsyncSession:
    """获取异步数据库会话"""
    async with AsyncSession(async_engine) as session:
        yield session


def create_db_and_tables():
    """创建数据库和表"""
    SQLModel.metadata.create_all(engine)