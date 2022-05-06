import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/qwork_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="session")
def init_and_destroy_db() -> None:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user(init_and_destroy_db: None):
    response = client.post(
        "/process_text_instant",
        json={"text": "Температура 37.9. Давление высокое - 120 на 80."},
    )
    assert response.status_code == 200
    response = client.get("/history")
    assert response.json()[0]["temperature"] == 37.9
