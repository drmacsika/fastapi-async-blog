import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import (AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn,
                      validator)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tech Blog"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PASSLIB_ALGORITHM: str = "HS256"
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000",
                                              "http://localhost:8000",
                                              "http://localhost:8080"
                                              ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    
    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite+aiosqlite:///./db.sqlite3"
    # SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@postgresserver/db"
    
    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )
    
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    @validator("EMAILS_FROM_NAME", allow_reuse=True)
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v
    
    
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/templates/build"
    EMAILS_ENABLED: bool = False
    
    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )
        
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    USERS_OPEN_REGISTRATION: bool = False
    
    
    # SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    
    class Config:
        case_sensitive = True
    
    def __repr__(self) -> str:
        return "<%r>" % "Settings"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
