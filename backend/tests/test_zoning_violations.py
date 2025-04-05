# File: backend/tests/test_zoning_violations.py
import pytest
import json
from app import create_app

@pytest.fixture
def app():
    _app = create_app("testing")
    _app.config["TESTING"] = True
    yield _app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_zoning_violations(client):
    response = client.get("/api/zoning_violations/violations?amenity=Free%20Space")
    assert response.status_code == 200, "Status code should be 200"
    
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert "data" in data
    # The test can be refined further based on expected output.