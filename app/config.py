"""
config.py — Application settings loaded from environment variables.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/analytics"
    secret_key: str = "change-me-in-env"
    debug: bool = False

    class Config:
        env_file = ".env"
