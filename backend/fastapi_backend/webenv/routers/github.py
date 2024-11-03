# backend/fastapi_backend/webenv/routers/github.py
from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()

TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")
GITHUB_REPO = "Sz0gun/learn-2-learn"

@router.get("/get_structure")
async def get_repo_structure():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/main"
    headers = {"Authorization": f"token {TOKEN_GITHUB}"}

    # Debugging prints
    print("URL:", url)
    print("TOKEN_GITHUB:", TOKEN_GITHUB)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
    except httpx.HTTPStatusError as e:
        print(f"Error: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Github API request failed: {e}")
