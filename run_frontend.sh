#!/bin/bash

echo "🚀 启动会议室预约系统前端..."
echo ""

cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖..."
    npm install
    echo ""
fi

echo "✅ 前端准备完成！"
echo ""
echo "🚀 启动前端服务..."
npm run dev

