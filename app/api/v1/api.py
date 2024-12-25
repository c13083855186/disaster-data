from fastapi import APIRouter
from app.api.v1.endpoints import region, upload, search, send, data

api_router = APIRouter()

api_router.include_router(region.router, prefix="/regions", tags=["地区数据"])
api_router.include_router(upload.router, prefix="/data/upload", tags=["数据接收"])
#api_router.include_router(search.router, prefix="/data/search", tags=["数据查找"])
api_router.include_router(send.router, prefix="/data/send", tags=["数据发送"]) 
api_router.include_router(data.router, prefix="/data", tags=["数据管理"])