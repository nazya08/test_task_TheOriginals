import os
import secrets
from typing import Optional, Any, Dict, List, Union, ClassVar

from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator, AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Test task for The Originals"
    API_STR: str = "/api"

    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", secrets.token_urlsafe(32)
    )
    JWT_REFRESH_SECRET_KEY: str = os.getenv(
        "JWT_REFRESH_SECRET_KEY", secrets.token_urlsafe(32)
    )
    ACTIVATION_SECRET_KEY: str = os.getenv(
        "ACTIVATION_SECRET_KEY", secrets.token_urlsafe(32)
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ACTIVATION_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3

    TOKEN_ALGORITHM: str = "HS256"

    SERVER_NAME: str = "tz_theoriginals"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    LOG_LEVEL: str = "debug"
    RELOAD: bool = True
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(
            cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # POSTGRES_SERVER: str = 'localhost:5432'
    POSTGRES_SERVER: str = (
        f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
    )
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    POSTGRES_TEST_SERVER: str = (
        f'{os.getenv("POSTGRES_TEST_HOST")}:{os.getenv("POSTGRES_TEST_PORT")}'
    )
    POSTGRES_TEST_USER: str = os.getenv("POSTGRES_TEST_USER")
    POSTGRES_TEST_PASSWORD: str = os.getenv("POSTGRES_TEST_PASSWORD")
    POSTGRES_TEST_DB: str = os.getenv("POSTGRES_TEST_DB")
    SQLALCHEMY_TEST_DATABASE_URL: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URL", mode="before")
    def assemble_db_connection(
            cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @field_validator("SQLALCHEMY_TEST_DATABASE_URL", mode="before")
    def assemble_test_db_connection(
            cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_TEST_USER"),
            password=values.get("POSTGRES_TEST_PASSWORD"),
            host=values.get("POSTGRES_TEST_SERVER"),
            path=f"/{values.get('POSTGRES_TEST_DB') or ''}",
        )

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    BROKER_URL: str = os.getenv("BROKER_URL")

    EMAILS_ENABLED: bool = True

    EMAILS_FROM_NAME: str = os.getenv("EMAILS_FROM_NAME")
    EMAILS_FROM_EMAIL: EmailStr = os.getenv("EMAILS_FROM_EMAIL")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: str = os.getenv("SMTP_PORT")
    SMTP_TLS: bool = os.getenv("SMTP_TLS")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = os.getenv("EMAIL_RESET_TOKEN_EXPIRE_HOURS")
    EMAIL_TEMPLATES_DIR: ClassVar[str] = "src/templates/email"

    class Config:
        case_sensitive = True


settings = Settings()
