# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    disaster_data = relationship("DisasterData", back_populates="source")

class DisasterData(Base):
    __tablename__ = "disaster_data"
    
    id = Column(Integer, primary_key=True, index=True)
    integrated_code = Column(String(36), unique=True, index=True, nullable=False)  # 一体化编码
    earthquake_code = Column(String(26), nullable=False)  # 震情编码 (26位)
    source_code = Column(String(3), nullable=False)  # 来源编码 (3位)
    carrier_code = Column(String(1), nullable=False)  # 载体编码 (1位)
    disaster_code = Column(String(6), nullable=False)  # 灾情编码 (6位)
    data_type = Column(String(20), nullable=False)  # 数据类型
    content = Column(Text, nullable=True)  # 原始内容或文件路径
    encoded_content = Column(Text, nullable=True)  # 编码后的内容
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    source = relationship("DataSource", back_populates="disaster_data")
    
    data_requests = relationship("DataRequest", back_populates="data")

class DataRequest(Base):
    __tablename__ = "data_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    requestor = Column(String(100), nullable=False)
    data_id = Column(Integer, ForeignKey("disaster_data.id"), nullable=False)
    request_time = Column(DateTime, default=datetime.utcnow)
    
    data = relationship("DisasterData", back_populates="data_requests")
