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
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://app.constructionintel.com"
    ]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_UPLOAD_EXTENSIONS: list = [".pdf", ".csv", ".xlsx", ".json", ".docx"]
    UPLOAD_STORAGE_PATH: str = "./uploads"
    
    # Cloud Storage (optional)
    AWS_S3_BUCKET: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    
    # Email/SMTP
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    SMTP_FROM_NAME: str = "BuildIntel Pro"
    
    # SSO Providers
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None
    AZURE_CLIENT_ID: Optional[str] = None
    AZURE_CLIENT_SECRET: Optional[str] = None
    AZURE_TENANT_ID: Optional[str] = None
    OKTA_DOMAIN: Optional[str] = None
    OKTA_CLIENT_ID: Optional[str] = None
    OKTA_CLIENT_SECRET: Optional[str] = None
    
    # Stripe Payments
    STRIPE_PUBLIC_KEY: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRICE_ID_PROFESSIONAL: Optional[str] = None
    STRIPE_PRICE_ID_ENTERPRISE: Optional[str] = None
    
    # Feature Flags
    ENABLE_WIN_PROBABILITY: bool = True
    ENABLE_DEMAND_FORECAST: bool = True
    ENABLE_COMPETITIVE_INTEL: bool = True
    ENABLE_WHITE_LABEL: bool = True
    ENABLE_API_ACCESS: bool = True
    ENABLE_EXPORTS: bool = True
    ENABLE_WEBHOOKS: bool = True
    ENABLE_ENTITY_EXTRACTION: bool = True
    ENABLE_PROJECT_CLASSIFICATION: bool = True
    ENABLE_SEMANTIC_SEARCH: bool = True
    ENABLE_SCENARIO_ANALYSIS: bool = False
    ENABLE_RISK_SCORING: bool = False
    
    # Deployment URLs
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    # Regional Settings
    DEFAULT_COUNTRY: str = "USA"
    DEFAULT_CURRENCY: str = "USD"
    DEFAULT_TIMEZONE: str = "America/New_York"
    DEFAULT_LANGUAGE: str = "en"
    
    # Business Rules
    DEFAULT_WIN_PROBABILITY_THRESHOLD: float = 0.7
    DEFAULT_OPPORTUNITY_SCORE_THRESHOLD: float = 0.6
    FORECASTING_PERIODS_DEFAULT: int = 6
    
    # Data Retention
    DATA_RETENTION_DAYS: int = 730  # 2 years
    ARCHIVE_OLD_PROJECTS: bool = True
    ARCHIVE_AFTER_DAYS: int = 365
    
    # Admin
    ADMIN_EMAIL: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None
    SUPPORT_EMAIL: Optional[str] = None
    SUPPORT_PHONE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Dependency for FastAPI"""
    return settings
