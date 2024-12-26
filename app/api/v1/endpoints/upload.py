from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.disaster import DisasterData, DataSource
from typing import Optional
import os
import shutil
from datetime import datetime

router = APIRouter()

# 确保上传目录存在
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_data(
    integrated_code: str = Form(...),
    earthquake_code: str = Form(...),
    source_code: str = Form(...),
    carrier_code: str = Form(...),
    disaster_code: str = Form(...),
    data_type: str = Form(...),
    indicator_value: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # 验证编码格式
    if len(integrated_code) != 36 or not integrated_code.isdigit():
        raise HTTPException(status_code=400, detail="一体化编码格式不正确")
    
    try:
        # 处理文件保存
        if file:
            # 构建文件保存路径：uploads/年月/文件名
            current_date = datetime.now()
            year_month = current_date.strftime("%Y%m")
            save_dir = os.path.join(UPLOAD_DIR, year_month)
            os.makedirs(save_dir, exist_ok=True)

            # 获取文件扩展名
            file_extension = os.path.splitext(file.filename)[1]
            save_filename = f"{integrated_code}{file_extension}"
            file_path = os.path.join(save_dir, save_filename)

            # 保存文件
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # 更新content为保存的相对路径
            content = os.path.join(year_month, save_filename)
        else:
            if not content:
                raise HTTPException(status_code=400, detail="必须提供文件或文本内容")
    
        # 创建灾情数据记录
        disaster_data = DisasterData(
            integrated_code=integrated_code,
            earthquake_code=earthquake_code,
            source_code=source_code,
            carrier_code=carrier_code,
            disaster_code=disaster_code,
            data_type=data_type,
            content=content,
            indicator_value=indicator_value
        )

        db.add(disaster_data)
        db.commit()
        db.refresh(disaster_data)
        
        return {
            "status": "success",
            "message": "文件上传成功",
            "data": {
                "integrated_code": disaster_data.integrated_code,
                "file_path": content if file else None,
                "indicator_value": disaster_data.indicator_value
            }
        }

    except Exception as e:
        # 如果发生错误，删除已上传的文件
        if file and 'file_path' in locals():
            try:
                os.remove(file_path)
            except:
                pass
        raise HTTPException(
            status_code=500,
            detail=f"上传失败: {str(e)}"
        ) 