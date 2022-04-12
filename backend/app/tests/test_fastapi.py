from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_now():
    response = client.get("/now")
    assert response.status_code == 200
