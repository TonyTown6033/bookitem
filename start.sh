#!/bin/bash

echo "🚀 启动会议室预约系统..."

# 启动后端
echo "📦 启动后端服务 (FastAPI)..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✅ 后端服务启动成功 (PID: $BACKEND_PID) - http://localhost:8000"

cd ..

# 启动前端
echo "📦 启动前端服务 (Vue3)..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装依赖..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
echo "✅ 前端服务启动成功 (PID: $FRONTEND_PID) - http://localhost:5173"

echo ""
echo "🎉 系统启动完成！"
echo "📖 前端地址: http://localhost:5173"
echo "📖 后端地址: http://localhost:8000"
echo "📖 API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待进程
wait

