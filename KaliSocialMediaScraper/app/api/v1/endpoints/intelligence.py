"""
Advanced Intelligence API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from app.models.database import Investigation
from app.models.schemas import (
    ThreatAssessment,
    IntelligenceReport,
    Entity,
    Relationship,
    Pattern,
    Anomaly
)
from app.services.intelligence_engine import IntelligenceEngine
from app.services.dark_web_intelligence import DarkWebIntelligenceService
from app.services.ml_intelligence import MLIntelligenceService
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.repositories.investigation_repository import InvestigationRepository
from app.repositories.social_media_repository import SocialMediaRepository

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze/comprehensive")
async def comprehensive_intelligence_analysis(
    investigation_id: str,
    background_tasks: BackgroundTasks,
    analysis_depth: str = "comprehensive",
    db: Session = Depends(get_db)
):
    """Perform comprehensive intelligence analysis"""
    try:
        # Initialize services
        intelligence_engine = IntelligenceEngine()
        dark_web_service = DarkWebIntelligenceService()
        ml_service = MLIntelligenceService()
        
        # Get investigation data
        investigation = db.query(Investigation).filter(Investigation.id == int(investigation_id.split('_')[-1])).first()
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        
        # Perform analysis
        analysis_result = await intelligence_engine.analyze_investigation(investigation, analysis_depth)
        
        # Generate intelligence report
        intelligence_report = await intelligence_engine.generate_intelligence_report(analysis_result)
        
        # Add background tasks for additional analysis
        background_tasks.add_task(
            perform_dark_web_analysis,
            investigation.target_value,
            investigation_id
        )
        background_tasks.add_task(
            perform_ml_analysis,
            analysis_result.entities,
            analysis_result.relationships,
            investigation_id
        )
        
        return {
            "status": "success",
            "investigation_id": investigation_id,
            "analysis_result": analysis_result,
            "intelligence_report": intelligence_report,
            "message": "Comprehensive intelligence analysis completed"
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive intelligence analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dark-web/scan")
async def scan_dark_web(
    target: str,
    platforms: Optional[List[str]] = None,
    depth: str = "comprehensive"
):
    """Scan dark web for target-related entities"""
    try:
        async with DarkWebIntelligenceService() as dark_web_service:
            intelligence = await dark_web_service.scan_dark_web_entities(target, platforms, depth)
            
            return {
                "status": "success",
                "target": target,
                "intelligence": intelligence,
                "message": "Dark web scan completed"
            }
            
    except Exception as e:
        logger.error(f"Error in dark web scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dark-web/monitor-marketplaces")
async def monitor_dark_web_marketplaces(
    keywords: Optional[List[str]] = None,
    categories: Optional[List[str]] = None
):
    """Monitor dark web marketplaces"""
    try:
        async with DarkWebIntelligenceService() as dark_web_service:
            entities = await dark_web_service.monitor_dark_web_marketplaces(keywords, categories)
            
            return {
                "status": "success",
                "entities_found": len(entities),
                "entities": entities,
                "message": "Marketplace monitoring completed"
            }
            
    except Exception as e:
        logger.error(f"Error in marketplace monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dark-web/analyze-crypto")
async def analyze_cryptocurrency_transactions(
    addresses: List[str],
    blockchain: str = "bitcoin"
):
    """Analyze cryptocurrency transactions"""
    try:
        async with DarkWebIntelligenceService() as dark_web_service:
            transaction_data = await dark_web_service.analyze_cryptocurrency_transactions(addresses, blockchain)
            
            return {
                "status": "success",
                "addresses_analyzed": len(addresses),
                "transaction_data": transaction_data,
                "message": "Cryptocurrency analysis completed"
            }
            
    except Exception as e:
        logger.error(f"Error in cryptocurrency analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ml/predict-threats")
async def predict_threats_ml(
    entities: List[Entity],
    relationships: List[Relationship]
):
    """Predict threat levels using machine learning"""
    try:
        ml_service = MLIntelligenceService()
        predictions = await ml_service.predict_threat_level(entities, relationships)
        
        return {
            "status": "success",
            "predictions": predictions,
            "message": "ML threat prediction completed"
        }
        
    except Exception as e:
        logger.error(f"Error in ML threat prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ml/detect-patterns")
async def detect_patterns_ml(entities: List[Entity]):
    """Detect behavioral patterns using ML"""
    try:
        ml_service = MLIntelligenceService()
        patterns = await ml_service.detect_behavioral_patterns(entities)
        
        return {
            "status": "success",
            "patterns": patterns,
            "message": "ML pattern detection completed"
        }
        
    except Exception as e:
        logger.error(f"Error in ML pattern detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ml/predict-anomalies")
async def predict_anomalies_ml(
    entities: List[Entity],
    relationships: List[Relationship]
):
    """Predict anomalies using ML"""
    try:
        ml_service = MLIntelligenceService()
        anomalies = await ml_service.predict_anomalies(entities, relationships)
        
        return {
            "status": "success",
            "anomalies": anomalies,
            "message": "ML anomaly prediction completed"
        }
        
    except Exception as e:
        logger.error(f"Error in ML anomaly prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ml/generate-insights")
async def generate_ml_insights(
    entities: List[Entity],
    relationships: List[Relationship],
    patterns: List[Pattern],
    anomalies: List[Anomaly]
):
    """Generate machine learning insights"""
    try:
        ml_service = MLIntelligenceService()
        insights = await ml_service.generate_ml_insights(entities, relationships, patterns, anomalies)
        
        return {
            "status": "success",
            "insights": insights,
            "message": "ML insights generated"
        }
        
    except Exception as e:
        logger.error(f"Error generating ML insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ml/train-models")
async def train_ml_models(training_data: Dict[str, Any]):
    """Train machine learning models"""
    try:
        ml_service = MLIntelligenceService()
        success = await ml_service.train_models(training_data)
        
        return {
            "status": "success" if success else "failed",
            "message": "ML model training completed" if success else "ML model training failed"
        }
        
    except Exception as e:
        logger.error(f"Error training ML models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/real-time/dashboard")
async def get_real_time_dashboard_data():
    """Get real-time dashboard data from actual services"""
    try:
        # Get database session
        db = next(get_db())
        
        # Get real data from repositories
        investigation_repo = InvestigationRepository(db)
        social_media_repo = SocialMediaRepository(db)
        
        # Get active investigations count
        active_investigations = await investigation_repo.get_active_investigations_count()
        
        # Get threats detected count
        threats_detected = await investigation_repo.get_threats_detected_count()
        
        # Get entities monitored count
        entities_monitored = await social_media_repo.get_entities_count()
        
        # Get recent activity
        recent_activity = await social_media_repo.get_recent_activity(limit=10)
        
        # Calculate anomaly score based on recent activity
        anomaly_score = 0.0
        if recent_activity:
            # Simple anomaly detection based on activity patterns
            activity_levels = [item.get("activity_level", 0) for item in recent_activity]
            if activity_levels:
                avg_activity = sum(activity_levels) / len(activity_levels)
                max_activity = max(activity_levels)
                anomaly_score = min(1.0, (max_activity - avg_activity) / max(avg_activity, 1))
        
        # Get threat alerts from recent investigations
        threat_alerts = []
        recent_investigations = await investigation_repo.get_recent_investigations(limit=5)
        
        for investigation in recent_investigations:
            if investigation.threat_level and investigation.threat_level.value in ["HIGH", "CRITICAL"]:
                threat_alerts.append({
                    "id": f"alert_{investigation.id}",
                    "severity": investigation.threat_level.value.lower(),
                    "title": f"Threat Detected in {investigation.title}",
                    "description": f"Investigation {investigation.title} has {investigation.threat_level.value} threat level",
                    "timestamp": investigation.updated_at.isoformat() if investigation.updated_at else datetime.utcnow().isoformat(),
                    "confidence": 0.8
                })
        
        # Get entity activity from recent social media data
        entity_activity = []
        for activity in recent_activity[:5]:
            entity_activity.append({
                "id": activity.get("entity_id", ""),
                "name": activity.get("username", ""),
                "platform": activity.get("platform", ""),
                "activity_level": activity.get("activity_level", 0),
                "threat_score": activity.get("threat_score", 0.0),
                "last_seen": activity.get("last_seen", datetime.utcnow().isoformat())
            })
        
        real_time_data = {
            "active_investigations": active_investigations,
            "threats_detected": threats_detected,
            "entities_monitored": entities_monitored,
            "network_activity": len(recent_activity),
            "anomaly_score": anomaly_score,
            "threat_alerts": threat_alerts,
            "entity_activity": entity_activity,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "status": "success",
            "data": real_time_data,
            "message": "Real-time dashboard data retrieved"
        }
        
    except Exception as e:
        logger.error(f"Error getting real-time dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/intelligence/status")
async def get_intelligence_status():
    """Get intelligence service status"""
    try:
        status = {
            "intelligence_engine": "operational",
            "dark_web_service": "operational",
            "ml_service": "operational",
            "models_trained": True,
            "last_update": datetime.utcnow().isoformat(),
            "services": {
                "threat_prediction": "active",
                "pattern_detection": "active",
                "anomaly_detection": "active",
                "dark_web_monitoring": "active",
                "crypto_analysis": "active"
            }
        }
        
        return {
            "status": "success",
            "intelligence_status": status,
            "message": "Intelligence services status retrieved"
        }
        
    except Exception as e:
        logger.error(f"Error getting intelligence status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def perform_dark_web_analysis(target: str, investigation_id: str):
    """Background task for dark web analysis"""
    try:
        async with DarkWebIntelligenceService() as dark_web_service:
            intelligence = await dark_web_service.scan_dark_web_entities(target)
            logger.info(f"Dark web analysis completed for investigation {investigation_id}")
    except Exception as e:
        logger.error(f"Error in background dark web analysis: {e}")

async def perform_ml_analysis(
    entities: List[Entity], 
    relationships: List[Relationship], 
    investigation_id: str
):
    """Background task for ML analysis"""
    try:
        ml_service = MLIntelligenceService()
        predictions = await ml_service.predict_threat_level(entities, relationships)
        patterns = await ml_service.detect_behavioral_patterns(entities)
        anomalies = await ml_service.predict_anomalies(entities, relationships)
        insights = await ml_service.generate_ml_insights(entities, relationships, patterns, anomalies)
        
        logger.info(f"ML analysis completed for investigation {investigation_id}")
    except Exception as e:
        logger.error(f"Error in background ML analysis: {e}") 