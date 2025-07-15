"""
Threat analysis API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from app.services.threat_analyzer import ThreatAnalyzer
from app.models.schemas import ThreatAnalysisRequest, ThreatCorrelationRequest

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_threat(request: ThreatAnalysisRequest):
    """Analyze threat level for given data"""
    try:
        analyzer = ThreatAnalyzer()
        
        # Extract target and analysis_type from threat_data
        threat_data = request.threat_data
        target = threat_data.get("target", "unknown")
        analysis_type = threat_data.get("analysis_type", "comprehensive")
        
        result = await analyzer.analyze_threat(target, analysis_type)
        return result.dict()
    except Exception as e:
        logger.error(f"Error analyzing threat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/correlate", response_model=Dict[str, Any])
async def correlate_threats(request: ThreatCorrelationRequest):
    """Correlate multiple threats"""
    try:
        analyzer = ThreatAnalyzer()
        result = await analyzer.correlate_threats(request.threats)
        return result
    except Exception as e:
        logger.error(f"Error correlating threats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/report", response_model=Dict[str, Any])
async def generate_threat_report(request: ThreatAnalysisRequest):
    """Generate comprehensive threat report"""
    try:
        analyzer = ThreatAnalyzer()
        result = await analyzer.generate_threat_report(request.threat_data)
        return result
    except Exception as e:
        logger.error(f"Error generating threat report: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 