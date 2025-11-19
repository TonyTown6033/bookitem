#!/bin/bash

echo "🚀 启动会议室预约系统..."

# 清理旧进程
echo "🧹 清理旧进程..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# 检查 pyenv 是否安装
if ! command -v pyenv &> /dev/null; then
    echo "❌ 错误: pyenv 未安装"
    echo "请先安装 pyenv: https://github.com/pyenv/pyenv"
    exit 1
fi

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ 错误: uv 未安装"
    echo "请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 启动后端
echo "📦 启动后端服务 (FastAPI)..."
cd backend

# 确保使用正确的 Python 版本
if [ -f ".python-version" ]; then
    PYTHON_VERSION=$(cat .python-version)
    echo "🐍 使用 Python 版本: $PYTHON_VERSION"
    
    # 检查该版本是否已安装
    if ! pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"; then
        echo "⚙️  安装 Python ${PYTHON_VERSION}..."
        pyenv install ${PYTHON_VERSION}
    fi
else
    echo "⚠️  未找到 .python-version 文件，使用系统默认 Python"
fi

# 使用 uv 创建/同步虚拟环境
if [ ! -d ".venv" ]; then
    echo "⚙️  创建虚拟环境 (使用 uv)..."
    uv venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 使用 uv 安装依赖
echo "📥 安装/更新依赖 (使用 uv)..."
uv pip install -r requirements.txt

# 启动后端服务
echo "🚀 启动后端服务..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ 后端服务启动成功 (PID: $BACKEND_PID) - http://localhost:8000"

cd ..

# 启动前端
echo "📦 启动前端服务 (Vue3)..."
cd frontend

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: npm 未安装"
    echo "请先安装 Node.js 和 npm"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "📥 安装前端依赖..."
    npm install
fi

echo "🚀 启动前端服务..."
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ 前端服务启动成功 (PID: $FRONTEND_PID) - http://localhost:5173"

cd ..

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉 系统启动完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📖 前端地址: http://localhost:5173"
echo "  📖 后端地址: http://localhost:8000"
echo "  📖 API文档:  http://localhost:8000/docs"
echo ""
echo "  📝 后端日志: backend.log"
echo "  📝 前端日志: frontend/frontend.log"
echo ""
echo "  🛑 停止服务: Ctrl+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 捕获 Ctrl+C 信号，优雅退出
trap 'echo ""; echo "🛑 停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# 等待进程
wait

