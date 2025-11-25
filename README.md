# 编程英语学习APP (Programming English Learning App)

一个专为编程初学者设计的跨平台英语学习应用，帮助用户掌握编程常用英语术语，提升阅读英文编程文档的能力。

B站视频介绍：https://www.bilibili.com/video/BV1RjUDBWENa/?vd_source=5c35e5f2b07da07b061c1b2b7c0d312b


## 📱 项目概述

随着全球数字化转型的加速，编程已成为一项基础技能。然而，对于非英语母语的编程初学者来说，语言障碍是学习编程的主要挑战之一。本应用专门解决这一痛点，通过科学的记忆方法和丰富的编程场景，让用户轻松掌握编程英语。

### 🎯 核心目标

- 掌握编程常用英语术语
- 理解编程概念的英文表达
- 通过代码示例加深词汇记忆
- 提升阅读英文编程文档的能力

### 👥 目标用户

- **主要用户**：编程初学者（18-35岁）
- **次要用户**：有一定编程基础但英语水平有限的开发者
- **潜在用户**：计算机专业学生、编程培训机构学员

## 🏗️ 技术架构

### 后端技术栈

- **框架**：FastAPI (Python)
- **数据库**：PostgreSQL + Redis
- **认证**：JWT Token
- **测试**：Pytest + Pytest-asyncio
- **部署**：Docker

### 前端技术栈

- **框架**：Flutter
- **状态管理**：Provider
- **网络请求**：Dio
- **本地存储**：SharedPreferences
- **语音合成**：Flutter TTS

### 项目结构

```
programming_english_app/
├── docs/                              # 项目文档
│   └── 需求分析文档.md                # 详细需求分析
├── programming_english_fastapi/        # 后端服务
│   ├── app/                          # 应用主目录
│   │   ├── api/                      # API路由
│   │   ├── core/                     # 核心配置
│   │   ├── db/                       # 数据库相关
│   │   ├── models/                   # 数据模型
│   │   ├── services/                 # 业务逻辑
│   │   └── utils/                    # 工具函数
│   ├── tests/                        # 测试文件
│   └── requirements.txt              # Python依赖
├── programming_english_flutter/       # Flutter前端
│   ├── lib/                          # Dart源码
│   │   ├── core/                     # 核心功能
│   │   ├── features/                 # 功能模块
│   │   └── main.dart                 # 应用入口
│   ├── test/                         # 测试文件
│   └── pubspec.yaml                  # Dart依赖
└── README.md                         # 项目说明
```

## ✨ 功能特性

### ?? 核心学习功能

- **单词学习模块**
  - 编程术语词汇库
  - 单词详细信息（英文、翻译、代码示例）
  - 按编程语言和概念分类
  - 个人收藏夹

- **多样化学习模式**
  - 闪卡记忆模式
  - 互动测验模式
  - 代码阅读模式
  - 语音学习模式

- **智能进度管理**
  - 学习进度跟踪
  - 掌握程度评估
  - 个性化复习计划
  - 成就系统

### 🔧 辅助功能

- **用户系统**
  - 用户注册/登录
  - 个人资料管理
  - 学习偏好设置
  - 多设备数据同步

- **离线支持**
  - 本地缓存功能
  - 离线学习模式
  - 数据同步机制

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Flutter**: 3.2.3+
- **PostgreSQL**: 12+
- **Redis**: 6+

### 后端部署

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd programming_english_app/programming_english_fastapi
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件设置数据库连接等配置
   ```

4. **初始化数据库**
   ```bash
   python init_db.py
   ```

5. **启动服务**
   ```bash
   # 开发环境
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # 或使用启动脚本
   python startup.py
   ```

6. **访问API文档**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### 前端部署

1. **进入前端目录**
   ```bash
   cd programming_english_flutter
   ```

2. **安装依赖**
   ```bash
   flutter pub get
   ```

3. **运行应用**
   ```bash
   # 开发环境
   flutter run
   
   # 构建发布版本
   flutter build apk --release
   flutter build web --release
   ```

## 🧪 测试

### 后端测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 查看测试覆盖率
pytest --cov=app
```

### 前端测试

```bash
# 运行Flutter测试
flutter test

# 查看测试覆盖率
flutter test --coverage
```

## 📊 项目进度

### 当前版本：v1.0 (MVP)

✅ **已完成功能**
- 基础API框架搭建
- 用户认证系统
- 单词数据模型
- 基础Flutter界面
- 跨平台兼容性

🚧 **开发中功能**
- 单词学习模块
- 测验功能
- 进度跟踪系统
- 语音学习功能

📋 **计划中功能**
- 社交学习功能
- 智能推荐系统
- 高级数据分析
- 多语言支持

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下步骤：

1. **Fork** 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 **Pull Request**

### 代码规范

- Python代码遵循 **PEP 8** 规范
- Dart代码遵循 **Dart Style Guide**
- 提交信息遵循 **Conventional Commits** 规范
- 所有新功能需要包含相应的测试用例

## 📝 开发计划

### v1.1 (计划中)
- [ ] 完善单词学习功能
- [ ] 添加语音合成
- [ ] 优化用户界面
- [ ] 增加更多代码示例

### v2.0 (长期规划)
- [ ] 社交学习功能
- [ ] AI智能推荐
- [ ] 多语言界面支持
- [ ] 高级数据分析

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- **项目维护者**：[您的姓名]
- **邮箱**：[your.email@example.com]
- **项目地址**：[https://github.com/yourusername/programming_english_app]

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户。特别感谢：

- FastAPI 团队提供的优秀框架
- Flutter 团队的跨平台解决方案
- 开源社区的支持和贡献

---

**⭐ 如果这个项目对您有帮助，请给我们一个Star！**
