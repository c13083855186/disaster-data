from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.disaster import DisasterData
from app.utils.decoding import decode_content_text, decode_content_file

router = APIRouter()

@router.get("/{data_id}")
async def send_data(
    data_id: int,
    decode: bool = Query(True, description="是否解码内容"),
    db: Session = Depends(get_db)
):
    # 获取数据记录
    data = db.query(DisasterData).filter(DisasterData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="数据不存在")
    
    # 解码内容
    if decode:
        if data.data_type == "text":
            decoded_content = decode_content_text(data.encoded_content)
        else:
            decoded_content = decode_content_file(data.encoded_content, data.data_type)
        
        # 返回解码后的数据
        return {
            "id": data.id,
            "integrated_code": data.integrated_code,
            "data_type": data.data_type,
            "content": decoded_content,
            "timestamp": data.timestamp
        }
    
    # 返回原始数据
    return data 