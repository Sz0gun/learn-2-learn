# shared/settings.py
from pydantic_settings import BaseSettings
from typing import List

class Config(BaseSettings):
    # Django settings
    DJANGO_SECRET_KEY: str
    DJANGO_DEBUG: bool = False

    ALLOWED_HOSTS: List[str] = []
    CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:8000"]

    # FastAPI settings
    FASTAPI_TITLE: str = "Learn2Learn API"
    FASTAPI_VERSION: str = "1.0.0"

    # Telegram API credentials
    TG_API_ID: int
    TG_API_HASH: str
    TG_BOT_TOKEN: str
    TG_CHANNEL: str
    m0dern: str

    # PostgreSQL settings
    PSQL_DB_DEV: str
    PSQL_HOST_DEV: str = "localhost"
    PSQL_PORT_DEV: str = "5432"
    PSQL_USER_DEV: str
    PSQL_PASSWORD_DEV: str
    PSQL_DB_PROD: str
    PSQL_HOST_PROD: str
    PSQL_PORT_PROD: str
    PSQL_USER_PROD: str
    PSQL_PASSWORD_PROD: str

    # OpenAI API key
    OPENAI_API: str

    class Config:
        env_file = ".env"

config = Config()

