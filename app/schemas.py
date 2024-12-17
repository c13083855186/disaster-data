# app/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# 数据源 schemas
class DataSourceBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "后方地震应急指挥部"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "负责收集和上报灾情数据"})

class DataSourceCreate(DataSourceBase):
    pass

class DataSource(DataSourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# 灾情数据 schemas
class DisasterDataBase(BaseModel):
    integrated_code: str = Field(..., json_schema_extra={"example": "63262620020620210100001010101"})
    earthquake_code: str = Field(..., json_schema_extra={"example": "63262620020620210100"})
    source_code: str = Field(..., json_schema_extra={"example": "100"})
    carrier_code: str = Field(..., json_schema_extra={"example": "1"})
    disaster_code: str = Field(..., json_schema_extra={"example": "010101"})
    data_type: str = Field(..., json_schema_extra={"example": "text"})

class DisasterDataCreate(DisasterDataBase):
    content: Optional[str] = Field(None, json_schema_extra={"example": "一般损坏面积：200平方米"})

class DisasterData(DisasterDataBase):
    id: int
    encoded_content: Optional[str] = Field(None, json_schema_extra={"example": "..."})
    timestamp: datetime
    created_at: datetime
    updated_at: datetime
    source_id: int

    model_config = ConfigDict(from_attributes=True)

# 数据请求 schemas
class DataRequestBase(BaseModel):
    requestor: str = Field(..., json_schema_extra={"example": "用户A"})
    data_id: int = Field(..., json_schema_extra={"example": 1})

class DataRequestCreate(DataRequestBase):
    pass

class DataRequest(DataRequestBase):
    id: int
    request_time: datetime

    model_config = ConfigDict(from_attributes=True)
