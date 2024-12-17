# app/crud.py

from sqlalchemy.orm import Session
from app.models import DataSource, DisasterData, DataRequest
from app.schemas import DataSourceCreate, DisasterDataCreate, DataRequestCreate
from fastapi import HTTPException, status

# 数据源 CRUD 操作
def create_data_source(db: Session, data_source: DataSourceCreate):
    db_source = DataSource(name=data_source.name, description=data_source.description)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

def get_data_source(db: Session, source_id: int):
    db_source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="数据来源不存在")
    return db_source

def get_data_source_by_name(db: Session, source_name: str):
    db_source = db.query(DataSource).filter(DataSource.name == source_name).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="数据来源名称不存在")
    return db_source

# 灾情数据 CRUD 操作
def create_disaster_data(db: Session, disaster_data: DisasterDataCreate, encoded_content: str):
    db_data = DisasterData(
        integrated_code=disaster_data.integrated_code,
        earthquake_code=disaster_data.earthquake_code,
        source_code=disaster_data.source_code,
        carrier_code=disaster_data.carrier_code,
        disaster_code=disaster_data.disaster_code,
        data_type=disaster_data.data_type,
        content=disaster_data.content,
        encoded_content=encoded_content,
        source_id=disaster_data.source_id
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_disaster_data(db: Session, data_id: int):
    db_data = db.query(DisasterData).filter(DisasterData.id == data_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="灾情数据不存在")
    return db_data

def search_disaster_data(db: Session, filters: dict, skip: int = 0, limit: int = 10):
    query = db.query(DisasterData)
    if "source_id" in filters:
        query = query.filter(DisasterData.source_id == filters["source_id"])
    if "data_type" in filters:
        query = query.filter(DisasterData.data_type == filters["data_type"])
    if "start_time" in filters and "end_time" in filters:
        query = query.filter(DisasterData.timestamp.between(filters["start_time"], filters["end_time"]))
    results = query.offset(skip).limit(limit).all()
    return results

# 数据请求 CRUD 操作
def create_data_request(db: Session, data_request: DataRequestCreate):
    db_request = DataRequest(
        requestor=data_request.requestor,
        data_id=data_request.data_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
