import pytest
from httpx import AsyncClient, ASGITransport
from fapi_main import app, get_redis
from unittest.mock import AsyncMock
from redis.exceptions import RedisError

@pytest.fixture
def mock_redis():
    return AsyncMock()

@pytest.fixture
def override_get_redis(mock_redis):
    app.dependency_overrides[get_redis] = lambda: mock_redis
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_set_value(mock_redis, override_get_redis):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/set_value", json={"key": "test_key", "value": "test_value"})
    assert response.status_code == 200
    assert response.json() == {"message": "Value set for key: test_key"}
    mock_redis.set.assert_awaited_once_with("test_key", "test_value")

@pytest.mark.asyncio
async def test_get_value(mock_redis, override_get_redis):
    mock_redis.get.return_value = b"test_value"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/get_value/test_key")
    assert response.status_code == 200
    assert response.json() == {"key": "test_key", "value": "test_value"}
    mock_redis.get.assert_awaited_once_with("test_key")

@pytest.mark.asyncio
async def test_get_value_not_found(mock_redis, override_get_redis):
    mock_redis.get.return_value = None
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/get_value/non_existent_key")
    assert response.status_code == 404
    assert response.json() == {"detail": "No value found for key: non_existent_key"}

@pytest.mark.asyncio
async def test_set_value_redis_error(mock_redis, override_get_redis):
    # Raise RedisError to match application code handling
    mock_redis.set.side_effect = RedisError("Redis error")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/set_value", json={"key": "test_key", "value": "test_value"})
    assert response.status_code == 500
    assert "Error setting value in Redis" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_value_redis_error(mock_redis, override_get_redis):
    # Raise RedisError to match application code handling
    mock_redis.get.side_effect = RedisError("Redis error")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/get_value/test_key")
    assert response.status_code == 500
    assert "Error retrieving value from Redis" in response.json()["detail"]

@pytest.mark.asyncio
async def test_set_value_invalid_input(mock_redis, override_get_redis):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/set_value", json={"invalid": "data"})
    assert response.status_code == 422  # Unprocessable Entity
