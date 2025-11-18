# 会议室预约系统

一个基于 Vue3 + FastAPI 的会议室预约管理系统，支持用户管理、会议室管理和预约管理功能。

## 项目结构

```
bookitem/
├── backend/                 # 后端项目 (FastAPI)
│   ├── main.py             # 主程序入口
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic schemas
│   ├── routers/            # API 路由
│   │   ├── users.py        # 用户管理路由
│   │   ├── rooms.py        # 会议室管理路由
│   │   └── bookings.py     # 预约管理路由
│   └── requirements.txt    # Python 依赖
│
└── frontend/               # 前端项目 (Vue3)
    ├── src/
    │   ├── main.js         # 入口文件
    │   ├── App.vue         # 根组件
    │   ├── router/         # 路由配置
    │   ├── api/            # API 接口
    │   └── views/          # 页面组件
    │       ├── Home.vue    # 首页
    │       ├── Users.vue   # 用户管理
    │       ├── Rooms.vue   # 会议室管理
    │       └── Bookings.vue # 预约管理
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 功能特性

### 用户管理
- ✅ 创建用户（用户名、邮箱、电话、密码）
- ✅ 查看用户列表
- ✅ 删除用户
- ✅ 用户状态管理

### 会议室管理
- ✅ 添加会议室（名称、位置、容纳人数、描述）
- ✅ 编辑会议室信息
- ✅ 删除会议室
- ✅ 查看会议室列表
- ✅ 会议室状态管理

### 预约管理
- ✅ 创建预约（选择用户、会议室、时间段、预约目的）
- ✅ 时间冲突检测
- ✅ 取消预约
- ✅ 删除预约
- ✅ 查看所有预约
- ✅ 按用户查看预约
- ✅ 按会议室查看预约

## 技术栈

### 后端
- **FastAPI**: 现代化、高性能的 Python Web 框架
- **SQLAlchemy**: Python SQL 工具包和 ORM
- **Pydantic**: 数据验证库
- **SQLite**: 轻量级数据库
- **Passlib**: 密码哈希库

### 前端
- **Vue 3**: 渐进式 JavaScript 框架
- **Vue Router**: 官方路由管理器
- **Pinia**: Vue 状态管理库
- **Element Plus**: Vue 3 UI 组件库
- **Axios**: HTTP 客户端
- **Vite**: 下一代前端构建工具

## 安装和运行

### 后端安装

#### 使用 uv 和 pyenv (推荐)

1. 进入后端目录：
```bash
cd backend
```

2. 设置 Python 版本（使用 pyenv）：
```bash
pyenv local 3.11.13  # 或其他已安装的 3.11+ 版本
```

3. 创建虚拟环境（使用 uv）：
```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

4. 安装依赖：
```bash
uv pip install -r requirements.txt
uv pip install email-validator  # 额外依赖
```

5. 初始化测试数据（首次运行）：
```bash
python init_data.py
```

6. 运行后端服务：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 传统方式

也可以使用传统的 pip 安装：
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install email-validator
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将运行在 http://localhost:8000

API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 前端安装

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run dev
```

前端服务将运行在 http://localhost:5173

## API 接口文档

### 用户 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/users | 获取用户列表 |
| GET | /api/users/{id} | 获取指定用户 |
| POST | /api/users | 创建用户 |
| DELETE | /api/users/{id} | 删除用户 |

### 会议室 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/rooms | 获取会议室列表 |
| GET | /api/rooms/{id} | 获取指定会议室 |
| POST | /api/rooms | 创建会议室 |
| PUT | /api/rooms/{id} | 更新会议室 |
| DELETE | /api/rooms/{id} | 删除会议室 |

### 预约 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/bookings | 获取所有预约 |
| GET | /api/bookings/{id} | 获取指定预约 |
| GET | /api/bookings/user/{user_id} | 获取用户的预约 |
| GET | /api/bookings/room/{room_id} | 获取会议室的预约 |
| POST | /api/bookings | 创建预约 |
| PUT | /api/bookings/{id}/cancel | 取消预约 |
| DELETE | /api/bookings/{id} | 删除预约 |

## 数据模型

### User（用户）
```python
{
  "id": int,
  "username": str,
  "email": str,
  "phone": str (可选),
  "is_active": bool,
  "created_at": datetime
}
```

### Room（会议室）
```python
{
  "id": int,
  "name": str,
  "location": str,
  "capacity": int,
  "description": str (可选),
  "is_available": bool,
  "created_at": datetime
}
```

### Booking（预约）
```python
{
  "id": int,
  "user_id": int,
  "room_id": int,
  "start_time": datetime,
  "end_time": datetime,
  "purpose": str (可选),
  "status": str (pending/confirmed/cancelled),
  "created_at": datetime
}
```

## 使用说明

1. **启动服务**：先启动后端服务，再启动前端服务

2. **添加用户**：进入"用户管理"页面，点击"添加用户"按钮创建用户

3. **添加会议室**：进入"会议室管理"页面，点击"添加会议室"按钮创建会议室

4. **创建预约**：
   - 进入"预约管理"页面
   - 点击"创建预约"按钮
   - 选择用户、会议室和时间段
   - 填写预约目的
   - 系统会自动检测时间冲突

5. **管理预约**：
   - 可以取消已确认的预约
   - 可以删除预约记录
   - 查看所有预约的详细信息

## 注意事项

- 后端默认使用 SQLite 数据库，数据文件为 `booking_system.db`
- 密码使用 bcrypt 加密存储
- 预约时会自动检测时间冲突
- 不能预约过去的时间
- 会议室被禁用时无法创建新预约

## 开发建议

- 后端修改代码后会自动重载（--reload）
- 前端修改代码后会自动热更新
- 建议使用 Chrome DevTools 进行前端调试
- 后端 API 可以通过 Swagger UI 进行测试

## 扩展功能建议

- [ ] 用户登录认证（JWT Token）
- [ ] 用户权限管理
- [ ] 预约审批流程
- [ ] 邮件通知功能
- [ ] 会议室设备管理
- [ ] 预约统计报表
- [ ] 日历视图展示
- [ ] 移动端适配

## 许可证

MIT License

