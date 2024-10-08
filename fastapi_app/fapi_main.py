import os
import logging
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from redis.asyncio import Redis, RedisError
from typing import Dict
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Redis connection details
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = int(os.getenv('REDIS_DB', 0))

if isinstance(redis_port, str) and redis_port.startswith('tcp://'):
    redis_port = redis_port.split(':')[-1]
redis_port = int(redis_port)


class Item(BaseModel):
    """Model reprezentujący dane dla klucza i wartości."""
    key: str
    value: str

# Define the lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and close the Redis client on application startup and shutdown."""
    app.state.redis = Redis(host=redis_host, port=redis_port, db=redis_db)
    yield
    await app.state.redis.close()

# Create the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Dependency to retrieve Redis client
async def get_redis() -> Redis:
    return app.state.redis

@app.post("/set_value")
async def set_value(item: Item, redis: Redis = Depends(get_redis)) -> Dict[str, str]:
    """
    Sets a value in Redis for a given key.

    Args:
        item (Item): The item containing the key and value to set.
        redis (Redis): The Redis client.

    Returns:
        Dict[str, str]: A message indicating success or failure.
    """
    try:
        logger.info(f"Setting value for key: {item.key}")
        await redis.set(item.key, item.value)
        return {"message": f"Value set for key: {item.key}"}
    except RedisError as e:
        logger.error(f"Error setting value in Redis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error setting value in Redis: {str(e)}")

@app.get("/get_value/{key}")
async def get_value(key: str, redis: Redis = Depends(get_redis)) -> Dict[str, str]:
    """
    Retrieves a value from Redis for a given key.

    Args:
        key (str): The key for which to retrieve the value.
        redis (Redis): The Redis client.

    Returns:
        Dict[str, str]: A dictionary containing the key and its value.
    """
    try:
        logger.info(f"Retrieving value for key: {key}")
        value = await redis.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail=f"No value found for key: {key}")
        return {"key": key, "value": value.decode()}
    except RedisError as e:
        logger.error(f"Error retrieving value from Redis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving value from Redis: {str(e)}")

@app.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Healthcheck endpoint to verify that the application is running."""
    return {"status": "healthy"}

