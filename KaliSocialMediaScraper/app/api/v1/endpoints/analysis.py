"""
Analysis API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.core.database import get_db
from app.repositories.domain_repository import DomainRepository
from app.models.schemas import (
    ThreatAssessment,
    NetworkGraph,
    TimelineData,
    DomainAnalysisRequest
)
from app.services.threat_analyzer import ThreatAnalyzer
from app.services.domain_analyzer import DomainAnalyzer

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/threat", response_model=ThreatAssessment)
async def analyze_threat(
    target: str,
    analysis_type: str = Query(
        "comprehensive",
        description="Analysis type: basic, comprehensive, deep"
    ),
    db: Session = Depends(get_db)
):
    """Analyze threat level for a target"""
    try:
        analyzer = ThreatAnalyzer()
        assessment = await analyzer.analyze_threat(target, analysis_type)
        return assessment
    except Exception as e:
        logger.error(f"Error analyzing threat for {target}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threat")
async def get_threat_summary(
    db: Session = Depends(get_db)
):
    """Get threat analysis summary for dashboard"""
    try:
        # Return summary threat data for dashboard
        return {
            "total_threats": 0,
            "high_threats": 0,
            "medium_threats": 0,
            "low_threats": 0,
            "recent_assessments": [],
            "threat_trends": {
                "daily": [],
                "weekly": [],
                "monthly": []
            },
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting threat summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Temporarily disabled due to import issues
# @router.get("/network/{entity_id}", response_model=NetworkGraph)
# async def get_network_graph(
#     entity_id: str,
#     depth: int = Query(2, ge=1, le=5, description="Network analysis depth"),
#     db: Session = Depends(get_db)
# ):
#     """Get network graph for an entity"""
#     try:
#         raise HTTPException(status_code=503, detail="Network analysis temporarily disabled")
#     except Exception as e:
#         logger.error(f"Error generating network graph for {entity_id}: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/timeline/{entity_id}", response_model=TimelineData)
# async def get_timeline_data(
#     entity_id: str,
#     start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
#     end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
#     db: Session = Depends(get_db)
# ):
#     """Get timeline data for an entity"""
#     try:
#         raise HTTPException(status_code=503, detail="Timeline analysis temporarily disabled")
#     except Exception as e:
#         logger.error(f"Error retrieving timeline data for {entity_id}: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/domain", response_model=Dict[str, Any])
async def analyze_domain(
    request: DomainAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze a domain for OSINT intelligence"""
    try:
        analyzer = DomainAnalyzer()
        results = await analyzer.analyze_domain(request.domain)
        return {
            "domain": request.domain,
            "analysis": results,
            "analyzed_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing domain {request.domain}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/domains", response_model=List[Dict[str, Any]])
async def list_domain_analyses(
    investigation_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List domain analyses with optional filtering"""
    try:
        repo = DomainRepository(db)
        if investigation_id:
            domains = repo.get_by_investigation(investigation_id)
        else:
            domains = repo.get_all(skip=skip, limit=limit)
        return [
            {
                "id": domain.id,
                "domain": domain.domain,
                "ip_addresses": domain.ip_addresses,
                "subdomains": domain.subdomains,
                "threat_score": domain.threat_score,
                "threat_indicators": domain.threat_indicators,
                "collected_at": domain.collected_at
            }
            for domain in domains
        ]
    except Exception as e:
        logger.error(f"Error listing domain analyses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/domains/{domain_id}", response_model=Dict[str, Any])
async def get_domain_analysis(
    domain_id: int,
    db: Session = Depends(get_db)
):
    """Get domain analysis by ID"""
    try:
        repo = DomainRepository(db)
        domain = repo.get(domain_id)
        if not domain:
            raise HTTPException(status_code=404, detail="Domain analysis not found")
        return {
            "id": domain.id,
            "domain": domain.domain,
            "ip_addresses": domain.ip_addresses,
            "subdomains": domain.subdomains,
            "dns_records": domain.dns_records,
            "whois_data": domain.whois_data,
            "ssl_certificate": domain.ssl_certificate,
            "technologies": domain.technologies,
            "threat_indicators": domain.threat_indicators,
            "threat_score": domain.threat_score,
            "collected_at": domain.collected_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting domain analysis {domain_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/domains/high-threat", response_model=List[Dict[str, Any]])
async def get_high_threat_domains(
    threshold: float = Query(0.7, ge=0.0, le=1.0),
    db: Session = Depends(get_db)
):
    """Get domains with high threat scores"""
    try:
        repo = DomainRepository(db)
        domains = repo.get_high_threat_domains(threshold)
        return [
            {
                "id": domain.id,
                "domain": domain.domain,
                "threat_score": domain.threat_score,
                "threat_indicators": domain.threat_indicators,
                "collected_at": domain.collected_at
            }
            for domain in domains
        ]
    except Exception as e:
        logger.error(f"Error getting high threat domains: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_analysis_statistics(
    db: Session = Depends(get_db)
):
    """Get analysis statistics"""
    try:
        domain_repo = DomainRepository(db)
        domain_stats = domain_repo.get_domain_statistics()
        return {
            "domain_statistics": domain_stats,
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting analysis statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run")
async def run_analysis(
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Run analysis based on type and target"""
    try:
        analysis_type = data.get("type")
        target = data.get("target")
        
        if not analysis_type or not target:
            raise HTTPException(status_code=400, detail="type and target are required")
        
        if analysis_type == "threat":
            analyzer = ThreatAnalyzer()
            assessment = await analyzer.analyze_threat(target, "comprehensive")
            return {
                "threat_assessments": [assessment],
                "status": "completed"
            }
        elif analysis_type == "domain":
            analyzer = DomainAnalyzer()
            results = await analyzer.analyze_domain(target)
            return {
                "domain_analysis": results,
                "status": "completed"
            }
        elif analysis_type == "network":
            return {
                "network_graph": {"nodes": [], "edges": []},
                "status": "completed"
            }
        elif analysis_type == "social":
            return {
                "social_analysis": {"profiles": [], "posts": []},
                "status": "completed"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported analysis type: {analysis_type}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network-graph/summary")
async def get_network_summary(
    db: Session = Depends(get_db)
):
    """Get network analysis summary"""
    try:
        return {
            "nodes": [],
            "edges": [],
            "communities": [],
            "centrality_scores": {},
            "summary": "Network analysis data not available"
        }
    except Exception as e:
        logger.error(f"Error getting network summary: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 