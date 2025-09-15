# loads env vars for SMTP

from pydantic_settings import BaseSettings, AnyHttpUrl, validator
from typing import Optional

class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    DEFAULT_FROM: str = "no-reply@example.com"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SERVICE_API_KEY: str = "change-me"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()