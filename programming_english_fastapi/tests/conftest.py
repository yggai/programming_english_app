"""测试配置模块"""

import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from fastapi.testclient import TestClient

# 测试数据库配置
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session() -> Generator[Session, None, None]:
    """覆盖数据库会话"""
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """设置测试数据库"""
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """创建测试数据库会话（SQLModel Session，每个测试用事务隔离）"""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """创建测试客户端"""
    # 延迟导入避免循环依赖
    from app.main import app
    from app.db.database import get_session
    
    app.dependency_overrides[get_session] = lambda: db_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def user_service(db_session: Session):
    """创建用户服务实例"""
    from app.services.user_service import UserService
    return UserService(db_session)


@pytest.fixture(scope="function")
def superuser_config():
    """获取超级用户配置"""
    from app.core.config import config
    return config.get('superuser', {})


@pytest.fixture(scope="function")
def test_user_data():
    """测试用户数据"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }


@pytest.fixture(scope="function")
def test_word_data():
    """测试单词数据"""
    return {
        "word": "function",
        "translation": "函数",
        "definition": "A block of code designed to perform a particular task",
        "example": "def my_function(): print('Hello')",
        "category": "basic",
        "difficulty": "beginner"
    }