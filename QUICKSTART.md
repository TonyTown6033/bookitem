# 快速开始指南

## 前提条件

- Python 3.8+ 
- Node.js 16+
- npm 或 yarn

## 一键启动（推荐）

### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

### Windows
```bash
start.bat
```

## 手动启动

### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（首次运行）
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端

打开新的终端窗口：

```bash
# 进入前端目录
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

## 访问系统

- 前端界面: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 测试数据

### 创建测试用户
1. 访问前端页面
2. 点击"用户管理"
3. 添加用户：
   - 用户名: admin
   - 邮箱: admin@example.com
   - 电话: 13800138000
   - 密码: admin123

### 创建测试会议室
1. 点击"会议室管理"
2. 添加会议室：
   - 名称: 大会议室
   - 位置: 1楼101室
   - 容纳人数: 20
   - 描述: 配备投影仪和白板

### 创建测试预约
1. 点击"预约管理"
2. 点击"创建预约"
3. 选择用户、会议室和时间段
4. 填写预约目的，提交

## 常见问题

### 1. 端口被占用
如果 8000 或 5173 端口被占用：
- 后端：修改启动命令中的 `--port 8000` 为其他端口
- 前端：修改 `vite.config.js` 中的 `server.port`

### 2. 数据库初始化失败
删除 `backend/booking_system.db` 文件，重新启动后端服务

### 3. 前端无法连接后端
检查 `frontend/src/api/index.js` 中的 `baseURL` 是否正确

### 4. 依赖安装失败
- Python: 尝试使用 `pip install --upgrade pip` 更新 pip
- Node: 尝试清除缓存 `npm cache clean --force`

## 开发建议

- 使用 Chrome DevTools 调试前端
- 使用 http://localhost:8000/docs 测试后端 API
- 修改代码后会自动热更新，无需重启

## 下一步

- 查看完整文档: [README.md](README.md)
- 了解 API 接口详情
- 开始自定义开发

