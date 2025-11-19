# 网络配置指南 - 解决admin登录网络错误

## 🔧 问题分析

admin登录提示"网络错误"通常由以下原因引起：

1. **API地址配置错误** - 使用localhost在模拟器中无法访问主机
2. **网络权限缺失** - Android/iOS缺少网络权限
3. **服务器未运行** - 后端服务未启动或端口未开放
4. **防火墙/代理问题** - 网络环境限制

## ✅ 已修复的问题

### 1. API地址配置
**已修复**：
- Android模拟器: 使用 `http://10.0.2.2:8000`
- iOS模拟器: 使用 `http://localhost:8000`

### 2. 网络权限配置
**已添加**：
- Android权限: `INTERNET` 和 `ACCESS_NETWORK_STATE`
- iOS: 默认支持localhost访问

### 3. 增强错误处理
**已实现**：
- 详细的网络错误提示
- 连接超时处理
- 服务器状态检查

## 🚀 使用指南

### 快速开始

1. **确保后端服务运行**
   ```bash
   # 在后端目录运行
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **检查服务器状态**
   - 登录页面会显示"服务器连接正常"或"无法连接服务器"
   - 点击"需要帮助？"查看详细调试信息

3. **测试连接**
   ```bash
   # 测试API连通性
   curl http://localhost:8000/api/v1/health
   ```

### 环境切换

根据你的开发环境，修改 `lib/core/constants/app_constants.dart`：

```dart
// Android模拟器
static const String baseUrl = 'http://10.0.2.2:8000';

// iOS模拟器
static const String baseUrl = 'http://localhost:8000';

// 真机调试（替换为你的电脑IP）
static const String baseUrl = 'http://192.168.x.x:8000';
```

### 常见错误排查

| 错误提示 | 可能原因 | 解决方案 |
|---------|----------|----------|
| 连接超时 | 服务器未启动 | 启动后端服务 |
| 无法连接服务器 | IP地址错误 | 检查baseUrl配置 |
| 网络权限被拒绝 | 缺少权限声明 | 确认AndroidManifest.xml权限 |
| 跨域请求失败 | CORS配置问题 | 检查后端CORS设置 |

## 🔍 调试工具

登录页面已添加网络诊断功能：
- 实时显示服务器连接状态
- 详细的错误提示信息
- 一键网络测试

## 📱 不同平台配置

### Android
- 模拟器使用 `10.0.2.2`
- 真机使用电脑局域网IP
- 已添加网络权限

### iOS
- 模拟器使用 `localhost`
- 真机需要配置App Transport Security

### Web
- 使用 `localhost:8000`
- 可能需要处理CORS

## 🛠️ 测试命令

```bash
# 测试服务器连通性
curl http://10.0.2.2:8000/api/v1/health

# 测试登录接口
curl -X POST http://10.0.2.2:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```