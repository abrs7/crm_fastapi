import pytest
from httpx import AsyncClient
from app.main import app  # Import FastAPI app
from app.database import SessionLocal

pytest_plugins = "pytest_asyncio"

@pytest.fixture(scope="function")
def test_db():
    """Create a new test database session for each test"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
async def client() -> AsyncClient:
    """Fixture to provide a test HTTP client for async requests"""
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac

@pytest.mark.asyncio
async def test_search_leads(client: AsyncClient):
    """Test the /leads/search endpoint"""
    login_data = {"username": "testuser", "password": "testpassword"}
    login_response = await client.post("/token", data=login_data)
    assert login_response.status_code == 200, login_response.text 
    
    # assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]  # Extract the token
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/leads/search?query=TestCompany", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of leads
