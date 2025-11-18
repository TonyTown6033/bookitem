from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, rooms, bookings

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="会议室预约系统",
    version="1.0.0"
)

# 配置CORS - 更宽松的配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（开发环境）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 注册路由（添加尾部斜杠）
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["会议室管理"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["预约管理"])

@app.get("/")
def read_root():
    return {"message": "欢迎使用会议室预约系统 API"}

