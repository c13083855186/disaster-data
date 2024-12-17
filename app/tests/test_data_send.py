# app/tests/test_data_send.py

import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app import crud, schemas
from app.database import SessionLocal
from app.utils.encoding import encode_content_text

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        # 在这里插入必要的初始数据
        yield db
    finally:
        db.rollback()
        db.close()

def test_send_data(db):
    # 创建数据源
    data_source = crud.create_data_source(
        db,
        schemas.DataSourceCreate(
            id="3",
            name=f"后方地震应急指挥部",#_{uuid.uuid4().hex[:8]}
            description="描述2"
        )
    )
    
    # 创建测试数据
    disaster_data = crud.create_disaster_data(
        db,
        schemas.DisasterDataCreate(
            id="3",
            integrated_code="111111111111111111111111111111111111",
            earthquake_code="11111111111111111111111111",
            source_code="111",
            carrier_code="1",
            disaster_code="111111",
            data_type="text",
            content="一般损坏面积：200平方米",

            source_id=data_source.id
        ),
        encode_content_text("一般损坏面积：200平方米"),
    )
    
    response = client.get(
        f"/api/data/send/{disaster_data.id}",
        params={
            "requestor": "用户A",
            "decode": True
        }
    )
    assert response.status_code == 200
    assert "content" in response.json()
