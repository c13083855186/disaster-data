from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base
from datetime import datetime

class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

class DisasterData(Base):
    __tablename__ = "disaster_data"
    
    id = Column(Integer, primary_key=True, index=True)
    integrated_code = Column(String(36), unique=True, index=True, nullable=False)
    earthquake_code = Column(String(26), nullable=False)
    source_code = Column(String(3), nullable=False)
    carrier_code = Column(String(1), nullable=False)
    disaster_code = Column(String(6), nullable=False)
    data_type = Column(String(20), nullable=False)
    content = Column(String(255), nullable=True)
    indicator_value = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 