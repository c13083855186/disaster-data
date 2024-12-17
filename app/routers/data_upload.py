# app/routers/data_upload.py

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import DisasterData, DisasterDataCreate, DataSourceCreate
from app.crud import create_data_source, get_data_source, create_disaster_data
from app.dependencies import get_db
from app.utils import encoding
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.post("/data/upload/", status_code=201)
async def upload_data(
    integrated_code: str = Form(..., examples=["632626200206202105220204001010302001"]),
    earthquake_code: str = Form(..., examples=["63262620020620210522020400"]),
    source_code: str = Form(..., examples=["101"]),
    carrier_code: str = Form(..., examples=["0"]),
    disaster_code: str = Form(..., examples=["302001"]),
    data_type: str = Form(..., examples=["text"]),
    content: Optional[str] = Form(None, examples=["一般损坏面积：200平方米"]),
    source_id: int = Form(..., examples=[1]),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # 验证数据源存在
    data_source = get_data_source(db, source_id)
    
    # 验证一体化编码格式
    if len(integrated_code) != 36 or not integrated_code.isdigit():
        raise HTTPException(status_code=400, detail="一体化编码格式不正确，应为36位数字")
    
    # 验证震情编码格式
    if len(earthquake_code) != 26 or not earthquake_code.isdigit():
        raise HTTPException(status_code=400, detail="震情编码格式不正确，应为26位数字")
    
    # 验证来源编码格式
    if len(source_code) != 3 or not source_code.isdigit():
        raise HTTPException(status_code=400, detail="来源编码格式不正确，应为3位数字")
    
    # 验证载体编码格式
    if len(carrier_code) != 1 or not carrier_code.isdigit():
        raise HTTPException(status_code=400, detail="载体编码格式不正确，应为1位数字")
    
    # 验证灾情编码格式
    if len(disaster_code) != 6 or not disaster_code.isdigit():
        raise HTTPException(status_code=400, detail="灾情编码格式不正确，应为6位数字")
    
    # 根据数据类型处理内容
    if data_type == "text":
        if not content:
            raise HTTPException(status_code=400, detail="文本数据必须提供内容")
        encoded_content = encoding.encode_content_text(content)
    else:
        if not file:
            raise HTTPException(status_code=400, detail="非文本数据必须上传文件")
        file_content = await file.read()
        try:
            encoded_content = encoding.encode_content_file(file_content, data_type)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        content = file.filename  # 存储文件名作为内容
    
    # 创建灾情数据记录
    disaster_data_create = DisasterDataCreate(
        integrated_code=integrated_code,
        earthquake_code=earthquake_code,
        source_code=source_code,
        carrier_code=carrier_code,
        disaster_code=disaster_code,
        data_type=data_type,
        content=content,
        source_id=source_id
    )
    new_data = create_disaster_data(db, disaster_data_create, encoded_content)
    
    return new_data
