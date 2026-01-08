"""
Configuration management for Construction Intelligence Platform
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "BuildIntel Pro"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    COMPANY_NAME: str = "Your Company Name"
    COMPANY_LOGO_URL: Optional[str] = None
    COMPANY_WEBSITE: Optional[str] = None
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/construction_intel"
    DATABASE_ECHO: bool = False  # Added: Set to True to see SQL queries in logs
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    
    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Data Sources
    PERMITS_API_URL: Optional[str] = None
    PERMITS_API_KEY: Optional[str] = None
    TENDERS_API_URL: Optional[str] = None
    TENDERS_API_KEY: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None
    NEWS_API_URL: Optional[str] = None
    SCRAPING_USER_AGENT: str = "BuildIntelBot/1.0"
    SCRAPING_RATE_LIMIT: int = 2  # requests per second
    
    # ML Models
    MODEL_PATH: str = "./models"
    MIN_CONFIDENCE_THRESHOLD: float = 0.7
    ML_BATCH_SIZE: int = 100
    ML_USE_LLM_BY_DEFAULT: bool = False
    
    # Multi-tenancy
    ENABLE_MULTI_TENANT: bool = True
    MAX_USERS_PER_TENANT: int = 50
    MAX_PROJECTS_PER_TENANT_FREE: int = 100
    MAX_PROJECTS_PER_TENANT_PRO: int = 1000
    MAX_PROJECTS_PER_TENANT_ENTERPRISE: int = 0  # 0 = unlimited
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_PER_DAY: int = 10000
    
    # API Credits (cost per operation)
    CREDIT_COST_CLASSIFICATION_RULE: int = 1
    CREDIT_COST_CLASSIFICATION_ML: int = 5
    CREDIT_COST_CLASSIFICATION_LLM: int = 10
    CREDIT_COST_WIN_PROBABILITY: int = 10
    CREDIT_COST_DEMAND_FORECAST: int = 50
    CREDIT_COST_SEMANTIC_SEARCH: int = 5
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: Optional[str] = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    LOG_LEVEL: str = "INFO"