# app/tests/test_data_upload.py

import pytest
import uuid
from sqlalchemy import text
from fastapi.testclient import TestClient
from app.main import app
from app import models, crud, schemas
from app.database import SessionLocal, engine
from app.utils.encoding import encode_content_text, encode_content_file

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    # 创建所有表
    models.Base.metadata.create_all(bind=engine)
    
    # 创建新的数据库会话
    db = SessionLocal()
    try:
        # 在这里插入必要的初始数据
        yield db
    finally:
        db.rollback()  # 确保回滚任何未提交的更改
        db.close()

def test_upload_text_data(db):
    # 创建数据源
    data_source = crud.create_data_source(
        db, 
        schemas.DataSourceCreate(
            id="1",
            name=f"后方地震应急指挥部", 
            description="描述1"
        )
    )
    
    # 上传文本数据
    response = client.post(
        "/api/data/upload/",
        data={
            "id":"1",
            "integrated_code": "632626200206202105220204001010302001",
            "earthquake_code": "63262620020620210522020400",
            "source_code": "101",
            "carrier_code": "0",
            "disaster_code": "302001",
            "data_type": "text",
            "content": "一般损坏面积：200平方米",
            "encoded_content": encode_content_text("一般损坏面积：200平方米"),
            "source_id": data_source.id
        }
    )
    assert response.status_code == 201
    assert response.json()["integrated_code"] == "632626200206202105220204001010302001"

def test_upload_file_data(db):
    # 创建数据源
    data_source = crud.create_data_source(
        db,
        schemas.DataSourceCreate(
            id="2",
            name=f"互联网感知",
            description="描述"
        )
    )
    
    # 上传文件数据
    with open("app/tests/test_image.png", "rb") as f:
        response = client.post(
            "/api/data/upload/",
            data={
                "id":"2",
                "integrated_code": "632626200206202105220204012001302001",
                "earthquake_code": "63262620020620210522020401",
                "source_code": "200",
                "carrier_code": "1",
                "disaster_code": "302001",
                "data_type": "image",
                "source_id": data_source.id
            },
            files={"file": ("test_image.png", f, "image/png")}
        )
    assert response.status_code == 201
    assert response.json()["integrated_code"] == "632626200206202105220204012001302001"