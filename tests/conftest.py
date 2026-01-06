import pytest
from httpx import AsyncClient
from gateway.app.main import app  # Changed from app.main
# Settings might need adjustment if they were imported from app.core...
# But for now, let's just make sure client works.

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
