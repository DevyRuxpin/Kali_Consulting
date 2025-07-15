"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from .endpoints import investigations, social_media, analysis, exports, intelligence, dashboard, settings, health, github, domain, threat, auth, websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

api_router.include_router(
    websocket.router,
    tags=["websocket"]
)

api_router.include_router(
    investigations.router,
    prefix="/investigations",
    tags=["investigations"]
)

api_router.include_router(
    social_media.router,
    prefix="/social-media",
    tags=["social-media"]
)

api_router.include_router(
    github.router,
    prefix="/github",
    tags=["github"]
)

api_router.include_router(
    domain.router,
    prefix="/domain",
    tags=["domain"]
)

api_router.include_router(
    threat.router,
    prefix="/threat",
    tags=["threat"]
)

api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)

api_router.include_router(
    exports.router,
    prefix="/exports",
    tags=["exports"]
)

api_router.include_router(
    intelligence.router,
    prefix="/intelligence",
    tags=["intelligence"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["dashboard"]
)

api_router.include_router(
    settings.router,
    prefix="/settings",
    tags=["settings"]
) 