from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from typing import List
from pydantic import ValidationError

# Define path to .env file
default_env_path = os.path.join(os.path.dirname(__file__), '../.env')
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", default_env_path)

# Load environment variables from .env file
if not os.path.exists(ENV_FILE_PATH):
    raise RuntimeError(f".env file not found at: {ENV_FILE_PATH}")

load_dotenv(ENV_FILE_PATH)

class Config(BaseSettings):
    DJANGO_SECRET_KEY: str
    DJANGO_DEBUG: bool = False
    ALLOWED_HOSTS: List[str] = []
    CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:8000"]
    FASTAPI_TITLE: str = "Learn2Learn API"
    FASTAPI_VERSION: str = "1.0.0"
    TG_API_ID: int
    TG_API_HASH: str
    TG_BOT_TOKEN: str
    TG_CHANNEL: str
    m0dern: str
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
    OPENAI_API: str

    class Config:
        env_file = ENV_FILE_PATH

# Singleton mechanism
_config_instance = None

def get_config():
    """Ensure the Config instance is created only once."""
    global _config_instance
    if _config_instance is None:
        try:
            _config_instance = Config()
        except ValidationError as e:
            raise RuntimeError(f"Environment configuration error: {e}")
    return _config_instance

# Set global instance
config = get_config()
