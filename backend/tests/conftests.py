import os

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db
from app.db import models
from app.core.security import get_password_hash

TEST_DB_URL = "sqlite:///./test_app.db"

engine_test = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    if os.path.exists("test_app.db"):
        os.remove("test_app.db")
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    user = models.User(
        username="testuser",
        role="uploader",
        hashed_password=get_password_hash("password123"),
    )
    db.add(user)
    db.commit()
    db.close()
    yield
    engine_test.dispose()
    if os.path.exists("test_app.db"):
        os.remove("test_app.db")

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
