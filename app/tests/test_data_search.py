# app/tests/test_data_search.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_data():
    response = client.get(
        "/api/data/search/",
        params={
            "source_id": 1,
            "data_type": "text",
            "start_time": "2021-05-22T00:00:00",
            "end_time": "2021-05-23T00:00:00",
            "skip": 0,
            "limit": 10
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
