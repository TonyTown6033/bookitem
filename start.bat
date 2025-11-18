@echo off
chcp 65001 >nul
echo 🚀 启动会议室预约系统...
echo.

REM 启动后端
echo 📦 启动后端服务 (FastAPI)...
cd backend
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate
pip install -q -r requirements.txt
start "Backend-FastAPI" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ✅ 后端服务启动成功 - http://localhost:8000
cd ..

REM 启动前端
echo 📦 启动前端服务 (Vue3)...
cd frontend
if not exist node_modules (
    echo 安装依赖...
    call npm install
)

start "Frontend-Vue3" cmd /k "npm run dev"
echo ✅ 前端服务启动成功 - http://localhost:5173

echo.
echo 🎉 系统启动完成！
echo 📖 前端地址: http://localhost:5173
echo 📖 后端地址: http://localhost:8000
echo 📖 API文档: http://localhost:8000/docs
echo.
pause

