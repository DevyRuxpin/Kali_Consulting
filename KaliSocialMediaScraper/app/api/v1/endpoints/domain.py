"""
Domain analysis API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from app.services.domain_analyzer import DomainAnalyzer
from app.models.schemas import DomainAnalysisRequest

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_domain(request: DomainAnalysisRequest):
    """Analyze domain for threats and intelligence"""
    try:
        analyzer = DomainAnalyzer()
        result = await analyzer.analyze_domain(request.domain)
        return result
    except Exception as e:
        logger.error(f"Error analyzing domain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info/{domain}", response_model=Dict[str, Any])
async def get_domain_info(domain: str):
    """Get basic domain information"""
    try:
        analyzer = DomainAnalyzer()
        result = await analyzer.get_domain_info(domain)
        return result
    except Exception as e:
        logger.error(f"Error getting domain info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reputation/{domain}", response_model=Dict[str, Any])
async def check_domain_reputation(domain: str):
    """Check domain reputation and threat score"""
    try:
        analyzer = DomainAnalyzer()
        result = await analyzer.check_domain_reputation(domain)
        return result
    except Exception as e:
        logger.error(f"Error checking domain reputation: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 