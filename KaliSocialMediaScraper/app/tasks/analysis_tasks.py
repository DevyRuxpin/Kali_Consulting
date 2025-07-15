"""
Analysis Background Tasks
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from celery import current_task

from app.core.celery_app import celery_app
from app.services.intelligence_engine import IntelligenceEngine
from app.services.entity_resolver import EntityResolver
from app.services.pattern_analyzer import PatternAnalyzer
from app.services.anomaly_detector import AnomalyDetector
from app.services.threat_correlator import ThreatCorrelator
from app.repositories.investigation_repository import InvestigationRepository
from app.models.schemas import Investigation, AnalysisResult

logger = logging.getLogger(__name__)

def run_async(coro):
    """Helper function to run async coroutines in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@celery_app.task(bind=True)
def run_comprehensive_analysis_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run comprehensive intelligence analysis for an investigation"""
    try:
        logger.info(f"Starting comprehensive analysis for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Initializing analysis", "progress": 5}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = run_async(investigation_repo.get_investigation(investigation_id))
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize intelligence engine
        intelligence_engine = IntelligenceEngine()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Extracting entities", "progress": 20}
        )
        
        # Run comprehensive analysis
        analysis_result = run_async(intelligence_engine.analyze_investigation(
            investigation, analysis_depth="comprehensive"
        ))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Generating intelligence report", "progress": 80}
        )
        
        # Generate intelligence report
        intelligence_report = run_async(intelligence_engine.generate_intelligence_report(analysis_result))
        
        # Save analysis results
        run_async(investigation_repo.save_analysis_results(investigation_id, analysis_result))
        run_async(investigation_repo.save_intelligence_report(investigation_id, intelligence_report))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analysis completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "entities_analyzed": len(analysis_result.entities),
            "relationships_found": len(analysis_result.relationships),
            "patterns_detected": len(analysis_result.patterns),
            "anomalies_identified": len(analysis_result.anomalies),
            "threat_assessments": len(analysis_result.threat_assessments),
            "confidence_score": analysis_result.confidence_score,
            "report_id": intelligence_report.id
        }
        
    except Exception as e:
        logger.error(f"Error running comprehensive analysis for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_entity_resolution_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run entity resolution for an investigation"""
    try:
        logger.info(f"Starting entity resolution for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading entities", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = run_async(investigation_repo.get_investigation(investigation_id))
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize entity resolver
        entity_resolver = EntityResolver()
        
        # Extract entities from investigation
        entities = run_async(intelligence_engine._extract_entities(investigation))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Resolving entities", "progress": 50}
        )
        
        # Resolve entities
        resolved_entities = run_async(entity_resolver.resolve_entities(entities))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Saving resolved entities", "progress": 80}
        )
        
        # Save resolved entities
        run_async(investigation_repo.save_resolved_entities(investigation_id, resolved_entities))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Entity resolution completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "original_entities": len(entities),
            "resolved_entities": len(resolved_entities),
            "resolution_groups": len([e for e in resolved_entities if e.metadata.get("resolved")])
        }
        
    except Exception as e:
        logger.error(f"Error running entity resolution for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_pattern_analysis_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run pattern analysis for an investigation"""
    try:
        logger.info(f"Starting pattern analysis for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading data", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = run_async(investigation_repo.get_investigation(investigation_id))
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize pattern analyzer
        pattern_analyzer = PatternAnalyzer()
        
        # Extract entities and relationships
        entities = run_async(intelligence_engine._extract_entities(investigation))
        relationships = run_async(intelligence_engine._analyze_relationships(entities, investigation))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting behavioral patterns", "progress": 30}
        )
        
        # Detect behavioral patterns
        behavioral_patterns = run_async(pattern_analyzer.detect_behavioral_patterns(entities))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting network patterns", "progress": 50}
        )
        
        # Detect network patterns
        network_patterns = run_async(pattern_analyzer.detect_network_patterns(relationships))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting temporal patterns", "progress": 70}
        )
        
        # Detect temporal patterns
        temporal_patterns = run_async(pattern_analyzer.detect_temporal_patterns(entities))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting content patterns", "progress": 90}
        )
        
        # Detect content patterns
        content_patterns = run_async(pattern_analyzer.detect_content_patterns(entities))
        
        # Combine all patterns
        all_patterns = behavioral_patterns + network_patterns + temporal_patterns + content_patterns
        
        # Save patterns
        run_async(investigation_repo.save_patterns(investigation_id, all_patterns))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Pattern analysis completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "behavioral_patterns": len(behavioral_patterns),
            "network_patterns": len(network_patterns),
            "temporal_patterns": len(temporal_patterns),
            "content_patterns": len(content_patterns),
            "total_patterns": len(all_patterns)
        }
        
    except Exception as e:
        logger.error(f"Error running pattern analysis for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_anomaly_detection_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run anomaly detection for an investigation"""
    try:
        logger.info(f"Starting anomaly detection for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading data", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = run_async(investigation_repo.get_investigation(investigation_id))
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize anomaly detector
        anomaly_detector = AnomalyDetector()
        
        # Extract entities and relationships
        entities = run_async(intelligence_engine._extract_entities(investigation))
        relationships = run_async(intelligence_engine._analyze_relationships(entities, investigation))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting behavioral anomalies", "progress": 25}
        )
        
        # Detect behavioral anomalies
        behavioral_anomalies = run_async(anomaly_detector.detect_behavioral_anomalies(entities))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting network anomalies", "progress": 50}
        )
        
        # Detect network anomalies
        network_anomalies = run_async(anomaly_detector.detect_network_anomalies(relationships))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting temporal anomalies", "progress": 75}
        )
        
        # Detect temporal anomalies
        temporal_anomalies = run_async(anomaly_detector.detect_temporal_anomalies(entities))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting content anomalies", "progress": 90}
        )
        
        # Detect content anomalies
        content_anomalies = run_async(anomaly_detector.detect_content_anomalies(entities))
        
        # Combine all anomalies
        all_anomalies = behavioral_anomalies + network_anomalies + temporal_anomalies + content_anomalies
        
        # Save anomalies
        run_async(investigation_repo.save_anomalies(investigation_id, all_anomalies))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Anomaly detection completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "behavioral_anomalies": len(behavioral_anomalies),
            "network_anomalies": len(network_anomalies),
            "temporal_anomalies": len(temporal_anomalies),
            "content_anomalies": len(content_anomalies),
            "total_anomalies": len(all_anomalies),
            "high_severity": len([a for a in all_anomalies if a.severity == "high"]),
            "medium_severity": len([a for a in all_anomalies if a.severity == "medium"]),
            "low_severity": len([a for a in all_anomalies if a.severity == "low"])
        }
        
    except Exception as e:
        logger.error(f"Error running anomaly detection for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_threat_correlation_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run threat correlation for an investigation"""
    try:
        logger.info(f"Starting threat correlation for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading data", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = run_async(investigation_repo.get_investigation(investigation_id))
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize threat correlator
        threat_correlator = ThreatCorrelator()
        
        # Extract entities, relationships, patterns, and anomalies
        entities = run_async(intelligence_engine._extract_entities(investigation))
        relationships = run_async(intelligence_engine._analyze_relationships(entities, investigation))
        
        # Get patterns and anomalies from repository
        patterns = run_async(investigation_repo.get_patterns(investigation_id))
        anomalies = run_async(investigation_repo.get_anomalies(investigation_id))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Correlating entity threats", "progress": 25}
        )
        
        # Correlate entity threats
        entity_threats = run_async(threat_correlator.correlate_entity_threats(entities))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Correlating relationship threats", "progress": 50}
        )
        
        # Correlate relationship threats
        relationship_threats = run_async(threat_correlator.correlate_relationship_threats(relationships))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Correlating pattern threats", "progress": 75}
        )
        
        # Correlate pattern threats
        pattern_threats = run_async(threat_correlator.correlate_pattern_threats(patterns))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Correlating anomaly threats", "progress": 90}
        )
        
        # Correlate anomaly threats
        anomaly_threats = run_async(threat_correlator.correlate_anomaly_threats(anomalies))
        
        # Combine all threat assessments
        all_threats = entity_threats + relationship_threats + pattern_threats + anomaly_threats
        
        # Save threat assessments
        run_async(investigation_repo.save_threat_assessments(investigation_id, all_threats))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Threat correlation completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "entity_threats": len(entity_threats),
            "relationship_threats": len(relationship_threats),
            "pattern_threats": len(pattern_threats),
            "anomaly_threats": len(anomaly_threats),
            "total_threats": len(all_threats),
            "high_threats": len([t for t in all_threats if t.threat_level == "HIGH"]),
            "medium_threats": len([t for t in all_threats if t.threat_level == "MEDIUM"]),
            "low_threats": len([t for t in all_threats if t.threat_level == "LOW"])
        }
        
    except Exception as e:
        logger.error(f"Error running threat correlation for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_quick_analysis_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run quick analysis for an investigation"""
    try:
        logger.info(f"Starting quick analysis for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Running quick analysis", "progress": 50}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = run_async(investigation_repo.get_investigation(investigation_id))
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize intelligence engine
        intelligence_engine = IntelligenceEngine()
        
        # Run quick analysis
        analysis_result = run_async(intelligence_engine.analyze_investigation(
            investigation, analysis_depth="quick"
        ))
        
        # Save analysis results
        run_async(investigation_repo.save_analysis_results(investigation_id, analysis_result))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Quick analysis completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "analysis_type": "quick",
            "entities_analyzed": len(analysis_result.entities),
            "confidence_score": analysis_result.confidence_score
        }
        
    except Exception as e:
        logger.error(f"Error running quick analysis for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_detailed_analysis_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run detailed analysis for an investigation"""
    try:
        logger.info(f"Starting detailed analysis for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Running detailed analysis", "progress": 25}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = run_async(investigation_repo.get_investigation(investigation_id))
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize intelligence engine
        intelligence_engine = IntelligenceEngine()
        
        # Run detailed analysis
        analysis_result = run_async(intelligence_engine.analyze_investigation(
            investigation, analysis_depth="detailed"
        ))
        
        # Generate intelligence report
        intelligence_report = run_async(intelligence_engine.generate_intelligence_report(analysis_result))
        
        # Save analysis results and report
        run_async(investigation_repo.save_analysis_results(investigation_id, analysis_result))
        run_async(investigation_repo.save_intelligence_report(investigation_id, intelligence_report))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detailed analysis completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "analysis_type": "detailed",
            "entities_analyzed": len(analysis_result.entities),
            "relationships_found": len(analysis_result.relationships),
            "patterns_detected": len(analysis_result.patterns),
            "anomalies_identified": len(analysis_result.anomalies),
            "threat_assessments": len(analysis_result.threat_assessments),
            "confidence_score": analysis_result.confidence_score,
            "report_id": intelligence_report.id
        }
        
    except Exception as e:
        logger.error(f"Error running detailed analysis for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

# Import intelligence engine for helper functions
from app.services.intelligence_engine import IntelligenceEngine
intelligence_engine = IntelligenceEngine() 