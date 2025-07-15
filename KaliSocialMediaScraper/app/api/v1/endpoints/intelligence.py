"""
Intelligence API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.utils.time_utils import get_current_time_iso
from app.repositories.investigation_repository import InvestigationRepository
from app.repositories.social_media_repository import SocialMediaRepository
from app.core.database import get_db

from app.models.schemas import IntelligenceRequest, IntelligenceReport
from app.services.intelligence_engine import IntelligenceEngine

router = APIRouter()

@router.post("/process", response_model=Dict[str, Any])
async def process_intelligence(request: IntelligenceRequest, db: Session = Depends(get_db)):
    """Process intelligence data from multiple sources"""
    try:
        intelligence_engine = IntelligenceEngine()
        
        # Get real data from database
        inv_repo = InvestigationRepository(db)
        sm_repo = SocialMediaRepository(db)
        
        # Get recent investigations and social media data
        recent_investigations = inv_repo.get_all(limit=50)
        recent_profiles = sm_repo.get_recent_profiles(limit=100)
        high_threat_profiles = sm_repo.get_high_threat_profiles(threshold=0.7)
        
        # Prepare data for processing
        data = {
            "domain_data": request.domain_data,
            "github_data": request.github_data,
            "social_media_data": request.social_media_data,
            "investigation_data": [
                {
                    "id": inv.id,
                    "target_type": inv.target_type,
                    "target_value": inv.target_value,
                    "status": inv.status,
                    "progress": inv.progress
                }
                for inv in recent_investigations
            ],
            "profile_data": [
                {
                    "id": profile.id,
                    "platform": profile.platform.name if hasattr(profile.platform, 'name') else profile.platform,
                    "username": profile.username,
                    "threat_score": profile.threat_score,
                    "indicators": profile.threat_indicators or []
                }
                for profile in high_threat_profiles
            ]
        }
        
        result = await intelligence_engine.process_intelligence(data)
        
        return {
            "status": "success",
            "processed_data": result,
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing intelligence: {str(e)}")

@router.post("/report", response_model=Dict[str, Any])
async def generate_intelligence_report(request: IntelligenceRequest, db: Session = Depends(get_db)):
    """Generate comprehensive intelligence report from database data"""
    try:
        intelligence_engine = IntelligenceEngine()
        
        # Get real data from database
        inv_repo = InvestigationRepository(db)
        sm_repo = SocialMediaRepository(db)
        
        # Get comprehensive data for report
        total_investigations = inv_repo.count_all()
        completed_investigations = inv_repo.count_by_status('completed')
        total_profiles = sm_repo.count_all()
        high_threat_profiles = sm_repo.count_high_threat_profiles(threshold=0.7)
        recent_profiles = sm_repo.get_recent_profiles(limit=50)
        
        # Prepare data for report generation
        data = {
            "domain_data": request.domain_data,
            "github_data": request.github_data,
            "social_media_data": request.social_media_data,
            "statistics": {
                "total_investigations": total_investigations,
                "completed_investigations": completed_investigations,
                "completion_rate": completed_investigations / total_investigations if total_investigations > 0 else 0,
                "total_profiles": total_profiles,
                "high_threat_profiles": high_threat_profiles,
                "threat_rate": high_threat_profiles / total_profiles if total_profiles > 0 else 0
            },
            "recent_activity": [
                {
                    "id": profile.id,
                    "platform": profile.platform.name if hasattr(profile.platform, 'name') else profile.platform,
                    "username": profile.username,
                    "threat_score": profile.threat_score,
                    "collected_at": profile.collected_at.isoformat() if profile.collected_at is not None else None
                }
                for profile in recent_profiles
            ]
        }
        
        result = await intelligence_engine.generate_report(data)
        
        return {
            "status": "success",
            "report": result,
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating intelligence report: {str(e)}") 