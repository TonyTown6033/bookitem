#!/bin/bash

echo "🚀 部署会议室预约系统到生产环境..."

# 检查必要工具
if ! command -v pyenv &> /dev/null; then
    echo "❌ 错误: pyenv 未安装"
    exit 1
fi

if ! command -v uv &> /dev/null; then
    echo "❌ 错误: uv 未安装"
    exit 1
fi

if ! command -v nginx &> /dev/null; then
    echo "⚠️  警告: nginx 未安装，建议安装 nginx 作为反向代理"
fi

# 1. 构建前端
echo "📦 构建前端..."
cd frontend
npm install
npm run build
cd ..

# 2. 部署后端
echo "📦 部署后端..."
cd backend

# 设置 Python 环境
if [ -f ".python-version" ]; then
    PYTHON_VERSION=$(cat .python-version)
    echo "🐍 使用 Python 版本: $PYTHON_VERSION"
    
    if ! pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"; then
        echo "⚙️  安装 Python ${PYTHON_VERSION}..."
        pyenv install ${PYTHON_VERSION}
    fi
fi

# 创建生产环境虚拟环境
if [ ! -d ".venv" ]; then
    echo "⚙️  创建生产环境虚拟环境..."
    uv venv
fi

source .venv/bin/activate
uv pip install -r requirements.txt

# 使用 gunicorn 启动（生产环境）
echo "🚀 启动生产环境后端服务..."
if ! command -v gunicorn &> /dev/null; then
    echo "📥 安装 gunicorn..."
    uv pip install gunicorn uvicorn[standard]
fi

# 停止旧进程
pkill -f "gunicorn" 2>/dev/null

# 启动 gunicorn（4个worker，绑定到所有网络接口）
gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --daemon \
    --access-logfile ../access.log \
    --error-logfile ../error.log \
    --pid ../gunicorn.pid

echo "✅ 后端服务启动成功 (4 workers)"

cd ..

# 3. 配置说明
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉 部署完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📦 前端构建产物: frontend/dist/"
echo "  🚀 后端服务: http://0.0.0.0:8000"
echo ""
echo "  📝 配置 Nginx 反向代理（推荐）:"
echo "     1. 编辑 /etc/nginx/sites-available/bookitem"
echo "     2. 重启 nginx: sudo systemctl restart nginx"
echo ""
echo "  📝 或者直接访问:"
echo "     • 后端 API: http://你的服务器IP:8000"
echo "     • 使用 nginx 提供前端静态文件"
echo ""
echo "  🛑 停止服务:"
echo "     kill \$(cat gunicorn.pid)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

