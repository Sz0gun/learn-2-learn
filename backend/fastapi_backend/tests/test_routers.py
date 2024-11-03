import pytest
from httpx import AsyncClient
from webenv.main import app

@pytest.mark.asyncio
async def test_get_repo_structure():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/github/get_structure")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)