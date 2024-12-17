# app/main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import data_upload_router, data_search_router, data_send_router
from fastapi.middleware.cors import CORSMiddleware
import os

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI()

# 允许跨域请求（根据需要配置）
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    # 添加其他允许的源
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含所有路由
app.include_router(data_upload_router, prefix="/api/data/upload", tags=["数据接收"])
app.include_router(data_search_router, prefix="/api/data/search", tags=["数据查找"])
app.include_router(data_send_router, prefix="/api/data/send", tags=["数据发送"])

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)
