from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # SMTP
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None
    SMTP_TLS: bool = True

    # Notifications
    ALERT_EMAIL_TO: Optional[str] = None
    WEBHOOK_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
