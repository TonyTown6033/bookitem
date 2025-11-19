# 📚 项目文档索引

## 核心文档

### 📖 README.md
项目主文档，包含：
- 项目介绍
- 功能特性
- 快速开始
- 技术栈
- 项目结构

### 🚀 start.sh / start.bat
一键启动脚本
- 同时启动前后端服务
- 自动激活虚拟环境
- 后台运行

## 技术文档

### 🔧 REFACTORING_GUIDE.md
**代码重构完整指南**
- 重构前后对比
- 新增模块说明
- 最佳实践
- 使用示例

**重构成果**：
- 前端代码量减少 72% (900行 → 250行)
- 后端引入服务层架构
- 工具函数模块化
- 代码可维护性大幅提升

### 🎨 UI_OPTIMIZATION.md
**UI 设计优化说明**
- 半小时网格系统（48格）
- 高端优雅配色方案
- 动画效果详解
- 视觉层次设计

**设计主题**：
- 紫色渐变 (#667eea → #764ba2)
- 现代化圆角设计
- 深度阴影效果
- Element Plus 图标系统

### 🖱️ CLICK_MODE_OPTIMIZATION.md
**点击模式交互优化**
- 从拖拽改为点击选择
- 移动端友好设计
- 实时预览反馈
- 完整的视觉提示

**交互流程**：
1. 第一次点击 → 显示脉动标记点
2. 鼠标移动 → 实时预览区间
3. 第二次点击 → 确认时间区间

### ⏰ TIMEZONE_FIX_V2.md
**时区问题修复详解**
- 问题根因分析
- 修复方案详解
- 时区处理流程
- 最佳实践

**核心改进**：
- 统一时区处理
- 前后端时间一致
- UTC 标准化存储

---

## 文档组织

```
bookitem/
├── README.md                    # 项目主文档 ⭐
├── DOCS.md                      # 本文档（文档索引）
├── REFACTORING_GUIDE.md         # 重构指南 🔧
├── UI_OPTIMIZATION.md           # UI优化说明 🎨
├── CLICK_MODE_OPTIMIZATION.md   # 交互优化说明 🖱️
├── TIMEZONE_FIX_V2.md           # 时区修复说明 ⏰
├── start.sh                     # 启动脚本（Unix/Mac）
└── start.bat                    # 启动脚本（Windows）
```

---

## 快速导航

### 我想了解...

**项目整体情况** → README.md

**如何启动项目** → README.md 快速开始 或 start.sh

**代码如何重构的** → REFACTORING_GUIDE.md

**UI设计细节** → UI_OPTIMIZATION.md

**点击交互如何实现** → CLICK_MODE_OPTIMIZATION.md

**时区问题如何解决** → TIMEZONE_FIX_V2.md

**前端工具函数** → frontend/src/utils/timeUtils.js

**前端 Composables** → frontend/src/composables/

**后端服务层** → backend/services/

**后端工具模块** → backend/utils/

---

## 代码架构

### 前端架构

```
frontend/src/
├── components/          # 组件
│   └── TimelineSelector.vue  (250行，简化72%)
├── composables/         # 组合式函数 ✨
│   ├── useBookingData.js
│   └── useTimelineSelection.js
├── utils/              # 工具函数 ✨
│   └── timeUtils.js    (20+个纯函数)
├── constants/          # 常量配置 ✨
│   └── booking.js
└── views/              # 页面视图
    ├── Home.vue
    ├── RoomBooking.vue
    ├── Bookings.vue
    ├── Rooms.vue
    └── Users.vue
```

### 后端架构

```
backend/
├── services/           # 服务层 ✨
│   ├── booking_service.py
│   ├── user_service.py
│   └── room_service.py
├── utils/              # 工具模块 ✨
│   ├── timezone.py
│   └── validators.py
├── routers/            # 路由层
│   ├── bookings.py
│   ├── users.py
│   └── rooms.py
├── models.py           # 数据模型
├── schemas.py          # Pydantic模式
└── database.py         # 数据库配置
```

---

## 技术栈

### 前端
- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus
- **构建**: Vite
- **路由**: Vue Router
- **HTTP**: Axios

### 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite
- **验证**: Pydantic
- **认证**: passlib + bcrypt

---

## 开发规范

### 代码风格
- **单一职责**: 每个模块/函数只做一件事
- **DRY原则**: Don't Repeat Yourself
- **纯函数优先**: 无副作用，易测试
- **命名清晰**: 见名知意

### 模块化原则
1. 工具函数 → utils/
2. 业务逻辑 → services/ (后端) 或 composables/ (前端)
3. 常量配置 → constants/
4. 组件/路由 → 各自目录

---

## 更新日期

2025-11-19

---

**文档齐全，代码优雅！** ✨

