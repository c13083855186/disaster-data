import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Province, City, County, Town, Village
import os
import re

# 添加所有省份代码列表
PROVINCE_CODES = ['11', '12', '13', '14', '15', '21', '22', '23', '31', '32', 
                 '33', '34', '35', '36', '37', '41', '42', '43', '45', '50', 
                 '51', '52', '53', '54', '61', '62', '63', '64', '65']

def extract_json_from_js(file_content):
    """从 JS 文件中提取 JSON 数据"""
    # 匹配 export default {...} 中的 JSON 内容
    match = re.search(r'export\s+default\s+({[\s\S]*})', file_content)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print(f"JSON 解析失败")
            return None
    return None

def get_or_create(db: Session, model, **kwargs):
    """获取或创建记录"""
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        db.add(instance)
        return instance, True

def import_regions():
    db = SessionLocal()
    try:
        # 第一步：先导入所有省份
        for code in PROVINCE_CODES:
            file_path = f'disaster-web/src/data/regions/{code}.js'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    province_data = extract_json_from_js(content)
                    
                    if province_data:
                        # 只添加省份
                        province, created = get_or_create(
                            db, 
                            Province,
                            code=province_data['value'],
                            name=province_data['label']
                        )
                        if created:
                            print(f"添加省份: {province_data['label']}")
        
        # 提交所有省份数据
        db.commit()
        print("完成所有省份数据导入")

        # 第二步：导入其他层级数据
        for code in PROVINCE_CODES:
            file_path = f'disaster-web/src/data/regions/{code}.js'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    province_data = extract_json_from_js(content)
                    
                    if province_data:
                        # 处理城市
                        for city in province_data.get('children', []):
                            city_obj, created = get_or_create(
                                db,
                                City,
                                code=city['value'],
                                name=city['label'],
                                province_code=province_data['value']
                            )
                            if created:
                                print(f"  添加城市: {city['label']}")
                                db.commit()  # 每添加一个城市就提交一次
                            
                            # 处理区县
                            for county in city.get('children', []):
                                county_obj, created = get_or_create(
                                    db,
                                    County,
                                    code=county['value'],
                                    name=county['label'],
                                    city_code=city['value']
                                )
                                if created:
                                    print(f"    添加区县: {county['label']}")
                                
                                # 处理街道/镇
                                for town in county.get('children', []):
                                    town_obj, created = get_or_create(
                                        db,
                                        Town,
                                        code=town['value'],
                                        name=town['label'],
                                        county_code=county['value']
                                    )
                                    if created:
                                        print(f"      添加街道: {town['label']}")
                                    
                                    # 处理村/社区
                                    for village in town.get('children', []):
                                        village_obj, created = get_or_create(
                                            db,
                                            Village,
                                            code=village['value'],
                                            name=village['label'],
                                            town_code=town['value']
                                        )
                                        if created:
                                            print(f"        添加村: {village['label']}")
                                
                                # 每处理完一个区县就提交一次
                                db.commit()
                        
                        print(f"完成省份 {province_data['label']} 的数据导入")
                    else:
                        print(f"无法解析文件: {file_path}")
            else:
                print(f"文件不存在: {file_path}")
                
    except Exception as e:
        print(f"导入失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_regions() 