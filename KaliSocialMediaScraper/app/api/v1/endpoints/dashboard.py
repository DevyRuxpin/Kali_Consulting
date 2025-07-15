"""
Dashboard API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from datetime import datetime
from app.utils.time_utils import get_current_time_iso

from app.repositories.investigation_repository import InvestigationRepository
from app.repositories.social_media_repository import SocialMediaRepository
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.get("/data", response_model=Dict[str, Any])
async def get_dashboard_data():
    """Get dashboard data"""
    try:
        return {
            "status": "success",
            "data": {
                "investigations": [
                    {
                        "id": 1,
                        "status": "active",
                        "title": "Test Investigation"
                    }
                ],
                "threats": [
                    {
                        "id": 1,
                        "level": "high",
                        "source": "twitter"
                    }
                ],
                "analytics": {
                    "total_investigations": 1,
                    "active_threats": 1,
                    "completion_rate": 0.5
                }
            },
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dashboard data: {str(e)}")

# Removed duplicate endpoint - using /real-time instead

@router.get("/analytics", response_model=Dict[str, Any])
async def get_analytics(db: Session = Depends(get_db)):
    """Get analytics data from the database"""
    sm_repo = SocialMediaRepository(db)
    # Example: platform usage and threat distribution
    platform_counts = {}
    for profile in sm_repo.get_recent_profiles(limit=1000):
        platform = profile.platform.name if hasattr(profile.platform, 'name') else profile.platform
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
    threat_distribution = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for profile in sm_repo.get_recent_profiles(limit=1000):
        score = profile.threat_score or 0
        if score >= 0.8:
            threat_distribution["critical"] += 1
        elif score >= 0.6:
            threat_distribution["high"] += 1
        elif score >= 0.3:
            threat_distribution["medium"] += 1
        else:
            threat_distribution["low"] += 1
    return {
        "status": "success",
        "data": {
            "platform_usage": platform_counts,
            "threat_distribution": threat_distribution,
        },
        "timestamp": get_current_time_iso()
    }

@router.get("/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics from the database"""
    inv_repo = InvestigationRepository(db)
    sm_repo = SocialMediaRepository(db)
    total_investigations = inv_repo.count_all()
    active_investigations = inv_repo.count_by_status('running')
    completed_investigations = inv_repo.count_by_status('completed')
    total_threats = sm_repo.count_high_threat_profiles()
    high_priority_threats = sm_repo.count_high_threat_profiles(threshold=0.8)
    total_profiles_scraped = sm_repo.count_all()
    total_posts_analyzed = db.query(sm_repo.model_post).count() if hasattr(sm_repo, 'model_post') else 0
    return {
        "status": "success",
        "data": {
            "total_investigations": total_investigations,
            "active_investigations": active_investigations,
            "completed_investigations": completed_investigations,
            "total_threats": total_threats,
            "high_priority_threats": high_priority_threats,
            "total_profiles_scraped": total_profiles_scraped,
            "total_posts_analyzed": total_posts_analyzed,
            "system_health": "operational",
            "last_updated": get_current_time_iso()
        },
        "timestamp": get_current_time_iso()
    }

@router.get("/real-time", response_model=Dict[str, Any])
async def get_real_time_dashboard(db: Session = Depends(get_db)):
    """Get real-time dashboard data from the database"""
    sm_repo = SocialMediaRepository(db)
    active_scrapers = 1  # If you have a way to count running scrapers, use it
    recent_activity = [
        {
            "type": "social_media_scrape",
            "platform": profile.platform.name if hasattr(profile.platform, 'name') else profile.platform,
            "timestamp": profile.collected_at.isoformat() if profile.collected_at is not None else None
        }
        for profile in sm_repo.get_recent_profiles(limit=5)
    ]
    return {
        "status": "success",
        "data": {
            "active_scrapers": active_scrapers,
            "recent_activity": recent_activity,
            "system_status": "operational"
        },
        "timestamp": get_current_time_iso()
    } 