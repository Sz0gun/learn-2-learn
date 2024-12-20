from pydantic_settings import BaseSettings
from typing import List

class Config(BaseSettings):
    # DJANGO_SECRET_KEY: str
    # DJANGO_DEBUG: bool = True
    # ALLOWED_HOSTS: List[str] = ["*"]

    FASTAPI_TITLE: str = "Learn2Learn API"
    FASTAPI_VERSION: str = "1.0.0"

    TG_API_ID: int
    TG_API_HASH: str
    TG_BOT_TOKEN: str
    TG_CHANNEL: str
    m0dern: str

    OPENAI_API: str

    # REDIS_HOST: str = "localhost"
    # REDIS_PORT: int = 6379

    # CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:8000"]

    class Config:
        env_file = ".env"

config = Config()
print(f"Loaded config: {config.dict()}")
