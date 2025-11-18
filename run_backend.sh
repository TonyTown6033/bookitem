#!/bin/bash

echo "🚀 启动会议室预约系统后端..."
echo ""

cd backend

# 检查 Python 版本
if [ -f ".python-version" ]; then
    PYTHON_VERSION=$(cat .python-version)
    echo "📌 使用 Python 版本: $PYTHON_VERSION"
    
    # 检查是否已安装该版本
    if ! pyenv versions | grep -q "$PYTHON_VERSION"; then
        echo "⚠️  Python $PYTHON_VERSION 未安装，正在安装..."
        pyenv install $PYTHON_VERSION
    fi
    
    # 设置本地版本
    pyenv local $PYTHON_VERSION
fi

echo "🐍 Python 版本:"
python --version
echo ""

# 使用 uv 创建虚拟环境并安装依赖
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    uv venv
fi

echo "📦 安装依赖..."
uv pip install -e .

# 初始化数据库和测试数据
if [ ! -f "booking_system.db" ]; then
    echo ""
    echo "📊 初始化测试数据..."
    source .venv/bin/activate
    python init_data.py
    echo ""
fi

echo "✅ 后端准备完成！"
echo ""
echo "🚀 启动后端服务..."
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

