from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.disaster import DisasterData, DataSource
from app.utils.encoding import encode_content_text, encode_content_file
from typing import Optional

router = APIRouter()

@router.post("/")
async def upload_data(
    integrated_code: str = Form(...),
    earthquake_code: str = Form(...),
    source_code: str = Form(...),
    carrier_code: str = Form(...),
    disaster_code: str = Form(...),
    data_type: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # 验证编码格式
    if len(integrated_code) != 36 or not integrated_code.isdigit():
        raise HTTPException(status_code=400, detail="一体化编码格式不正确")
    
    # 处理内容编码
    if data_type == "text":
        if not content:
            raise HTTPException(status_code=400, detail="文本数据必须提供内容")
        encoded_content = encode_content_text(content)
    else:
        if not file:
            raise HTTPException(status_code=400, detail="非文本数据必须上传文件")
        file_content = await file.read()
        encoded_content = encode_content_file(file_content, data_type)
        content = file.filename
    
    # 创建灾情数据记录
    disaster_data = DisasterData(
        integrated_code=integrated_code,
        earthquake_code=earthquake_code,
        source_code=source_code,
        carrier_code=carrier_code,
        disaster_code=disaster_code,
        data_type=data_type,
        content=content,
        encoded_content=encoded_content
    )

    db.add(disaster_data)
    db.commit()
    db.refresh(disaster_data)
    
    return disaster_data 