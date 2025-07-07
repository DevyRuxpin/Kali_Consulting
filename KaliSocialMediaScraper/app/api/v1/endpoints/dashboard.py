"""
Dashboard API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.repositories.investigation_repository import InvestigationRepository
from app.repositories.social_media_repository import SocialMediaRepository

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    try:
        investigation_repo = InvestigationRepository(db)
        social_repo = SocialMediaRepository(db)
        
        # Get basic statistics
        total_investigations = investigation_repo.count_all()
        completed_investigations = investigation_repo.count_by_status("completed")
        failed_investigations = investigation_repo.count_by_status("failed")
        active_investigations = investigation_repo.count_by_status("in_progress")
        
        # Get social media statistics
        total_profiles = social_repo.count_all()
        high_threat_profiles = social_repo.count_high_threat_profiles()
        
        # Calculate success rate
        success_rate = 0
        if total_investigations > 0:
            success_rate = (completed_investigations / total_investigations) * 100
        
        return {
            "total_investigations": total_investigations,
            "completed_investigations": completed_investigations,
            "failed_investigations": failed_investigations,
            "active_investigations": active_investigations,
            "success_rate": round(success_rate, 2),
            "total_profiles": total_profiles,
            "high_threat_profiles": high_threat_profiles,
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/activity")
async def get_dashboard_activity(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent dashboard activity"""
    try:
        investigation_repo = InvestigationRepository(db)
        social_repo = SocialMediaRepository(db)
        
        # Get recent investigations
        recent_investigations = investigation_repo.get_recent(limit=limit)
        
        # Get recent social media activity
        recent_profiles = social_repo.get_recent_profiles(limit=limit)
        
        # Combine and sort by timestamp
        activity = []
        
        for inv in recent_investigations:
            activity.append({
                "type": "investigation",
                "id": inv.id,
                "title": inv.title,
                "status": inv.status,
                "timestamp": inv.updated_at or inv.created_at,
                "description": f"Investigation {inv.status}: {inv.title}"
            })
        
        for profile in recent_profiles:
            activity.append({
                "type": "profile",
                "id": profile.id,
                "username": profile.username,
                "platform": profile.platform.name,
                "timestamp": profile.collected_at,
                "description": f"Profile collected: {profile.username} on {profile.platform.name}"
            })
        
        # Sort by timestamp (most recent first)
        activity.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "activity": activity[:limit],
            "total_count": len(activity)
        }
    except Exception as e:
        logger.error(f"Error getting dashboard activity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/real-time")
async def get_real_time_data(db: Session = Depends(get_db)):
    """Get real-time dashboard data"""
    try:
        investigation_repo = InvestigationRepository(db)
        
        # Get current active investigations
        active_investigations = investigation_repo.get_by_status("in_progress")
        
        # Get recent updates (last 5 minutes)
        recent_time = datetime.utcnow() - timedelta(minutes=5)
        recent_updates = investigation_repo.get_updates_since(recent_time)
        
        return {
            "active_investigations": len(active_investigations),
            "recent_updates": len(recent_updates),
            "last_updated": datetime.utcnow().isoformat(),
            "system_status": "operational"
        }
    except Exception as e:
        logger.error(f"Error getting real-time data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/investigations/summary")
async def get_investigations_summary(db: Session = Depends(get_db)):
    """Get investigations summary for dashboard"""
    try:
        investigation_repo = InvestigationRepository(db)
        
        # Get investigations by status
        by_status = investigation_repo.get_count_by_status()
        
        # Get investigations by target type
        by_target_type = investigation_repo.get_count_by_target_type()
        
        # Get recent investigations
        recent = investigation_repo.get_recent(limit=5)
        
        return {
            "by_status": by_status,
            "by_target_type": by_target_type,
            "recent": [
                {
                    "id": inv.id,
                    "title": inv.title,
                    "status": inv.status,
                    "target_type": inv.target_type,
                    "target_value": inv.target_value,
                    "created_at": inv.created_at,
                    "updated_at": inv.updated_at
                }
                for inv in recent
            ]
        }
    except Exception as e:
        logger.error(f"Error getting investigations summary: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 