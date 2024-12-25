from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.disaster import DisasterData
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.get("/")
async def search_data(
    data_type: Optional[str] = Query(None, description="数据类型"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    skip: int = Query(0, description="跳过记录数"),
    limit: int = Query(10, description="返回记录数"),
    db: Session = Depends(get_db)
):
    query = db.query(DisasterData)
    
    # 应用过滤条件
    if data_type:
        query = query.filter(DisasterData.data_type == data_type)
    if start_time and end_time:
        query = query.filter(DisasterData.timestamp.between(start_time, end_time))
    
    # 排序、分页
    total = query.count()
    results = query.order_by(DisasterData.timestamp.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": results,
        "skip": skip,
        "limit": limit
    } 