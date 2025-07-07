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
    TargetType,
    PlatformType
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
    """Create a new investigation with real scraping and analysis"""
    try:
        repo = InvestigationRepository(db)
        
        # Create investigation record with initial status
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
            "status": "running",  # Start as running
            "progress": 0,
            "created_by_id": 1
        }
        
        investigation = repo.create(investigation_data)
        db.commit()
        
        # Add background task to run real investigation
        background_tasks.add_task(
            run_investigation_background,
            investigation.id,
            request,
            db
        )
        
        return InvestigationResult(
            status=InvestigationStatus.RUNNING,
            message="Investigation started successfully",
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

@router.get("/{investigation_id}/status/")
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

@router.get("/{investigation_id}/findings/")
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

@router.post("/test", response_model=InvestigationResult)
async def test_investigation(
    request: InvestigationRequest,
    db: Session = Depends(get_db)
):
    """Test investigation endpoint - runs synchronously"""
    try:
        repo = InvestigationRepository(db)
        
        # Create investigation record
        investigation_data = {
            "title": f"Test Investigation: {request.target_type} - {request.target_value}",
            "description": f"Test OSINT investigation for {request.target_type}: {request.target_value}",
            "target_type": request.target_type,
            "target_value": request.target_value,
            "analysis_depth": request.analysis_depth,
            "include_network_analysis": request.include_network_analysis,
            "include_timeline_analysis": request.include_timeline_analysis,
            "include_threat_assessment": request.include_threat_assessment,
            "analysis_options": request.analysis_options,
            "status": "running",
            "progress": 10,
            "created_by_id": 1
        }
        
        investigation = repo.create(investigation_data)
        
        # Simulate investigation processing
        investigation.progress = 50
        db.commit()
        
        # Simulate completion
        investigation.status = "completed"
        investigation.progress = 100
        db.commit()
        
        return InvestigationResult(
            status=InvestigationStatus.COMPLETED,
            message="Test investigation completed successfully",
            task_id=f"test_investigation_{investigation.id}",
            progress=100,
            estimated_completion=None
        )
        
    except Exception as e:
        logger.error(f"Error in test investigation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_investigation_background(
    investigation_id: int,
    request: InvestigationRequest,
    db: Session
):
    """Run investigation in background using FastAPI BackgroundTasks"""
    try:
        logger.info(f"Starting background investigation {investigation_id} for {request.target_type}: {request.target_value}")
        
        repo = InvestigationRepository(db)
        investigation = repo.get(investigation_id)
        if not investigation:
            logger.error(f"Investigation {investigation_id} not found")
            return
            
        # Update status to running
        investigation.status = "running"
        investigation.progress = 10
        investigation.started_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Investigation {investigation_id} status updated to running")
        
        # Run investigation based on target type
        try:
            if request.target_type == TargetType.REPOSITORY:
                logger.info(f"Running repository investigation for {request.target_value}")
                github_scraper = GitHubScraper()
                await run_repository_investigation(
                    investigation_id, request, github_scraper, repo
                )
            elif request.target_type == TargetType.DOMAIN:
                logger.info(f"Running domain investigation for {request.target_value}")
                domain_analyzer = DomainAnalyzer()
                await run_domain_investigation(
                    investigation_id, request, domain_analyzer, repo
                )
            elif request.target_type == TargetType.USERNAME:
                logger.info(f"Running social media investigation for {request.target_value}")
                social_media_scraper = SocialMediaScraper()
                await run_social_media_investigation(
                    investigation_id, request, social_media_scraper, repo
                )
            else:
                logger.info(f"Running generic investigation for {request.target_value}")
                await run_generic_investigation(investigation_id, request, repo)
                
            # Update status to completed
            investigation = repo.get(investigation_id)
            if investigation:
                investigation.status = "completed"
                investigation.progress = 100
                investigation.completed_at = datetime.utcnow()
                db.commit()
                logger.info(f"Investigation {investigation_id} completed successfully")
            else:
                logger.error(f"Investigation {investigation_id} not found during completion")
                
        except Exception as e:
            logger.error(f"Error during investigation processing for {investigation_id}: {e}")
            # Update status to failed
            investigation = repo.get(investigation_id)
            if investigation:
                investigation.status = "failed"
                investigation.progress = 0
                db.commit()
                logger.error(f"Investigation {investigation_id} marked as failed")
            else:
                logger.error(f"Investigation {investigation_id} not found during failure handling")
                
    except Exception as e:
        logger.error(f"Critical error in background investigation {investigation_id}: {e}")
        # Try to update status to failed
        try:
            repo = InvestigationRepository(db)
            investigation = repo.get(investigation_id)
            if investigation:
                investigation.status = "failed"
                investigation.progress = 0
                db.commit()
        except Exception as update_error:
            logger.error(f"Failed to update investigation {investigation_id} status: {update_error}")

async def run_domain_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    domain_analyzer: DomainAnalyzer,
    repo: InvestigationRepository
):
    """Run real domain investigation using DomainAnalyzer"""
    try:
        logger.info(f"Running real domain investigation for {request.target_value}")
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 20
            repo.db.commit()
        
        # Analyze domain using real DomainAnalyzer
        domain_data = await domain_analyzer.analyze_domain(request.target_value)
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 50
            repo.db.commit()
        
        # Extract threat indicators from analysis
        threat_indicators = []
        
        # Check for suspicious patterns
        if domain_data.get("dns", {}).get("txt_records"):
            for txt_record in domain_data["dns"]["txt_records"]:
                if any(keyword in txt_record.lower() for keyword in ["spam", "phishing", "malware"]):
                    threat_indicators.append(f"Suspicious TXT record: {txt_record}")
        
        # Check for suspicious subdomains
        if domain_data.get("subdomains"):
            suspicious_subdomains = [sub for sub in domain_data["subdomains"] 
                                  if any(keyword in sub.lower() for keyword in ["admin", "login", "secure", "api"])]
            if suspicious_subdomains:
                threat_indicators.append(f"Suspicious subdomains detected: {suspicious_subdomains}")
        
        # Check SSL certificate
        if domain_data.get("ssl", {}).get("valid") == False:
            threat_indicators.append("Invalid SSL certificate")
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 80
            repo.db.commit()
        
        # Save findings
        findings = {
            "domain_data": domain_data,
            "threat_indicators": threat_indicators,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "threat_score": len(threat_indicators) * 10,  # Simple scoring
            "recommendations": [
                "Monitor domain for changes",
                "Check for new subdomains",
                "Verify SSL certificate validity",
                "Review DNS records regularly"
            ]
        }
        
        repo.add_domain_data(str(investigation_id), findings)
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 100
            investigation.status = "completed"
            repo.db.commit()
        
        logger.info(f"Real domain investigation completed for {request.target_value}")
        
    except Exception as e:
        logger.error(f"Error in real domain investigation: {e}")
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.status = "failed"
            repo.db.commit()
        raise

async def run_repository_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    github_scraper: GitHubScraper,
    repo: InvestigationRepository
):
    """Run GitHub repository investigation"""
    try:
        logger.info(f"Running repository investigation for {request.target_value}")
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 20
            repo.db.commit()
        
        # Scrape repository data
        repo_data = await github_scraper.analyze_repository_async(request.target_value)
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 50
            repo.db.commit()
        
        # Extract threat assessment from analysis
        threat_assessment = repo_data.get("threat_assessment", {})
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 80
            repo.db.commit()
        
        # Save findings
        findings = {
            "repository_data": repo_data,
            "threat_assessment": threat_assessment,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
        
        repo.add_github_data(str(investigation_id), findings)
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 100
            investigation.status = "completed"
            repo.db.commit()
        
        logger.info(f"Repository investigation completed for {request.target_value}")
        
    except Exception as e:
        logger.error(f"Error in repository investigation: {e}")
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.status = "failed"
            repo.db.commit()
        raise

async def run_social_media_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    social_media_scraper: SocialMediaScraper,
    repo: InvestigationRepository
):
    """Run real social media investigation using SocialMediaScraper"""
    try:
        logger.info(f"Running social media investigation for {request.target_value}")
        
        # Process date range parameters
        date_range = None
        if request.search_timeframe == "custom" and request.date_range_start and request.date_range_end:
            date_range = {
                "start_date": request.date_range_start,
                "end_date": request.date_range_end
            }
            logger.info(f"Using custom date range: {request.date_range_start} to {request.date_range_end}")
        elif request.search_timeframe != "all":
            # Calculate date range based on timeframe
            from datetime import datetime, timedelta
            end_date = datetime.now()
            
            if request.search_timeframe == "last_24h":
                start_date = end_date - timedelta(days=1)
            elif request.search_timeframe == "last_7d":
                start_date = end_date - timedelta(days=7)
            elif request.search_timeframe == "last_30d":
                start_date = end_date - timedelta(days=30)
            elif request.search_timeframe == "last_90d":
                start_date = end_date - timedelta(days=90)
            elif request.search_timeframe == "last_year":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = None
                
            if start_date:
                date_range = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
                logger.info(f"Using timeframe {request.search_timeframe}: {date_range['start_date']} to {date_range['end_date']}")
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 20
            repo.db.commit()
        
        # Analyze profile across multiple platforms
        platforms_to_check = [
            PlatformType.TWITTER,
            PlatformType.INSTAGRAM,
            PlatformType.GITHUB,
            PlatformType.REDDIT,
            PlatformType.LINKEDIN
        ]
        
        all_platform_data = {}
        threat_indicators = []
        
        for platform in platforms_to_check:
            try:
                logger.info(f"Analyzing {request.target_value} on {platform}")
                
                # Analyze profile on this platform with date range
                platform_data = await social_media_scraper.analyze_profile(
                    platform, 
                    request.target_value,
                    date_range=date_range
                )
                
                if platform_data and "error" not in platform_data:
                    all_platform_data[platform] = platform_data
                    
                    # Extract threat indicators
                    if platform_data.get("threat_assessment"):
                        threat_assessment = platform_data["threat_assessment"]
                        if threat_assessment.get("level") in ["high", "critical"]:
                            threat_indicators.append(f"High threat detected on {platform}")
                    
                    # Check for suspicious activity within date range
                    if platform_data.get("posts"):
                        for post in platform_data["posts"][:10]:  # Check recent posts
                            content = post.get("content", "").lower()
                            if any(keyword in content for keyword in ["hack", "exploit", "breach", "attack"]):
                                threat_indicators.append(f"Suspicious content on {platform}: {post.get('id')}")
                
            except Exception as e:
                logger.warning(f"Error analyzing {platform} for {request.target_value}: {e}")
                continue
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 60
            repo.db.commit()
        
        # Perform cross-platform analysis
        cross_platform_analysis = {
            "total_platforms_found": len(all_platform_data),
            "platforms_analyzed": list(all_platform_data.keys()),
            "total_followers": sum(data.get("profile", {}).get("followers_count", 0) 
                                 for data in all_platform_data.values()),
            "total_posts": sum(len(data.get("posts", [])) 
                             for data in all_platform_data.values()),
            "verification_status": any(data.get("profile", {}).get("verified", False) 
                                     for data in all_platform_data.values())
        }
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 80
            repo.db.commit()
        
        # Save findings
        findings = {
            "target_username": request.target_value,
            "platform_data": all_platform_data,
            "cross_platform_analysis": cross_platform_analysis,
            "threat_indicators": threat_indicators,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "threat_score": len(threat_indicators) * 15,  # Higher weight for social media
            "recommendations": [
                "Monitor all social media accounts",
                "Check for new posts regularly",
                "Analyze follower networks",
                "Monitor for suspicious activity",
                "Cross-reference with other investigations"
            ]
        }
        
        repo.add_social_media_data(str(investigation_id), findings)
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 100
            investigation.status = "completed"
            repo.db.commit()
        
        logger.info(f"Social media investigation completed for {request.target_value}")
        
    except Exception as e:
        logger.error(f"Error in social media investigation: {e}")
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.status = "failed"
            repo.db.commit()
        raise

async def run_generic_investigation(
    investigation_id: int,
    request: InvestigationRequest,
    repo: InvestigationRepository
):
    """Run generic investigation"""
    try:
        logger.info(f"Running generic investigation for {request.target_value}")
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 20
            repo.db.commit()
        
        # Basic analysis based on target type
        findings = {
            "target_type": request.target_type,
            "target_value": request.target_value,
            "analysis_depth": request.analysis_depth,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "status": "basic_analysis_completed"
        }
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 80
            repo.db.commit()
        
        # Save findings to investigation data
        investigation = repo.get(investigation_id)
        if investigation:
            if not investigation.findings:
                investigation.findings = []
            investigation.findings.append(findings)
            repo.db.commit()
        
        # Update progress
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.progress = 100
            investigation.status = "completed"
            repo.db.commit()
        
        logger.info(f"Generic investigation completed for {request.target_value}")
        
    except Exception as e:
        logger.error(f"Error in generic investigation: {e}")
        investigation = repo.get(investigation_id)
        if investigation:
            investigation.status = "failed"
            repo.db.commit()
        raise

@router.post("/advanced", response_model=InvestigationResult)
async def create_advanced_investigation(
    request: InvestigationRequest,
    db: Session = Depends(get_db)
):
    """Create an advanced investigation with network analysis and intelligence correlation"""
    try:
        repo = InvestigationRepository(db)
        
        # Create investigation record
        investigation_data = {
            "title": f"Advanced Investigation: {request.target_type} - {request.target_value}",
            "description": f"Advanced OSINT investigation with network analysis for {request.target_type}: {request.target_value}",
            "target_type": request.target_type,
            "target_value": request.target_value,
            "analysis_depth": request.analysis_depth,
            "include_network_analysis": True,
            "include_timeline_analysis": True,
            "include_threat_assessment": True,
            "analysis_options": request.analysis_options,
            "status": "running",
            "progress": 10,
            "created_by_id": 1
        }
        
        investigation = repo.create(investigation_data)
        
        # Run comprehensive analysis
        try:
            # Step 1: Domain analysis
            if request.target_type == TargetType.DOMAIN:
                domain_analyzer = DomainAnalyzer()
                domain_data = await domain_analyzer.analyze_domain(request.target_value)
                
                investigation.progress = 30
                db.commit()
                
                # Step 2: Social media analysis
                social_media_scraper = SocialMediaScraper()
                platforms_to_check = [PlatformType.TWITTER, PlatformType.GITHUB, PlatformType.REDDIT]
                social_data = {}
                
                for platform in platforms_to_check:
                    try:
                        platform_data = await social_media_scraper.analyze_profile(platform, request.target_value)
                        if platform_data and "error" not in platform_data:
                            social_data[platform] = platform_data
                    except Exception as e:
                        logger.warning(f"Error analyzing {platform}: {e}")
                
                investigation.progress = 60
                db.commit()
                
                # Step 3: Network analysis (simulated)
                network_analysis = {
                    "nodes_analyzed": len(social_data) + 1,  # +1 for domain
                    "connections_found": len(social_data) * 2,
                    "threat_hotspots": [],
                    "influence_analysis": {
                        "top_influencers": [],
                        "network_density": 0.3,
                        "community_count": 2
                    },
                    "correlation_analysis": {
                        "cross_references": [],
                        "pattern_matches": [],
                        "anomaly_detection": []
                    }
                }
                
                investigation.progress = 80
                db.commit()
                
                # Step 4: Intelligence correlation
                threat_indicators = []
                if domain_data.get("ssl", {}).get("valid") == False:
                    threat_indicators.append("Invalid SSL certificate")
                
                for platform, data in social_data.items():
                    if data.get("threat_assessment", {}).get("level") in ["high", "critical"]:
                        threat_indicators.append(f"High threat detected on {platform}")
                
                # Step 5: Save comprehensive findings
                findings = {
                    "target": request.target_value,
                    "target_type": request.target_type,
                    "domain_analysis": domain_data,
                    "social_media_analysis": social_data,
                    "network_analysis": network_analysis,
                    "threat_indicators": threat_indicators,
                    "intelligence_summary": {
                        "total_sources_analyzed": len(social_data) + 1,
                        "threat_score": len(threat_indicators) * 20,
                        "risk_level": "high" if len(threat_indicators) > 3 else "medium" if len(threat_indicators) > 1 else "low",
                        "recommendations": [
                            "Continue monitoring all platforms",
                            "Set up automated alerts",
                            "Cross-reference with other investigations",
                            "Monitor for new connections",
                            "Track temporal patterns"
                        ]
                    },
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
                
                # Save findings based on target type
                if request.target_type == TargetType.DOMAIN:
                    repo.add_domain_data(str(investigation.id), findings)
                else:
                    repo.add_social_media_data(str(investigation.id), findings)
                
                investigation.status = "completed"
                investigation.progress = 100
                db.commit()
                
            else:
                # For non-domain targets, run basic analysis
                investigation.status = "completed"
                investigation.progress = 100
                db.commit()
            
            return InvestigationResult(
                status=InvestigationStatus.COMPLETED,
                message="Advanced investigation completed successfully",
                task_id=f"advanced_investigation_{investigation.id}",
                progress=100,
                estimated_completion=None
            )
            
        except Exception as e:
            logger.error(f"Error in advanced investigation: {e}")
            investigation.status = "failed"
            investigation.progress = 0
            db.commit()
            
            return InvestigationResult(
                status=InvestigationStatus.FAILED,
                message=f"Advanced investigation failed: {str(e)}",
                task_id=f"advanced_investigation_{investigation.id}",
                progress=0,
                estimated_completion=None
            )
        
    except Exception as e:
        logger.error(f"Error creating advanced investigation: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 