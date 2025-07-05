"""
Report Generation Background Tasks
"""

import asyncio
import logging
import json
import csv
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
import zipfile
import io

from app.core.celery_app import celery_app
from app.repositories.investigation_repository import InvestigationRepository
from app.services.intelligence_engine import IntelligenceEngine
from app.models.schemas import Investigation, IntelligenceReport

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def generate_intelligence_report_task(self, investigation_id: str) -> Dict[str, Any]:
    """Generate comprehensive intelligence report for an investigation"""
    try:
        logger.info(f"Starting intelligence report generation for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading investigation data", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = await investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize intelligence engine
        intelligence_engine = IntelligenceEngine()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Running analysis", "progress": 30}
        )
        
        # Run analysis if not already done
        analysis_result = await intelligence_engine.analyze_investigation(investigation)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Generating report", "progress": 70}
        )
        
        # Generate intelligence report
        intelligence_report = await intelligence_engine.generate_intelligence_report(analysis_result)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Saving report", "progress": 90}
        )
        
        # Save report
        await investigation_repo.save_intelligence_report(investigation_id, intelligence_report)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Report generation completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "report_id": intelligence_report.id,
            "report_title": intelligence_report.title,
            "confidence_score": intelligence_report.confidence_score,
            "key_findings_count": len(intelligence_report.key_findings),
            "recommendations_count": len(intelligence_report.recommendations)
        }
        
    except Exception as e:
        logger.error(f"Error generating intelligence report for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def generate_executive_summary_task(self, investigation_id: str) -> Dict[str, Any]:
    """Generate executive summary for an investigation"""
    try:
        logger.info(f"Starting executive summary generation for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading data", "progress": 20}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = await investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Get existing intelligence report or generate new one
        intelligence_report = await investigation_repo.get_intelligence_report(investigation_id)
        
        if not intelligence_report:
            # Generate new report
            intelligence_engine = IntelligenceEngine()
            analysis_result = await intelligence_engine.analyze_investigation(investigation)
            intelligence_report = await intelligence_engine.generate_intelligence_report(analysis_result)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Generating executive summary", "progress": 80}
        )
        
        # Create executive summary
        executive_summary = {
            "investigation_id": investigation_id,
            "title": investigation.title,
            "description": investigation.description,
            "executive_summary": intelligence_report.executive_summary,
            "key_findings": intelligence_report.key_findings[:5],  # Top 5 findings
            "threat_assessment": intelligence_report.threat_assessment,
            "recommendations": intelligence_report.recommendations[:3],  # Top 3 recommendations
            "confidence_score": intelligence_report.confidence_score,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        # Save executive summary
        await investigation_repo.save_executive_summary(investigation_id, executive_summary)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Executive summary completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "executive_summary": executive_summary
        }
        
    except Exception as e:
        logger.error(f"Error generating executive summary for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def export_investigation_data_task(self, investigation_id: str, export_format: str = "json") -> Dict[str, Any]:
    """Export investigation data in various formats"""
    try:
        logger.info(f"Starting data export for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading investigation data", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = await investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Preparing export data", "progress": 30}
        )
        
        # Prepare export data
        export_data = await prepare_export_data(investigation, investigation_repo)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": f"Generating {export_format} export", "progress": 60}
        )
        
        # Generate export based on format
        if export_format == "json":
            export_file = generate_json_export(export_data, investigation_id)
        elif export_format == "csv":
            export_file = generate_csv_export(export_data, investigation_id)
        elif export_format == "zip":
            export_file = generate_zip_export(export_data, investigation_id)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Saving export file", "progress": 90}
        )
        
        # Save export file
        export_path = await investigation_repo.save_export_file(investigation_id, export_file, export_format)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Export completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "export_format": export_format,
            "export_path": export_path,
            "file_size": len(export_file)
        }
        
    except Exception as e:
        logger.error(f"Error exporting investigation data for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def generate_threat_report_task(self, investigation_id: str) -> Dict[str, Any]:
    """Generate detailed threat assessment report"""
    try:
        logger.info(f"Starting threat report generation for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading threat data", "progress": 20}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = await investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Get threat assessments
        threat_assessments = await investigation_repo.get_threat_assessments(investigation_id)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing threats", "progress": 50}
        )
        
        # Generate threat report
        threat_report = {
            "investigation_id": investigation_id,
            "title": f"Threat Assessment Report - {investigation.title}",
            "generated_at": datetime.utcnow().isoformat(),
            "total_threats": len(threat_assessments),
            "high_threats": len([t for t in threat_assessments if t.threat_level == "HIGH"]),
            "medium_threats": len([t for t in threat_assessments if t.threat_level == "MEDIUM"]),
            "low_threats": len([t for t in threat_assessments if t.threat_level == "LOW"]),
            "threat_assessments": [
                {
                    "target": t.target,
                    "target_type": t.target_type,
                    "threat_level": t.threat_level,
                    "threat_score": t.threat_score,
                    "indicators": t.indicators,
                    "assessment_timestamp": t.assessment_timestamp.isoformat()
                }
                for t in threat_assessments
            ],
            "summary": {
                "overall_risk_level": "HIGH" if len([t for t in threat_assessments if t.threat_level == "HIGH"]) > 0 else "MEDIUM",
                "critical_threats": len([t for t in threat_assessments if t.threat_score > 0.8]),
                "recommended_actions": generate_threat_recommendations(threat_assessments)
            }
        }
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Saving threat report", "progress": 80}
        )
        
        # Save threat report
        await investigation_repo.save_threat_report(investigation_id, threat_report)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Threat report completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "threat_report": threat_report
        }
        
    except Exception as e:
        logger.error(f"Error generating threat report for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def generate_network_analysis_report_task(self, investigation_id: str) -> Dict[str, Any]:
    """Generate network analysis report"""
    try:
        logger.info(f"Starting network analysis report generation for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Loading network data", "progress": 20}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = await investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Get relationships and patterns
        relationships = await investigation_repo.get_relationships(investigation_id)
        patterns = await investigation_repo.get_patterns(investigation_id)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing network", "progress": 50}
        )
        
        # Generate network analysis report
        network_report = {
            "investigation_id": investigation_id,
            "title": f"Network Analysis Report - {investigation.title}",
            "generated_at": datetime.utcnow().isoformat(),
            "network_statistics": {
                "total_relationships": len(relationships),
                "relationship_types": count_relationship_types(relationships),
                "network_patterns": len([p for p in patterns if p.pattern_type == "network"]),
                "centrality_analysis": analyze_network_centrality(relationships)
            },
            "key_entities": identify_key_entities(relationships),
            "network_patterns": [
                {
                    "id": p.id,
                    "pattern_type": p.pattern_type,
                    "category": p.category,
                    "title": p.title,
                    "description": p.description,
                    "confidence": p.confidence,
                    "severity": p.severity
                }
                for p in patterns if p.pattern_type == "network"
            ],
            "recommendations": generate_network_recommendations(relationships, patterns)
        }
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Saving network report", "progress": 80}
        )
        
        # Save network report
        await investigation_repo.save_network_report(investigation_id, network_report)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Network report completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "network_report": network_report
        }
        
    except Exception as e:
        logger.error(f"Error generating network analysis report for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

# Helper functions
async def prepare_export_data(investigation: Investigation, investigation_repo: InvestigationRepository) -> Dict[str, Any]:
    """Prepare data for export"""
    try:
        # Get all related data
        github_data = await investigation_repo.get_github_data(investigation.id)
        social_media_data = await investigation_repo.get_social_media_data(investigation.id)
        domain_data = await investigation_repo.get_domain_data(investigation.id)
        analysis_results = await investigation_repo.get_analysis_results(investigation.id)
        intelligence_report = await investigation_repo.get_intelligence_report(investigation.id)
        
        return {
            "investigation": investigation.dict(),
            "github_data": [data.dict() for data in github_data],
            "social_media_data": [data.dict() for data in social_media_data],
            "domain_data": [data.dict() for data in domain_data],
            "analysis_results": analysis_results.dict() if analysis_results else None,
            "intelligence_report": intelligence_report.dict() if intelligence_report else None
        }
        
    except Exception as e:
        logger.error(f"Error preparing export data: {e}")
        raise

def generate_json_export(export_data: Dict[str, Any], investigation_id: str) -> bytes:
    """Generate JSON export"""
    try:
        json_data = json.dumps(export_data, indent=2, default=str)
        return json_data.encode('utf-8')
        
    except Exception as e:
        logger.error(f"Error generating JSON export: {e}")
        raise

def generate_csv_export(export_data: Dict[str, Any], investigation_id: str) -> bytes:
    """Generate CSV export"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write investigation data
        writer.writerow(["Investigation Data"])
        writer.writerow(["ID", "Title", "Description", "Status", "Created At"])
        investigation = export_data["investigation"]
        writer.writerow([
            investigation["id"],
            investigation["title"],
            investigation["description"],
            investigation["status"],
            investigation["created_at"]
        ])
        
        # Write GitHub data
        if export_data["github_data"]:
            writer.writerow([])
            writer.writerow(["GitHub Data"])
            writer.writerow(["Type", "Value", "Data"])
            for data in export_data["github_data"]:
                writer.writerow([data.get("type"), data.get("value"), str(data.get("data"))])
        
        # Write social media data
        if export_data["social_media_data"]:
            writer.writerow([])
            writer.writerow(["Social Media Data"])
            writer.writerow(["Platform", "Username", "Data"])
            for data in export_data["social_media_data"]:
                writer.writerow([data.get("platform"), data.get("username"), str(data.get("data"))])
        
        return output.getvalue().encode('utf-8')
        
    except Exception as e:
        logger.error(f"Error generating CSV export: {e}")
        raise

def generate_zip_export(export_data: Dict[str, Any], investigation_id: str) -> bytes:
    """Generate ZIP export with multiple files"""
    try:
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add JSON export
            json_data = json.dumps(export_data, indent=2, default=str)
            zip_file.writestr(f"{investigation_id}_full_export.json", json_data)
            
            # Add CSV export
            csv_data = generate_csv_export(export_data, investigation_id)
            zip_file.writestr(f"{investigation_id}_data.csv", csv_data.decode('utf-8'))
            
            # Add investigation summary
            summary = {
                "investigation_id": investigation_id,
                "export_timestamp": datetime.utcnow().isoformat(),
                "data_summary": {
                    "github_entries": len(export_data.get("github_data", [])),
                    "social_media_entries": len(export_data.get("social_media_data", [])),
                    "domain_entries": len(export_data.get("domain_data", [])),
                    "has_analysis": export_data.get("analysis_results") is not None,
                    "has_intelligence_report": export_data.get("intelligence_report") is not None
                }
            }
            summary_json = json.dumps(summary, indent=2)
            zip_file.writestr(f"{investigation_id}_summary.json", summary_json)
        
        return zip_buffer.getvalue()
        
    except Exception as e:
        logger.error(f"Error generating ZIP export: {e}")
        raise

def generate_threat_recommendations(threat_assessments: List) -> List[str]:
    """Generate recommendations based on threat assessments"""
    try:
        recommendations = []
        
        high_threats = [t for t in threat_assessments if t.threat_level == "HIGH"]
        if high_threats:
            recommendations.append("Immediate action required for high-threat entities")
            recommendations.append("Implement enhanced monitoring for critical threats")
        
        medium_threats = [t for t in threat_assessments if t.threat_level == "MEDIUM"]
        if medium_threats:
            recommendations.append("Monitor medium-threat entities closely")
            recommendations.append("Consider additional investigation for suspicious patterns")
        
        if not recommendations:
            recommendations.append("Continue standard monitoring procedures")
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating threat recommendations: {e}")
        return ["Continue monitoring"]

def count_relationship_types(relationships: List) -> Dict[str, int]:
    """Count relationship types"""
    try:
        counts = {}
        for rel in relationships:
            rel_type = rel.relationship_type
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts
        
    except Exception as e:
        logger.error(f"Error counting relationship types: {e}")
        return {}

def analyze_network_centrality(relationships: List) -> Dict[str, Any]:
    """Analyze network centrality"""
    try:
        # Simple centrality analysis
        entity_centrality = {}
        for rel in relationships:
            source = rel.source_id
            target = rel.target_id
            
            entity_centrality[source] = entity_centrality.get(source, 0) + 1
            entity_centrality[target] = entity_centrality.get(target, 0) + 1
        
        if entity_centrality:
            max_centrality = max(entity_centrality.values())
            avg_centrality = sum(entity_centrality.values()) / len(entity_centrality)
            
            return {
                "max_centrality": max_centrality,
                "average_centrality": avg_centrality,
                "high_centrality_entities": len([c for c in entity_centrality.values() if c > avg_centrality * 2])
            }
        
        return {"max_centrality": 0, "average_centrality": 0, "high_centrality_entities": 0}
        
    except Exception as e:
        logger.error(f"Error analyzing network centrality: {e}")
        return {"error": str(e)}

def identify_key_entities(relationships: List) -> List[Dict[str, Any]]:
    """Identify key entities in the network"""
    try:
        entity_centrality = {}
        for rel in relationships:
            source = rel.source_id
            target = rel.target_id
            
            entity_centrality[source] = entity_centrality.get(source, 0) + 1
            entity_centrality[target] = entity_centrality.get(target, 0) + 1
        
        # Get top entities by centrality
        sorted_entities = sorted(entity_centrality.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {
                "entity_id": entity_id,
                "centrality_score": score,
                "rank": i + 1
            }
            for i, (entity_id, score) in enumerate(sorted_entities[:10])  # Top 10
        ]
        
    except Exception as e:
        logger.error(f"Error identifying key entities: {e}")
        return []

def generate_network_recommendations(relationships: List, patterns: List) -> List[str]:
    """Generate network analysis recommendations"""
    try:
        recommendations = []
        
        # Analyze relationship density
        if len(relationships) > 100:
            recommendations.append("High relationship density detected - consider network clustering analysis")
        
        # Analyze patterns
        network_patterns = [p for p in patterns if p.pattern_type == "network"]
        if network_patterns:
            recommendations.append("Network patterns detected - investigate relationship clusters")
        
        # Analyze centrality
        entity_centrality = {}
        for rel in relationships:
            source = rel.source_id
            target = rel.target_id
            entity_centrality[source] = entity_centrality.get(source, 0) + 1
            entity_centrality[target] = entity_centrality.get(target, 0) + 1
        
        if entity_centrality:
            avg_centrality = sum(entity_centrality.values()) / len(entity_centrality)
            high_centrality = [c for c in entity_centrality.values() if c > avg_centrality * 2]
            
            if high_centrality:
                recommendations.append("High centrality entities detected - investigate influence patterns")
        
        if not recommendations:
            recommendations.append("Continue standard network monitoring")
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating network recommendations: {e}")
        return ["Continue monitoring"] 