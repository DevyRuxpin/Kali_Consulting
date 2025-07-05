"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from .endpoints import investigations, social_media, analysis, exports

api_router = APIRouter()

# Include all endpoint routers
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
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)

api_router.include_router(
    exports.router,
    prefix="/exports",
    tags=["exports"]
) 