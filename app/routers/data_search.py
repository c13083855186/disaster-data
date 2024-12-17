# app/routers/data_search.py

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.schemas import DisasterData
from app.crud import search_disaster_data
from app.dependencies import get_db
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.get("/data/search/")
async def search_data(
    source_id: Optional[int] = Query(None, examples={"default": 1}),
    data_type: Optional[str] = Query(None, examples={"default": "text"}),
    start_time: Optional[datetime] = Query(None, examples={"default": "2021-05-22T00:00:00"}),
    end_time: Optional[datetime] = Query(None, examples={"default": "2021-05-23T00:00:00"}),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    filters = {}
    if source_id:
        filters["source_id"] = source_id
    if data_type:
        filters["data_type"] = data_type
    if start_time and end_time:
        filters["start_time"] = start_time
        filters["end_time"] = end_time
    
    results = search_disaster_data(db, filters, skip, limit)
    if not results:
        raise HTTPException(status_code=404, detail="未找到符合条件的数据")
    return results
