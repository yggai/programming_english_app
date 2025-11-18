# Programming English FastAPI

一个基于 FastAPI 的编程英语学习后端服务，遵循 TDD 开发规范。

## 项目结构

```
programming_english_fastapi/
├── app/                          # 应用主目录
│   ├── __init__.py
│   ├── main.py                   # FastAPI应用入口
│   ├── api/                      # API路由
│   │   ├── __init__.py
│   │   └── v1/                   # API版本1
│   │       ├── __init__.py
│   │       ├── words.py          # 单词相关API
│   │       ├── root.py           # 根路径API
│   │       ├── routes.py         # 路由汇总
│   │       └── legacy_words.py   # 兼容API
│   ├── core/                      # 核心配置
│   │   ├── __init__.py
│   │   ├── settings.py           # 应用配置
│   │   └── security.py           # 安全相关
│   ├── db/                        # 数据库相关
│   │   ├── __init__.py
│   │   └── database.py           # 数据库连接
│   ├── models/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py               # 用户模型
│   │   └── word.py               # 单词模型
│   ├── schemas/                   # Pydantic模式
│   ├── services/                  # 业务逻辑服务
│   │   ├── __init__.py
│   │   └── word_service.py       # 单词服务
│   └── utils/                     # 工具函数
│       ├── __init__.py
│       └── deps.py               # 依赖注入
├── tests/                         # 测试目录
│   ├── __init__.py
│   ├── conftest.py               # pytest配置
│   ├── test_main.py              # 主应用测试
│   ├── unit/                     # 单元测试
│   └── integration/              # 集成测试
├── .env.example                  # 环境变量示例
├── requirements.txt              # 依赖列表
├── pytest.ini                    # 测试配置
└── README.md                     # 项目说明
```

## 启动方式

### 1. 使用uvicorn直接启动（推荐）

```bash
# 开发环境
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产环境
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. 使用启动脚本

```bash
python startup.py
```

### 3. 使用命令行参数

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

## 环境配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，设置相应的配置
```

## API文档

启动应用后，可以访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/
pytest tests/integration/

# 显示详细输出
pytest -v

# 显示覆盖率
pytest --cov=app
```