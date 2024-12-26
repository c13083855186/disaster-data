from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse, JSONResponse
import os
from datetime import datetime
from pydantic import BaseModel
import io
from sqlalchemy import text

from app.core.dependencies import get_db
from app.models.disaster import DisasterData

# 定义响应模型
class DisasterDataResponse(BaseModel):
    id: int
    integrated_code: str
    source_code: str
    carrier_code: str
    disaster_code: str
    data_type: str
    content: Optional[str]
    region_name: Optional[str]  # 地区名称
    category_name: Optional[str]  # 灾情分类名称
    sub_category_name: Optional[str]  # 灾情子类名称
    indicator_name: Optional[str]  # 灾情指标名称
    indicator_value: Optional[str]  # 指标值
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DisasterDataList(BaseModel):
    total: int
    items: List[DisasterDataResponse]

router = APIRouter()

def get_region_name(region_code: str) -> str:
    """根据地区编码获取地区名称"""
    try:
        if not region_code or len(region_code) < 12:
            print(f"地区编码无效: {region_code}")
            return "未知地区"
        
        # 从数据库查询地区信息
        region_code = region_code[:12]  # 取前12位
        print(f"处理后的地区编码: {region_code}")
        
        db = next(get_db())
        
        # 构建完整的地区名称
        names = []
        
        # 查询省级名称（前2位）
        if len(region_code) >= 2:
            province_code = region_code[:2]
            province = db.execute(
                text("SELECT name FROM provinces WHERE code = :code"),
                {"code": province_code}
            ).fetchone()
            if province:
                names.append(province[0])
        
        # 查询市级名称（前4位）
        if len(region_code) >= 4:
            city_code = region_code[:4]
            city = db.execute(
                text("SELECT name FROM cities WHERE code = :code"),
                {"code": city_code}
            ).fetchone()
            if city:
                names.append(city[0])
        
        # 查询县级名称（前6位）
        if len(region_code) >= 6:
            county_code = region_code[:6]
            county = db.execute(
                text("SELECT name FROM counties WHERE code = :code"),
                {"code": county_code}
            ).fetchone()
            if county:
                names.append(county[0])
        
        # 查询镇级名称（前9位）
        if len(region_code) >= 9:
            town_code = region_code[:9]
            town = db.execute(
                text("SELECT name FROM towns WHERE code = :code"),
                {"code": town_code}
            ).fetchone()
            if town:
                names.append(town[0])
        
        # 查询村级名称（12位）
        if len(region_code) == 12:
            village = db.execute(
                text("SELECT name FROM villages WHERE code = :code"),
                {"code": region_code}
            ).fetchone()
            if village:
                names.append(village[0])
        
        # 如果没有找到任何名称，返回未知地区
        if not names:
            print(f"未找到地区编码 {region_code} 对应的名称")
            return "未知地区"
        
        # 拼接完整地区名称
        full_name = "".join(names)
        print(f"地区编码 {region_code} 对应的完整名称: {full_name}")
        return full_name
        
    except Exception as e:
        print(f"获取地区名称失败: {str(e)}")
        return "未知地区"

def get_disaster_info(disaster_code: str) -> tuple:
    """根据灾情编码获取分类、子类和指标信息"""
    print(f"处理灾情编码: {disaster_code}")
    
    if not disaster_code or len(disaster_code) != 6:
        print(f"灾情编码无效: {disaster_code}")
        return "未知分类", "未知子类", "未知指标"
    
    # 灾情分类映射
    category_map = {
        "1": "地震事件信息",
        "2": "人员伤亡及失踪信息",
        "3": "房屋破坏信息",
        "4": "生命线工程灾情信息",
        "5": "次生灾害信息"
    }
    
    # 子类映射
    sub_category_map = {
        # 地震事件信息子类
        "10": "地震事件基本信息",
        "11": "地震烈度信息",
        "12": "地震监测信息",
        
        # 人员伤亡及失踪信息子类
        "20": "死亡人员信息",
        "21": "受伤人员信息",
        "22": "失踪人员信息",
        
        # 房屋破坏信息子类
        "30": "一般房屋破坏信息",
        "31": "房屋破坏统计信息",
        "32": "房屋破坏分布信息",
        
        # 生命线工程灾情信息子类
        "40": "交通系统",
        "41": "供水系统",
        "42": "输油系统",
        "43": "燃气系统",
        "44": "电力系统",
        "45": "通信系统",
        "46": "水利系统",
        
        # 次生灾害信息子类
        "50": "崩塌",
        "51": "滑坡",
        "52": "泥石流",
        "53": "地面裂缝",
        "54": "地面沉降",
        "55": "其他次生灾害"
    }
    
    # 指标映射
    indicator_map = {
        # 通用指标
        "001": "受灾设施数",
        "002": "受灾范围",
        "003": "受灾程度",
        
        # 地震事件指标
        "101": "震级",
        "102": "震源深度",
        "103": "烈度",
        
        # 人员伤亡指标
        "201": "死亡人数",
        "202": "受伤人数",
        "203": "失踪人数",
        
        # 房屋破坏指标
        "301": "倒塌面积",
        "302": "严重破坏面积",
        "303": "一般破坏面积",
        
        # 生命线指标
        "401": "设施损坏数量",
        "402": "影响范围",
        "403": "修复情况",
        
        # 次生灾害指标
        "501": "发生位置",
        "502": "影响范围",
        "503": "发展趋势"
    }
    
    print(f"分类编码: {disaster_code[0]}")
    print(f"类编码: {disaster_code[:2]}")
    print(f"指标编码: {disaster_code[3:]}")
    
    category = category_map.get(disaster_code[0], "未知分类")
    sub_category = sub_category_map.get(disaster_code[:2], "未知子类")
    indicator = indicator_map.get(disaster_code[3:], "未知指标")
    
    print(f"查询结果: 分类={category}, 子类={sub_category}, 指标={indicator}")
    
    return category, sub_category, indicator

@router.get("/search", response_model=DisasterDataList, summary="查询灾情数据")
async def search_data(
    region: Optional[str] = Query(None, description="地区编码"),
    category: Optional[str] = Query(None, description="灾情分类"),
    subCategory: Optional[str] = Query(None, description="灾情子类"),
    indicator: Optional[str] = Query(None, description="灾情指标"),
    indicatorValue: Optional[str] = Query(None, description="指标值"),
    startTime: Optional[str] = Query(None, description="开始时间"),
    endTime: Optional[str] = Query(None, description="结束时间"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    查询灾情数据，支持多条件筛选和分页
    
    状态码：
    - 200: 成功
    - 400: 请求参数错误
    - 500: 服务器内部错误
    """
    try:
        # 构建查询条件
        query = db.query(DisasterData)
        
        # 处理地区编码查询
        if region:
            print(f"应用地区编码过滤: {region}")
            query = query.filter(DisasterData.integrated_code.startswith(region))
        
        # 处理灾情分类查询
        if category:
            print(f"应用灾情分类过滤: {category}")
            query = query.filter(DisasterData.disaster_code.startswith(category))
        
        # 处理灾情子类查询
        if subCategory:
            print(f"应用灾情子类过滤: {subCategory}")
            if len(subCategory) == 1 and category:
                subCategory = f"{category}{subCategory}"
            print(f"最终灾情子类编码: {subCategory}")
            query = query.filter(DisasterData.disaster_code.startswith(subCategory))
        
        # 处理灾情指标查询
        if indicator:
            print(f"应用灾情指标过滤: {indicator}")
            if category and subCategory:
                full_code = f"{category}{subCategory}{indicator.zfill(3)}"
                print(f"使用完整编码查询: {full_code}")
                query = query.filter(DisasterData.disaster_code == full_code)
            else:
                print(f"使用指标后缀查询: {indicator.zfill(3)}")
                query = query.filter(DisasterData.disaster_code.endswith(indicator.zfill(3)))
            
        # 处理指标值查询
        if indicatorValue:
            print(f"应用指标值过滤: {indicatorValue}")
            query = query.filter(DisasterData.indicator_value == indicatorValue)
            
        # 处理时间范围
        if startTime:
            try:
                start_date = datetime.strptime(startTime, "%Y-%m-%d")
                print(f"应用开始时间过滤: {start_date}")
                query = query.filter(DisasterData.created_at >= start_date)
            except ValueError as e:
                print(f"开始时间格式错误: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"开始时间格式错误: {str(e)}"
                )
                
        if endTime:
            try:
                end_date = datetime.strptime(endTime, "%Y-%m-%d")
                print(f"应用结束时间过滤: {end_date}")
                query = query.filter(DisasterData.created_at <= end_date)
            except ValueError as e:
                print(f"结束时间格式错误: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"结束时间格式错误: {str(e)}"
                )

        # 打印最终的SQL查询语句
        print("最终SQL查询:", str(query))

        # 计算总数
        total = query.count()
        print(f"查询结果总数: {total}")
        
        # 分页
        items = query.offset((page - 1) * pageSize).limit(pageSize).all()
        print(f"当前页数据条数: {len(items)}")
        
        # 处理返回数据
        result_items = []
        for item in items:
            try:
                # 获取地区名称
                region_code = item.integrated_code[:12]
                region_name = get_region_name(region_code)
                
                # 获取灾情信息
                category_name, sub_category_name, indicator_name = get_disaster_info(item.disaster_code)
                
                # 创建响应对象
                result_item = DisasterDataResponse(
                    id=item.id,
                    integrated_code=item.integrated_code,
                    source_code=item.source_code,
                    carrier_code=item.carrier_code,
                    disaster_code=item.disaster_code,
                    data_type=item.data_type,
                    content=item.content,
                    region_name=region_name,
                    category_name=category_name,
                    sub_category_name=sub_category_name,
                    indicator_name=indicator_name,
                    indicator_value=item.indicator_value,
                    timestamp=item.timestamp,
                    created_at=item.created_at,
                    updated_at=item.updated_at
                )
                result_items.append(result_item)
            except Exception as e:
                print(f"处理数据项时出错: {str(e)}")
                continue
        
        return {
            "items": result_items,
            "total": total
        }
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"查询数据失败: {str(e)}")
        print(f"错误堆栈: {error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"查询数据失败: {str(e)}\n{error_trace}"
        )

@router.get("/download/{integrated_code}", summary="下载灾情数据文件")
async def download_data(
    integrated_code: str = Path(..., description="一体化编码"),
    db: Session = Depends(get_db)
):
    """
    根据一体化编码下载对应的数据文件
    
    状态码：
    - 200: 成功
    - 404: 文件不存在
    - 500: 服务器内部错误
    """
    try:
        # 查询数据记录
        data = db.query(DisasterData).filter(
            DisasterData.integrated_code == integrated_code
        ).first()
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"未找到编码为 {integrated_code} 的数据"
            )
            
        if not data.content:
            raise HTTPException(
                status_code=404,
                detail="数据内容为空"
            )
            
        # 确定文件类型
        content_type_map = {
            "0": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "1": "image/jpeg",
            "2": "audio/mpeg",
            "3": "video/mp4",
            "4": "application/octet-stream"
        }
        
        content_type = content_type_map.get(data.carrier_code, "application/octet-stream")
        
        # 从本地文件系统读取文件
        file_path = os.path.join("uploads", data.content)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="文件不存在"
            )
        
        file_obj = open(file_path, "rb")
        filename = os.path.basename(file_path)
        
        # 设置响应头，确保文件名正确编码
        headers = {
            "Content-Disposition": f'attachment; filename*=UTF-8\'\'{filename}',
            "Content-Type": content_type
        }
                    
        return StreamingResponse(
            file_obj,
            media_type=content_type,
            headers=headers,
            background=lambda: file_obj.close() if hasattr(file_obj, 'close') else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"下载文件失败: {str(e)}"
        ) 