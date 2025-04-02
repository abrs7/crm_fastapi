import pytest
from app.main import app, get_db
from app.database import  SessionLocal
# from app.models import UserAuth
from httpx import AsyncClient


@pytest.fixture(scope="function")
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac

import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Ensure a new event loop for each test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

