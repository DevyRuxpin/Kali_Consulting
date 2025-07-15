"""
Exports API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.utils.time_utils import get_current_time_iso
from app.repositories.investigation_repository import InvestigationRepository
from app.repositories.social_media_repository import SocialMediaRepository
from app.core.database import get_db

router = APIRouter()

@router.post("/data", response_model=Dict[str, Any])
async def export_data(export_request: Dict[str, Any], db: Session = Depends(get_db)):
    """Export data in various formats from the database"""
    try:
        inv_repo = InvestigationRepository(db)
        sm_repo = SocialMediaRepository(db)
        
        # Get real data from database
        investigations = inv_repo.get_all(limit=1000)
        profiles = sm_repo.get_recent_profiles(limit=1000)
        posts = sm_repo.get_recent_posts(limit=1000)
        
        # Transform to export format
        export_data = {
            "investigations": [
                {
                    "id": inv.id,
                    "title": inv.title,
                    "target_type": inv.target_type,
                    "target_value": inv.target_value,
                    "status": inv.status,
                    "created_at": inv.created_at.isoformat() if hasattr(inv, 'created_at') and inv.created_at else None,
                    "updated_at": inv.updated_at.isoformat() if hasattr(inv, 'updated_at') and inv.updated_at else None
                }
                for inv in investigations
            ],
            "profiles": [
                {
                    "id": profile.id,
                    "platform": profile.platform.name if hasattr(profile.platform, 'name') else profile.platform,
                    "username": profile.username,
                    "display_name": profile.display_name,
                    "threat_score": profile.threat_score,
                    "collected_at": profile.collected_at.isoformat() if profile.collected_at is not None else None
                }
                for profile in profiles
            ],
            "posts": [
                {
                    "id": post.id,
                    "platform": post.platform.name if hasattr(post.platform, 'name') else post.platform,
                    "author": post.author,
                    "content": post.content,
                    "threat_score": post.threat_score,
                    "collected_at": post.collected_at.isoformat() if post.collected_at is not None else None
                }
                for post in posts
            ]
        }
        
        return {
            "status": "success",
            "export_id": f"export_{get_current_time_iso().replace(':', '-').replace('.', '-')}",
            "format": export_request.get("format", "json"),
            "data": export_data,
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting data: {str(e)}")

@router.post("/investigation", response_model=Dict[str, Any])
async def export_investigation(investigation_id: str, db: Session = Depends(get_db)):
    """Export investigation data from the database"""
    try:
        inv_repo = InvestigationRepository(db)
        investigation = inv_repo.get(int(investigation_id))
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        # Get related data
        sm_repo = SocialMediaRepository(db)
        target_value = str(investigation.target_value) if investigation.target_value else ""
        related_profiles = sm_repo.get_by_username(target_value) if target_value else []
        related_posts = sm_repo.get_recent_posts(limit=100)
        
        export_data = {
            "investigation": {
                "id": investigation.id,
                "title": investigation.title,
                "target_type": investigation.target_type,
                "target_value": investigation.target_value,
                "status": investigation.status,
                "progress": investigation.progress,
                "created_at": investigation.created_at.isoformat() if investigation.created_at is not None else None,
                "updated_at": investigation.updated_at.isoformat() if investigation.updated_at is not None else None
            },
            "findings": {
                "profiles_found": len(related_profiles),
                "posts_analyzed": len(related_posts),
                "threat_indicators": []
            },
            "threats": [
                {
                    "profile_id": profile.id,
                    "platform": profile.platform.name if hasattr(profile.platform, 'name') else profile.platform,
                    "username": profile.username,
                    "threat_score": profile.threat_score,
                    "indicators": profile.threat_indicators or []
                }
                for profile in related_profiles if profile.threat_score and profile.threat_score > 0.5
            ]
        }
        
        return {
            "status": "success",
            "investigation_id": investigation_id,
            "data": export_data,
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting investigation: {str(e)}")

@router.post("/report", response_model=Dict[str, Any])
async def export_report(report_request: Dict[str, Any], db: Session = Depends(get_db)):
    """Export report data from the database"""
    try:
        inv_repo = InvestigationRepository(db)
        sm_repo = SocialMediaRepository(db)
        
        # Get statistics for report
        total_investigations = inv_repo.count_all()
        completed_investigations = inv_repo.count_by_status('completed')
        total_profiles = sm_repo.count_all()
        high_threat_profiles = sm_repo.count_high_threat_profiles(threshold=0.7)
        
        # Generate report summary
        report_data = {
            "summary": {
                "total_investigations": total_investigations,
                "completed_investigations": completed_investigations,
                "completion_rate": completed_investigations / total_investigations if total_investigations > 0 else 0,
                "total_profiles_scraped": total_profiles,
                "high_threat_profiles": high_threat_profiles,
                "threat_rate": high_threat_profiles / total_profiles if total_profiles > 0 else 0
            },
            "findings": [
                {
                    "type": "investigation_summary",
                    "description": f"Total investigations: {total_investigations}, Completed: {completed_investigations}",
                    "severity": "info"
                },
                {
                    "type": "threat_analysis",
                    "description": f"High threat profiles detected: {high_threat_profiles}",
                    "severity": "warning" if high_threat_profiles > 0 else "info"
                }
            ],
            "recommendations": [
                "Continue monitoring high-threat profiles",
                "Review investigation completion rates",
                "Analyze threat patterns across platforms"
            ]
        }
        
        return {
            "status": "success",
            "report_id": f"report_{get_current_time_iso().replace(':', '-').replace('.', '-')}",
            "format": report_request.get("format", "pdf"),
            "data": report_data,
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting report: {str(e)}") 