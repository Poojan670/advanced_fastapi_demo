import os
from pydantic import (AnyHttpUrl, BaseSettings, EmailStr, HttpUrl,
                      PostgresDsn, validator)
from typing import (Any, Dict, List,
                    Optional, Union)
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRY_TIME: int = 60 * 24 * 1  # 1 day
    SERVER_HOST: str = os.getenv("SERVER_HOST")
    SERVER_PORT: int = os.getenv("SERVER_PORT")
    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS")
    BACKEND_CORS_ORIGINS: AnyHttpUrl = os.getenv("BACKEND_CORS_ORIGINS")

    PROJECT_NAME: str = os.getenv("PROJECT_NAME")

    DB_HOST: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = os.getenv("SMTP_PORT")
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: Optional[EmailStr] = os.getenv("EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: Optional[str] = os.getenv("EMAILS_FROM_NAME")

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "templates"
    EMAILS_ENABLED: bool = os.getenv("EMAILS_ENABLED")

    EMAIL_TEST_USER: EmailStr = os.getenv("EMAIL_TEST_USER")
    FIRST_SUPERUSER_USERNAME: str = os.getenv("FIRST_SUPERUSER_USERNAME")
    FIRST_SUPERUSER_EMAIL: str = os.getenv("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    USERS_OPEN_REGISTRATION: bool = True

    class Config:
        case_sensitive = True


settings = Settings()
