# app/routers/data_send.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas import DisasterData, DataRequestCreate
from app.crud import get_disaster_data, create_data_request
from app.dependencies import get_db
from app.utils import decoding

router = APIRouter()

@router.get("/data/send/{data_id}")
def send_data(
    data_id: int,
    requestor: str = Query(..., examples={"default": "用户A"}),
    decode: bool = Query(..., examples={"default": True}),
    db: Session = Depends(get_db)
):
    # 获取目标数据
    disaster_data = get_disaster_data(db, data_id)
    
    # 记录数据请求日志
    data_request_create = DataRequestCreate(
        requestor=requestor,
        data_id=data_id
    )
    create_data_request(db, data_request_create)
    
    # 解码数据
    if decode:
        if disaster_data.data_type == "text":
            decoded_content = decoding.decode_content_text(disaster_data.encoded_content)
        else:
            decoded_content = decoding.decode_content_file(disaster_data.encoded_content, disaster_data.data_type)
    else:
        decoded_content = disaster_data.encoded_content
    
    # 返回数据
    response_data = DisasterData(
        id=disaster_data.id,
        integrated_code=disaster_data.integrated_code,
        earthquake_code=disaster_data.earthquake_code,
        source_code=disaster_data.source_code,
        carrier_code=disaster_data.carrier_code,
        disaster_code=disaster_data.disaster_code,
        data_type=disaster_data.data_type,
        content=decoded_content if decode else disaster_data.encoded_content,
        encoded_content=disaster_data.encoded_content,
        timestamp=disaster_data.timestamp,
        created_at=disaster_data.created_at,
        updated_at=disaster_data.updated_at,
        source_id=disaster_data.source_id
    )
    
    return response_data
