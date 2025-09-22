# loads env vars for SMTP

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # SMTP config
    MAIL_PROVIDER: str = "smtp" # SMTP for testing/dev phase, SES for production phase
    MAIL_HOST: str
    MAIL_PORT: int = 587
    MAIL_USER: Optional[str] = None
    MAIL_PASS: Optional[str] = None
    MAIL_FROM: str = "no-reply@example.com"    # Redis
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # AWS SES
    AWS_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    # App
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SERVICE_API_KEY: str = "change-me"


    ENV: str = "dev" 
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()