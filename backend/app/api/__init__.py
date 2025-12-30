"""API package initialization."""
from .projects import router as projects_router
from .analytics import router as analytics_router
from .intelligence import router as intelligence_router
from .auth import router as auth_router

__all__ = [
    "projects_router",
    "analytics_router",
    "intelligence_router",
    "auth_router",
]
