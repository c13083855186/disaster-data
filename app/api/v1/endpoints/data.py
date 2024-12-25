from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse, JSONResponse
import os
from datetime import datetime
from pydantic import BaseModel
import io

from app.core.dependencies import get_db
from app.models.disaster import DisasterData
from app.utils.decoding import decode_content_text, decode_content_file

# 定义响应模型
class DisasterDataResponse(BaseModel):
    id: int
    integrated_code: str
    earthquake_code: str
    source_code: str
    carrier_code: str
    disaster_code: str
    data_type: str
    content: Optional[str]
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DisasterDataList(BaseModel):
    total: int
    items: List[DisasterDataResponse]

router = APIRouter()

@router.get("/search", response_model=DisasterDataList, summary="查询灾情数据")
async def search_data(
    region: Optional[str] = Query(None, description="地区编码"),
    category: Optional[str] = Query(None, description="灾情分类"),
    subCategory: Optional[str] = Query(None, description="灾情子类"),
    indicator: Optional[str] = Query(None, description="灾情指标"),
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
        
        if region:
            query = query.filter(DisasterData.integrated_code.startswith(region))
        if category:
            query = query.filter(DisasterData.category == category)
        if subCategory:
            query = query.filter(DisasterData.sub_category == subCategory)
        if indicator:
            query = query.filter(DisasterData.indicator == indicator)
            
        # 处理时间范围
        if startTime:
            try:
                start_date = datetime.strptime(startTime, "%Y-%m-%d")
                query = query.filter(DisasterData.created_at >= start_date)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="开始时间格式错误，应为YYYY-MM-DD"
                )
                
        if endTime:
            try:
                end_date = datetime.strptime(endTime, "%Y-%m-%d")
                query = query.filter(DisasterData.created_at <= end_date)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="结束时间格式错误，应为YYYY-MM-DD"
                )

        # 计算总数
        total = query.count()
        
        # 分页
        items = query.offset((page - 1) * pageSize).limit(pageSize).all()
        
        return {
            "items": items,
            "total": total
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"查询数据失败: {str(e)}"
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
            
        print(f"找到数据记录: carrier_code={data.carrier_code}, content={data.content}")
            
        if not data.encoded_content:
            raise HTTPException(
                status_code=404,
                detail="数据内容为空"
            )
            
        # 解码文件内容
        try:
            print("开始解码文件内容...")
            file_content = decode_content_file(data.encoded_content, data.carrier_code)
            print(f"解码成功，内容长度: {len(file_content)} bytes")
        except Exception as e:
            print(f"解码失败: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"解码文件内容失败: {str(e)}"
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
        print(f"文件类型: {content_type}")
        
        # 处理文件名
        filename = data.content if data.content else f"{integrated_code}.dat"
        print(f"下载文件名: {filename}")
        
        # 创建内存文件对象
        file_obj = io.BytesIO(file_content)
        
        # 设置响应头，确保文件名正确编码
        headers = {
            "Content-Disposition": f'attachment; filename*=UTF-8\'\'{filename}',
            "Content-Type": content_type
        }
        print(f"响应头: {headers}")
                    
        return StreamingResponse(
            file_obj,
            media_type=content_type,
            headers=headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"下载失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"下载文件失败: {str(e)}"
        )

@router.get("/preview/{integrated_code}", summary="预览灾情数据")
async def preview_data(
    integrated_code: str = Path(..., description="一体化编码"),
    db: Session = Depends(get_db)
):
    """
    根据一体化编码预览数据内容
    
    状态码：
    - 200: 成功
    - 404: 数据不存在
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
            
        if not data.encoded_content:
            raise HTTPException(
                status_code=404,
                detail="数据内容为空"
            )
            
        # 根据文件类型处理预览内容
        preview_data = None
        file_type = data.carrier_code
        
        if file_type == "0":  # Excel文件
            import pandas as pd
            try:
                # 解码文件内��
                file_content = decode_content_file(data.encoded_content, data.carrier_code)
                # 使用BytesIO创建内存文件对象
                excel_file = io.BytesIO(file_content)
                # 读取Excel文件
                df = pd.read_excel(excel_file)
                preview_data = df.head(10).to_dict('records')  # 只预览前10行
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Excel文件读取失败: {str(e)}"
                )
        elif file_type == "1":  # 图片
            # 对于图片，返回Base64编码的内容供前端直接显示
            preview_data = {
                "content_type": "image/jpeg",
                "data": data.encoded_content
            }
        else:
            preview_data = {"message": "此类型文件不支持预览"}
            
        return {
            "data": preview_data,
            "fileType": file_type,
            "fileName": f"{integrated_code}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"预览数据失败: {str(e)}"
        ) 