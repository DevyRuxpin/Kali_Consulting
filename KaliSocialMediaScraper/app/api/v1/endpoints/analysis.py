"""
Analysis API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from datetime import datetime
from app.utils.time_utils import get_current_time_iso

from app.models.schemas import AnalysisRequest, AnomalyDetectionRequest, PatternAnalysisRequest
from app.services.anomaly_detector import AnomalyDetector
from app.services.pattern_analyzer import PatternAnalyzer

router = APIRouter()

@router.post("/anomalies", response_model=Dict[str, Any])
async def detect_anomalies(request: AnomalyDetectionRequest):
    """Detect anomalies in data"""
    try:
        anomaly_detector = AnomalyDetector()
        
        result = await anomaly_detector.detect_anomalies(request.data)
        
        return {
            "status": "success",
            "anomaly_score": result.get("anomaly_score", 0.0),
            "anomalies": result.get("anomalies", []),
            "detected": result.get("detected", False),
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting anomalies: {str(e)}")

@router.post("/patterns", response_model=Dict[str, Any])
async def analyze_patterns(request: PatternAnalysisRequest):
    """Analyze patterns in data"""
    try:
        pattern_analyzer = PatternAnalyzer()
        
        result = await pattern_analyzer.analyze_patterns(request.data)
        
        return {
            "status": "success",
            "pattern_analysis": result.get("analysis", "No patterns detected"),
            "pattern_types": result.get("patterns", []),
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing patterns: {str(e)}") 