"""
API package initialization.

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
"""
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
