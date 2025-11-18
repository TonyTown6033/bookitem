# 项目文件清单

## 📁 项目目录结构

\`\`\`
bookitem/
│
├── 📚 文档文件
│   ├── README.md                 - 项目完整说明
│   ├── QUICKSTART.md             - 快速开始指南
│   ├── PROJECT_STRUCTURE.md      - 项目结构详解
│   ├── PROJECT_OVERVIEW.md       - 项目概览
│   ├── API_TESTING.md            - API 测试指南
│   ├── FEATURES.md               - 功能特性说明
│   ├── CHANGELOG.md              - 版本更新日志
│   ├── RUN_STATUS.md             - 运行状态报告
│   └── PROJECT_FILES.md          - 项目文件清单（本文件）
│
├── 🚀 启动脚本
│   ├── start.sh                  - Linux/Mac 一键启动脚本
│   ├── start.bat                 - Windows 一键启动脚本
│   ├── run_backend.sh            - 后端独立启动脚本
│   └── run_frontend.sh           - 前端独立启动脚本
│
├── 🧪 测试脚本
│   └── test_api_simple.py        - API 功能测试脚本
│
├── 🔧 配置文件
│   └── .gitignore                - Git 忽略文件配置
│
├── 🐍 后端 (backend/)
│   ├── 核心文件
│   │   ├── main.py               - FastAPI 应用入口
│   │   ├── database.py           - 数据库配置
│   │   ├── models.py             - 数据模型 (User, Room, Booking)
│   │   └── schemas.py            - Pydantic 验证模式
│   │
│   ├── 路由 (routers/)
│   │   ├── __init__.py           - 路由包初始化
│   │   ├── users.py              - 用户管理 API
│   │   ├── rooms.py              - 会议室管理 API
│   │   └── bookings.py           - 预约管理 API
│   │
│   ├── 配置文件
│   │   ├── requirements.txt      - Python 依赖列表
│   │   ├── pyproject.toml        - uv 项目配置
│   │   └── .python-version       - pyenv 版本配置
│   │
│   ├── 工具脚本
│   │   └── init_data.py          - 测试数据初始化脚本
│   │
│   └── 运行时文件（自动生成）
│       ├── .venv/                - 虚拟环境目录
│       ├── booking_system.db     - SQLite 数据库
│       └── backend.log           - 运行日志
│
└── 🎨 前端 (frontend/)
    ├── 入口文件
    │   ├── index.html            - HTML 入口
    │   ├── package.json          - npm 配置
    │   └── vite.config.js        - Vite 构建配置
    │
    ├── 源代码 (src/)
    │   ├── main.js               - Vue 应用入口
    │   ├── App.vue               - 根组件
    │   │
    │   ├── 路由 (router/)
    │   │   └── index.js          - 路由配置
    │   │
    │   ├── API (api/)
    │   │   └── index.js          - axios 配置和 API 封装
    │   │
    │   └── 页面 (views/)
    │       ├── Home.vue          - 首页
    │       ├── Users.vue         - 用户管理页
    │       ├── Rooms.vue         - 会议室管理页
    │       └── Bookings.vue      - 预约管理页
    │
    └── 运行时文件（自动生成）
        ├── node_modules/         - npm 依赖
        ├── package-lock.json     - npm 依赖锁定
        └── frontend.log          - 运行日志
\`\`\`

## 📊 文件统计

### 后端文件
- Python 源文件: 8 个
- 配置文件: 3 个
- 总代码行数: ~1200 行

### 前端文件
- Vue 组件: 5 个
- JavaScript 文件: 3 个
- 配置文件: 2 个
- 总代码行数: ~1000 行

### 文档文件
- Markdown 文档: 9 个
- 总文档行数: ~2500 行

### 脚本文件
- 启动脚本: 4 个
- 测试脚本: 1 个

## 🎯 核心文件说明

### 后端核心文件

#### main.py
- FastAPI 应用实例
- CORS 配置
- 路由注册
- 应用启动配置

#### database.py
- SQLAlchemy 引擎
- 数据库会话管理
- Base 模型基类

#### models.py
- User 模型（用户）
- Room 模型（会议室）
- Booking 模型（预约）
- 数据库关系定义

#### schemas.py
- UserCreate/UserResponse
- RoomCreate/RoomResponse
- BookingCreate/BookingResponse
- BookingDetailResponse

#### routers/users.py
- POST /api/users - 创建用户
- GET /api/users - 获取用户列表
- GET /api/users/{id} - 获取用户详情
- DELETE /api/users/{id} - 删除用户

#### routers/rooms.py
- GET /api/rooms - 获取会议室列表
- POST /api/rooms - 创建会议室
- GET /api/rooms/{id} - 获取会议室详情
- PUT /api/rooms/{id} - 更新会议室
- DELETE /api/rooms/{id} - 删除会议室

#### routers/bookings.py
- GET /api/bookings - 获取预约列表
- POST /api/bookings - 创建预约
- GET /api/bookings/{id} - 获取预约详情
- GET /api/bookings/user/{user_id} - 获取用户预约
- GET /api/bookings/room/{room_id} - 获取会议室预约
- PUT /api/bookings/{id}/cancel - 取消预约
- DELETE /api/bookings/{id} - 删除预约

### 前端核心文件

#### App.vue
- 应用根组件
- 全局导航栏
- 路由视图容器
- 全局样式

#### views/Home.vue
- 系统统计数据展示
- 快捷入口卡片
- 数据概览面板

#### views/Users.vue
- 用户列表表格
- 添加用户表单
- 用户删除功能

#### views/Rooms.vue
- 会议室列表表格
- 添加/编辑会议室表单
- 会议室删除功能

#### views/Bookings.vue
- 预约列表表格（含关联信息）
- 创建预约表单
- 时间选择器
- 取消/删除预约功能

#### api/index.js
- axios 实例配置
- API 基础 URL
- 请求/响应拦截器
- userAPI, roomAPI, bookingAPI 封装

## 🔧 配置文件说明

### backend/requirements.txt
Python 依赖包列表：
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pydantic==2.5.0
- 等其他依赖...

### backend/pyproject.toml
uv 项目配置：
- 项目元数据
- 依赖列表
- 构建系统配置

### backend/.python-version
pyenv Python 版本指定：
- 3.11.13

### frontend/package.json
npm 项目配置：
- 项目元数据
- 依赖列表（vue, element-plus, axios 等）
- 脚本命令

### frontend/vite.config.js
Vite 构建配置：
- Vue 插件
- 路径别名
- 代理配置
- 服务器配置

## 📝 文档文件说明

### README.md
- 项目介绍
- 技术栈说明
- 安装运行指南
- API 文档
- 数据模型说明

### QUICKSTART.md
- 快速开始步骤
- 测试数据说明
- 常见问题解答

### PROJECT_STRUCTURE.md
- 详细目录结构
- 模块功能说明
- 数据流程说明
- 扩展建议

### PROJECT_OVERVIEW.md
- 项目概览
- 系统架构
- 核心模块介绍
- 数据库关系图

### API_TESTING.md
- curl 测试示例
- Python 测试脚本
- JavaScript 测试示例
- 测试场景说明

### FEATURES.md
- 功能特性列表
- 业务规则说明
- UI/UX 特性
- 性能优化说明

### CHANGELOG.md
- 版本更新记录
- 新功能列表
- 未来计划

### RUN_STATUS.md
- 当前运行状态
- 测试结果报告
- 环境配置信息
- 维护命令

## 🚀 启动脚本说明

### start.sh (Linux/Mac)
- 一键启动前后端
- 自动检查依赖
- 后台运行服务

### start.bat (Windows)
- Windows 环境启动
- 打开新终端窗口
- 显示启动信息

### run_backend.sh
- 独立启动后端
- pyenv 版本设置
- uv 虚拟环境创建
- 依赖安装
- 数据初始化

### run_frontend.sh
- 独立启动前端
- npm 依赖安装
- Vite 开发服务器启动

## 🧪 测试脚本说明

### test_api_simple.py
- 服务器连接测试
- 用户管理 API 测试
- 会议室管理 API 测试
- 预约管理 API 测试
- 时间冲突检测测试

## 📏 代码质量

### 代码规范
- 后端：遵循 PEP 8
- 前端：Vue 3 风格指南
- 命名：清晰、语义化
- 注释：关键逻辑注释

### 文档质量
- 完整的项目文档
- 详细的 API 说明
- 清晰的使用指南
- 丰富的示例代码

## 🎓 学习资源

本项目包含：
- RESTful API 设计
- 前后端分离架构
- Vue 3 Composition API
- FastAPI 框架使用
- SQLAlchemy ORM
- Element Plus 组件库
- 现代化工具链（uv, pyenv, vite）

## 🔄 版本控制

建议的 .gitignore 已配置：
- Python __pycache__
- 虚拟环境 .venv/
- Node modules
- 数据库文件
- 日志文件

## 📦 部署准备

项目包含所有部署所需文件：
- 依赖配置文件
- 启动脚本
- 环境配置
- 文档说明

---

**项目总计**：
- 源代码文件：18 个
- 配置文件：7 个
- 文档文件：9 个
- 脚本文件：5 个
- 总行数：约 4700+ 行

**最后更新**：2025-11-19
