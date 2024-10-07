import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from redis.asyncio import Redis, RedisError
from typing import Dict
from contextlib import asynccontextmanager

# Define Redis connection details
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 0))

class Item(BaseModel):
    key: str
    value: str

# Define the lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Redis client
    app.state.redis = Redis(host=redis_host, port=redis_port, db=redis_db)
    yield
    # Shutdown: Closing Redis connection
    await app.state.redis.close()

# Create the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Dependency to retrieve Redis client
async def get_redis() -> Redis:
    return app.state.redis

@app.post("/set_value")
async def set_value(item: Item, redis: Redis = Depends(get_redis)) -> Dict[str, str]:
    try:
        await redis.set(item.key, item.value)
        return {"message": f"Value set for key: {item.key}"}
    except RedisError as e:
        raise HTTPException(status_code=500, detail=f"Error setting value in Redis: {str(e)}")

@app.get("/get_value/{key}")
async def get_value(key: str, redis: Redis = Depends(get_redis)) -> Dict[str, str]:
    try:
        value = await redis.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail=f"No value found for key: {key}")
        return {"key": key, "value": value.decode()}
    except RedisError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving value from Redis: {str(e)}")
