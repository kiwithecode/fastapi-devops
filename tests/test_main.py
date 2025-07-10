from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"

def test_valid_post():
    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    response = client.post(
        "/DevOps",
        headers={"X-Parse-REST-API-Key": API_KEY},
        json=payload
    )
    assert response.status_code == 200
    assert "Hello Juan Perez" in response.json()["message"]

def test_invalid_method_get():
    response = client.get("/DevOps")
    assert response.status_code == 405
    assert response.text == "ERROR"

def test_invalid_method_put():
    response = client.put("/DevOps")
    assert response.status_code == 405
    assert response.text == "ERROR"

def test_invalid_apikey():
    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    response = client.post(
        "/DevOps",
        headers={"X-Parse-REST-API-Key": "wrong-api-key"},
        json=payload
    )
    assert response.status_code == 403
