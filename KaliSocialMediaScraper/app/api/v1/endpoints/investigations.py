"""
Investigation API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.core.database import get_db
from app.repositories.investigation_repository import InvestigationRepository
from app.models.schemas import (
    InvestigationRequest,
    InvestigationResult,
    InvestigationResponse,
    InvestigationStatus,
    TargetType
)
from app.services.github_scraper import GitHubScraper
from app.services.social_media_scraper import SocialMediaScraper
from app.services.domain_analyzer import DomainAnalyzer

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=InvestigationResult)
async def create_investigation(
    request: InvestigationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new investigation"""
    try:
        repo = InvestigationRepository(db)
        
        # Create investigation record
        investigation_data = {
            "title": f"Investigation: {request.target_type} - {request.target_value}",
            "description": f"OSINT investigation for {request.target_type}: {request.target_value}",
            "target_type": request.target_type,
            "target_value": request.target_value,
            "analysis_depth": request.analysis_depth,
            "include_network_analysis": request.include_network_analysis,
            "include_timeline_analysis": request.include_timeline_analysis,
            "include_threat_assessment": request.include_threat_assessment,
            "analysis_options": request.analysis_options,
            "status": "pending",
            "created_by_id": 1  # TODO: Get from authentication
        }
        
        investigation = repo.create(investigation_data)
        
        # Start background investigation
        background_tasks.add_task(
            run_investigation,
            investigation.id,
            request,
            db
        )
        
        return InvestigationResult(
            status=InvestigationStatus.PENDING,
            message="Investigation created and started",
            task_id=f"investigation_{investigation.id}",
            progress=0,
            estimated_completion=None
        )
        
    except Exception as e:
        logger.error(f"Error creating investigation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[InvestigationResponse])
async def list_investigations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    target_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all investigations with optional filtering"""
    try:
        repo = InvestigationRepository(db)
        
        if status:
            investigations = repo.get_by_status(status)
        elif target_type:
            investigations = repo.filter(target_type=target_type)
        else:
            investigations = repo.get_all(skip=skip, limit=limit)
        
        return [
            InvestigationResponse(
                id=inv.id,
                title=inv.title,
                description=inv.description,
                target_type=inv.target_type,
                target_value=inv.target_value,
                status=inv.status,
                progress=inv.progress,
                created_at=inv.created_at,
                updated_at=inv.updated_at
            )
            for inv in investigations
        ]
        
    except Exception as e:
        logger.error(f"Error listing investigations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{investigation_id}", response_model=InvestigationResponse)
async def get_investigation(
    investigation_id: int,
    db: Session = Depends(get_db)
):
    """Get investigation by ID"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        return InvestigationResponse(
            id=investigation.id,
            title=investigation.title,
            description=investigation.description,
            target_type=investigation.target_type,
            target_value=investigation.target_value,
            status=investigation.status,
            progress=investigation.progress,
            created_at=investigation.created_at,
            updated_at=investigation.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting investigation {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{investigation_id}", response_model=InvestigationResponse)
async def update_investigation(
    investigation_id: int,
    updates: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update investigation"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.update(investigation_id, updates)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        return InvestigationResponse(
            id=investigation.id,
            title=investigation.title,
            description=investigation.description,
            target_type=investigation.target_type,
            target_value=investigation.target_value,
            status=investigation.status,
            progress=investigation.progress,
            created_at=investigation.created_at,
            updated_at=investigation.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating investigation {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{investigation_id}")
async def delete_investigation(
    investigation_id: int,
    db: Session = Depends(get_db)
):
    """Delete investigation"""
    try:
        repo = InvestigationRepository(db)
        success = repo.delete(investigation_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        return {"message": "Investigation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting investigation {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{investigation_id}/status")
async def get_investigation_status(
    investigation_id: int,
    db: Session = Depends(get_db)
):
    """Get investigation status and progress"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        return {
            "id": investigation.id,
            "status": investigation.status,
            "progress": investigation.progress,
            "created_at": investigation.created_at,
            "updated_at": investigation.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting investigation status {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{investigation_id}/findings")
async def get_investigation_findings(
    investigation_id: int,
    db: Session = Depends(get_db)
):
    """Get investigation findings"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        # TODO: Implement findings retrieval logic
        return {
            "investigation_id": investigation_id,
            "findings": [],
            "total_findings": 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting investigation findings {investigation_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_investigation_statistics(
    db: Session = Depends(get_db)
):
    """Get investigation statistics"""
    try:
        repo = InvestigationRepository(db)
        stats = repo.get_statistics()
        
        return {
            "total_investigations": stats.get("total", 0),
            "completed_investigations": stats.get("completed", 0),
            "pending_investigations": stats.get("pending", 0),
            "failed_investigations": stats.get("failed", 0)
        }
        
    except Exception as e:
        logger.error(f"Error getting investigation statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    db: Session
):
    """Run investigation in background"""
    try:
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        if not investigation:
            logger.error(f"Investigation {investigation_id} not found")
            return
        # Update status to running
        investigation.status = "running"
        investigation.progress = 10
        db.commit()
        # Run investigation based on target type
        if request.target_type == TargetType.GITHUB_REPOSITORY:
            github_scraper = GitHubScraper()
            await run_repository_investigation(
                investigation_id, request, github_scraper, repo
            )
        elif request.target_type == TargetType.DOMAIN:
            domain_analyzer = DomainAnalyzer()
            await run_domain_investigation(
                investigation_id, request, domain_analyzer, repo
            )
        elif request.target_type == TargetType.SOCIAL_MEDIA:
            social_media_scraper = SocialMediaScraper()
            await run_social_media_investigation(
                investigation_id, request, social_media_scraper, repo
            )
        else:
            await run_generic_investigation(investigation_id, request, repo)
        # Update status to completed
        investigation.status = "completed"
        investigation.progress = 100
        db.commit()
        logger.info(f"Investigation {investigation_id} completed successfully")
    except Exception as e:
        logger.error(f"Error running investigation {investigation_id}: {e}")
        # Update status to failed
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.status = "failed"
            db.commit()

async def run_repository_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    github_scraper: GitHubScraper,
    repo: InvestigationRepository
):
    """Run GitHub repository investigation"""
    try:
        # TODO: Implement repository investigation logic
        logger.info(f"Running repository investigation for {request.target_value}")
    except Exception as e:
        logger.error(f"Error in repository investigation: {e}")

async def run_domain_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    domain_analyzer: DomainAnalyzer,
    repo: InvestigationRepository
):
    """Run domain investigation"""
    try:
        # TODO: Implement domain investigation logic
        logger.info(f"Running domain investigation for {request.target_value}")
    except Exception as e:
        logger.error(f"Error in domain investigation: {e}")

async def run_social_media_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    social_media_scraper: SocialMediaScraper,
    repo: InvestigationRepository
):
    """Run social media investigation"""
    try:
        # TODO: Implement social media investigation logic
        logger.info(f"Running social media investigation for {request.target_value}")
    except Exception as e:
        logger.error(f"Error in social media investigation: {e}")

async def run_generic_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    repo: InvestigationRepository
):
    """Run generic investigation"""
    try:
        # TODO: Implement generic investigation logic
        logger.info(f"Running generic investigation for {request.target_value}")
    except Exception as e:
        logger.error(f"Error in generic investigation: {e}") 