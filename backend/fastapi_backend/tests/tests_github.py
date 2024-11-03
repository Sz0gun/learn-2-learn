# backend/fastapi_backend/tests/test_github.py

import pytest
import respx
from fastapi.testclient import TestClient
from webenv.main import app
from httpx import Response

client = TestClient(app)

@pytest.fixture(autouse=True)
def set_github_token(monkeypatch):
    """Fixture to set a fake TOKEN_GITHUB for testing."""
    monkeypatch.setenv("TOKEN_GITHUB", "fake-token-for-testing")

@pytest.fixture
def github_repo():
    return "Sz0gun/learn-2-learn"

@pytest.fixture
def github_url(github_repo):
    return f"https://api.github.com/repos/{github_repo}/git/trees/main"

@respx.mock
def test_get_repo_structure_success(github_url):
    """Test successful retrieval of repository structure."""
    
    # Mockowanie odpowiedzi z GitHub API
    respx.get(github_url).respond(
        status_code=200,
        json={
            "sha": "abc123",
            "url": github_url,
            "tree": [
                {"path": "backend", "type": "tree"},
                {"path": "frontend", "type": "tree"},
            ],
            "truncated": False
        }
    )
    
    response = client.get("/github/get_structure")
    assert response.status_code == 200
    response_json = response.json()
    assert "tree" in response_json
    assert isinstance(response_json["tree"], list)
    assert len(response_json["tree"]) > 0

@respx.mock
def test_get_repo_structure_failure(github_url):
    """Test handling of GitHub API failure."""
    
    # Mockowanie błędu z GitHub API
    respx.get(github_url).respond(status_code=404, json={"message": "Not Found"})
    
    response = client.get("/github/get_structure")
    assert response.status_code == 500
    assert response.json()["detail"].startswith("Github API request failed")
