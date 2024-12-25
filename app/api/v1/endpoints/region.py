from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.region import Province, City, County, Town, Village
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/provinces")
def get_provinces(db: Session = Depends(get_db)):
    try:
        print("正在查询省份数据...")
        provinces = db.query(Province).all()
        print(f"查询到 {len(provinces)} 条省份数据")
        result = [{"value": p.code, "label": p.name} for p in provinces]
        logger.info(f"获取省份数据: {result}")
        return result
    except Exception as e:
        logger.error(f"获取省份数据失败: {e}")
        raise

@router.get("/cities/{province_code}")
def get_cities(province_code: str, db: Session = Depends(get_db)):
    try:
        cities = db.query(City).filter(City.province_code == province_code).all()
        result = [{"value": c.code, "label": c.name} for c in cities]
        logger.info(f"获取城市数据: {result}")
        return result
    except Exception as e:
        logger.error(f"获取城市数据失败: {e}")
        raise

@router.get("/counties/{city_code}")
def get_counties(city_code: str, db: Session = Depends(get_db)):
    try:
        counties = db.query(County).filter(County.city_code == city_code).all()
        result = [{"value": c.code, "label": c.name} for c in counties]
        logger.info(f"获取区县数据: {result}")
        return result
    except Exception as e:
        logger.error(f"获取区县数据失败: {e}")
        raise

@router.get("/towns/{county_code}")
def get_towns(county_code: str, db: Session = Depends(get_db)):
    try:
        towns = db.query(Town).filter(Town.county_code == county_code).all()
        result = [{"value": t.code, "label": t.name} for t in towns]
        logger.info(f"获取街道数据: {result}")
        return result
    except Exception as e:
        logger.error(f"获取街道数据失败: {e}")
        raise

@router.get("/villages/{town_code}")
def get_villages(town_code: str, db: Session = Depends(get_db)):
    try:
        villages = db.query(Village).filter(Village.town_code == town_code).all()
        result = [{"value": v.code, "label": v.name} for v in villages]
        logger.info(f"获取村数据: {result}")
        return result
    except Exception as e:
        logger.error(f"获取村数据失败: {e}")
        raise 