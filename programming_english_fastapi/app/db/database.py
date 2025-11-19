"""数据库连接配置"""
from sqlmodel import SQLModel, Session, create_engine
from ..core.config import DATABASE_URL, DATABASE_ECHO

# 同步数据库引擎
engine = create_engine(DATABASE_URL, echo=DATABASE_ECHO)


def get_session() -> Session:
    """获取同步数据库会话"""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """创建数据库和表"""
    SQLModel.metadata.create_all(engine)