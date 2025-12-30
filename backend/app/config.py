"""Configuration management for the application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "Construction Intelligence Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/construction_intel"
    DATABASE_ECHO: bool = False
    
    # Authentication
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
