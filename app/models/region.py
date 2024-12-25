from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base

class Province(Base):
    __tablename__ = "provinces"
    code = Column(String(2), primary_key=True)
    name = Column(String(50), nullable=False)

class City(Base):
    __tablename__ = "cities"
    code = Column(String(4), primary_key=True)
    name = Column(String(50), nullable=False)
    province_code = Column(String(2), ForeignKey('provinces.code'), nullable=False)

class County(Base):
    __tablename__ = "counties"
    code = Column(String(6), primary_key=True)
    name = Column(String(50), nullable=False)
    city_code = Column(String(4), ForeignKey('cities.code'), nullable=False)

class Town(Base):
    __tablename__ = "towns"
    code = Column(String(9), primary_key=True)
    name = Column(String(50), nullable=False)
    county_code = Column(String(6), ForeignKey('counties.code'), nullable=False)

class Village(Base):
    __tablename__ = "villages"
    code = Column(String(12), primary_key=True)
    name = Column(String(50), nullable=False)
    town_code = Column(String(9), ForeignKey('towns.code'), nullable=False) 