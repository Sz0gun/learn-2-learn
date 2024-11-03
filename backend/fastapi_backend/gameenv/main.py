#backend/fastapi_backend/gameenv/main.py

from fastapi import FastAPI
from .routers import game_router

app = FastAPI(title="Game Enviiroment API")

app.include_router(game_router, prefix="/game", tags=["Game"])

@app.get("/")
async def root():
    return {"message": "Welcome to Learn-2-Learn Game Environment API!"}