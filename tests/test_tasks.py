import pytest
from httpx import AsyncClient
from gateway.app.main import app  # Point to Gateway app

@pytest.mark.anyio
async def test_create_task(client: AsyncClient):
    # This now tests Gateway -> gRPC -> DB flow
    response = await client.post("/tasks/", json={"title": "Microservice Task", "description": "Testing gRPC flow"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Microservice Task"
    assert "id" in data
    assert data["status"] == "new"

@pytest.mark.anyio
async def test_list_tasks(client: AsyncClient):
    response = await client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_get_stats(client: AsyncClient):
    response = await client.get("/tasks/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
