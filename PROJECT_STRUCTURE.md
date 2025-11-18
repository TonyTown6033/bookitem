# 项目结构说明

## 完整目录结构

```
bookitem/
│
├── backend/                          # 后端项目目录
│   ├── main.py                       # FastAPI 主应用程序入口
│   ├── database.py                   # 数据库连接和会话配置
│   ├── models.py                     # SQLAlchemy 数据模型定义
│   ├── schemas.py                    # Pydantic 数据验证模式
│   ├── requirements.txt              # Python 依赖包列表
│   ├── booking_system.db            # SQLite 数据库文件（运行时生成）
│   └── routers/                      # API 路由模块
│       ├── __init__.py              # 路由包初始化
│       ├── users.py                 # 用户管理 API
│       ├── rooms.py                 # 会议室管理 API
│       └── bookings.py              # 预约管理 API
│
├── frontend/                         # 前端项目目录
│   ├── index.html                    # HTML 入口文件
│   ├── package.json                  # npm 配置文件
│   ├── vite.config.js               # Vite 构建配置
│   ├── node_modules/                # npm 依赖（自动生成）
│   └── src/                         # 源代码目录
│       ├── main.js                  # Vue 应用入口
│       ├── App.vue                  # 根组件
│       ├── router/                  # 路由配置
│       │   └── index.js            # 路由定义
│       ├── api/                     # API 接口封装
│       │   └── index.js            # axios 配置和 API 方法
│       └── views/                   # 页面组件
│           ├── Home.vue            # 首页 - 系统概览
│           ├── Users.vue           # 用户管理页面
│           ├── Rooms.vue           # 会议室管理页面
│           └── Bookings.vue        # 预约管理页面
│
├── README.md                         # 项目说明文档
├── QUICKSTART.md                     # 快速开始指南
├── PROJECT_STRUCTURE.md              # 项目结构说明（本文件）
├── .gitignore                        # Git 忽略文件配置
├── start.sh                          # Linux/Mac 启动脚本
└── start.bat                         # Windows 启动脚本
```

## 后端模块说明

### main.py
- FastAPI 应用实例创建
- CORS 跨域配置
- 路由注册
- 数据库表创建

### database.py
- SQLAlchemy 引擎配置
- 数据库会话工厂
- Base 基类定义
- get_db 依赖注入函数

### models.py
数据库模型定义：
- **User**: 用户模型（id, username, email, phone, hashed_password, is_active, created_at）
- **Room**: 会议室模型（id, name, location, capacity, description, is_available, created_at）
- **Booking**: 预约模型（id, user_id, room_id, start_time, end_time, purpose, status, created_at）

### schemas.py
Pydantic 验证模式：
- **UserCreate/UserResponse**: 用户数据验证
- **RoomCreate/RoomResponse**: 会议室数据验证
- **BookingCreate/BookingResponse/BookingDetailResponse**: 预约数据验证

### routers/
API 路由模块，包含完整的 CRUD 操作：
- **users.py**: 用户的增删查改
- **rooms.py**: 会议室的增删查改
- **bookings.py**: 预约的创建、查询、取消、删除，包含时间冲突检测

## 前端模块说明

### main.js
- Vue 应用创建
- 插件注册（Router, Pinia, Element Plus）
- 全局图标注册
- 应用挂载

### App.vue
- 应用根组件
- 全局导航栏
- 路由出口
- 全局样式

### router/index.js
路由配置：
- `/` - 首页
- `/users` - 用户管理
- `/rooms` - 会议室管理
- `/bookings` - 预约管理

### api/index.js
API 接口封装：
- axios 实例配置
- 请求/响应拦截器
- userAPI: 用户相关接口
- roomAPI: 会议室相关接口
- bookingAPI: 预约相关接口

### views/
页面组件：
- **Home.vue**: 
  - 显示系统统计信息
  - 快捷入口卡片
  - 数据概览

- **Users.vue**:
  - 用户列表展示（表格）
  - 添加用户对话框
  - 删除用户功能

- **Rooms.vue**:
  - 会议室列表展示（表格）
  - 添加/编辑会议室对话框
  - 删除会议室功能

- **Bookings.vue**:
  - 预约列表展示（表格）
  - 创建预约对话框（带时间选择器）
  - 取消/删除预约功能
  - 显示用户和会议室详情

## 数据流程

### 创建预约流程
1. 用户在前端填写预约信息
2. 前端发送 POST 请求到 `/api/bookings`
3. 后端验证：
   - 用户和会议室是否存在
   - 时间是否有效（不能是过去时间）
   - 是否有时间冲突
4. 验证通过后创建预约记录
5. 返回预约详情给前端
6. 前端更新列表并显示成功消息

### 时间冲突检测
- 后端使用 SQL 查询检测时间重叠
- 检测规则：
  - 新预约开始时间在已有预约时间段内
  - 新预约结束时间在已有预约时间段内
  - 新预约完全包含已有预约时间段
- 只检测未取消的预约

## 技术特点

### 后端特点
- RESTful API 设计
- 自动生成 API 文档（Swagger UI）
- 数据验证（Pydantic）
- ORM 操作（SQLAlchemy）
- 密码加密存储（bcrypt）
- 依赖注入模式

### 前端特点
- 组件化开发
- 响应式设计
- Element Plus UI 组件库
- 路由管理（Vue Router）
- API 统一封装
- 错误处理和用户提示
- 表单验证

## 扩展点

### 可扩展功能
1. **认证授权**: 添加 JWT Token 认证
2. **权限管理**: 基于角色的访问控制（RBAC）
3. **文件上传**: 会议室图片、用户头像
4. **通知系统**: 邮件/短信通知
5. **日历视图**: 可视化时间轴展示预约
6. **统计报表**: 预约统计、使用率分析
7. **审批流程**: 预约需要管理员审批
8. **循环预约**: 定期会议预约

### 代码扩展位置
- 后端中间件: `backend/middleware/`
- 前端组件: `frontend/src/components/`
- 前端状态管理: `frontend/src/stores/`
- 工具函数: `backend/utils/`, `frontend/src/utils/`

## 开发规范

### 后端规范
- 遵循 PEP 8 Python 编码规范
- 使用类型提示
- API 路由使用 RESTful 风格
- 统一的错误处理和响应格式

### 前端规范
- 使用 Composition API
- 组件命名采用 PascalCase
- 变量命名采用 camelCase
- 适当的注释和文档

## 性能优化建议

1. **数据库**: 添加适当的索引
2. **缓存**: Redis 缓存常用数据
3. **分页**: 大量数据时使用分页
4. **懒加载**: 前端路由懒加载
5. **图片优化**: 图片压缩和 CDN
6. **代码分割**: 按需加载组件

