"""
Investigation repository for database operations
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime
import asyncio

from .base_repository import BaseRepository
from app.models.database import Investigation, InvestigationFinding, InvestigationReport, SocialMediaData, DomainData, NetworkData

class InvestigationRepository(BaseRepository[Investigation]):
    """Repository for investigation operations"""
    
    def __init__(self, db: Session = None):
        super().__init__(Investigation, db)
    
    # Sync methods for Celery tasks
    def create_investigation(self, investigation_data: Dict[str, Any]) -> Investigation:
        """Create a new investigation"""
        investigation = Investigation(**investigation_data)
        self.db.add(investigation)
        self.db.commit()
        self.db.refresh(investigation)
        return investigation
    
    def get_investigation(self, investigation_id: str) -> Optional[Investigation]:
        """Get investigation by ID"""
        return self.db.query(Investigation).filter(Investigation.id == investigation_id).first()
    
    def update_investigation_status(self, investigation_id: str, status: str) -> bool:
        """Update investigation status"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.status = status
            investigation.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def add_github_data(self, investigation_id: str, github_data: Dict[str, Any]) -> bool:
        """Add GitHub data to investigation"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            if not investigation.github_data:
                investigation.github_data = []
            investigation.github_data.append(github_data)
            self.db.commit()
            return True
        return False
    
    def add_social_media_data(self, investigation_id: str, social_data: Dict[str, Any]) -> bool:
        """Add social media data to investigation"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            if not investigation.social_media_data:
                investigation.social_media_data = []
            investigation.social_media_data.append(social_data)
            self.db.commit()
            return True
        return False
    
    def add_domain_data(self, investigation_id: str, domain_data: Dict[str, Any]) -> bool:
        """Add domain data to investigation"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            if not investigation.domain_data:
                investigation.domain_data = []
            investigation.domain_data.append(domain_data)
            self.db.commit()
            return True
        return False
    
    def save_analysis_results(self, investigation_id: str, analysis_result: Any) -> bool:
        """Save analysis results"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.analysis_results = analysis_result.dict() if hasattr(analysis_result, 'dict') else analysis_result
            self.db.commit()
            return True
        return False
    
    def save_intelligence_report(self, investigation_id: str, intelligence_report: Any) -> bool:
        """Save intelligence report"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.intelligence_report = intelligence_report.dict() if hasattr(intelligence_report, 'dict') else intelligence_report
            self.db.commit()
            return True
        return False
    
    def save_resolved_entities(self, investigation_id: str, resolved_entities: List[Any]) -> bool:
        """Save resolved entities"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.resolved_entities = [e.dict() if hasattr(e, 'dict') else e for e in resolved_entities]
            self.db.commit()
            return True
        return False
    
    def save_patterns(self, investigation_id: str, patterns: List[Any]) -> bool:
        """Save patterns"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.patterns = [p.dict() if hasattr(p, 'dict') else p for p in patterns]
            self.db.commit()
            return True
        return False
    
    def save_anomalies(self, investigation_id: str, anomalies: List[Any]) -> bool:
        """Save anomalies"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.anomalies = [a.dict() if hasattr(a, 'dict') else a for a in anomalies]
            self.db.commit()
            return True
        return False
    
    def save_threat_assessments(self, investigation_id: str, threat_assessments: List[Any]) -> bool:
        """Save threat assessments"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.threat_assessments = [t.dict() if hasattr(t, 'dict') else t for t in threat_assessments]
            self.db.commit()
            return True
        return False
    
    def get_patterns(self, investigation_id: str) -> List[Any]:
        """Get patterns for investigation"""
        investigation = self.get_investigation(investigation_id)
        return investigation.patterns if investigation and investigation.patterns else []
    
    def get_anomalies(self, investigation_id: str) -> List[Any]:
        """Get anomalies for investigation"""
        investigation = self.get_investigation(investigation_id)
        return investigation.anomalies if investigation and investigation.anomalies else []
    
    def get_relationships(self, investigation_id: str) -> List[Any]:
        """Get relationships for investigation"""
        investigation = self.get_investigation(investigation_id)
        return investigation.relationships if investigation and investigation.relationships else []
    
    def get_intelligence_report(self, investigation_id: str) -> Optional[Any]:
        """Get intelligence report for investigation"""
        investigation = self.get_investigation(investigation_id)
        return investigation.intelligence_report if investigation else None
    
    def save_executive_summary(self, investigation_id: str, executive_summary: Dict[str, Any]) -> bool:
        """Save executive summary"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.executive_summary = executive_summary
            self.db.commit()
            return True
        return False
    
    def save_threat_report(self, investigation_id: str, threat_report: Dict[str, Any]) -> bool:
        """Save threat report"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.threat_report = threat_report
            self.db.commit()
            return True
        return False
    
    def save_network_report(self, investigation_id: str, network_report: Dict[str, Any]) -> bool:
        """Save network report"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            investigation.network_report = network_report
            self.db.commit()
            return True
        return False
    
    def save_export_file(self, investigation_id: str, export_file: bytes, export_format: str) -> str:
        """Save export file and return path"""
        # This would implement actual file saving
        # For now, return a placeholder path
        return f"exports/{investigation_id}_{export_format}.{export_format}"
    
    def get_old_investigations(self, cutoff_date: datetime) -> List[Investigation]:
        """Get old investigations for cleanup"""
        return self.db.query(Investigation).filter(
            Investigation.created_at < cutoff_date,
            Investigation.status.in_(["completed", "failed"])
        ).all()
    
    def delete_investigation(self, investigation_id: str) -> bool:
        """Delete investigation"""
        investigation = self.get_investigation(investigation_id)
        if investigation:
            self.db.delete(investigation)
            self.db.commit()
            return True
        return False
    
    # Original methods
    def get_by_status(self, status: str) -> List[Investigation]:
        """Get investigations by status"""
        return self.db.query(Investigation).filter(Investigation.status == status).all()
    
    def get_by_target(self, target_type: str, target_value: str) -> List[Investigation]:
        """Get investigations by target"""
        return self.db.query(Investigation).filter(
            and_(
                Investigation.target_type == target_type,
                Investigation.target_value == target_value
            )
        ).all()
    
    def get_recent(self, limit: int = 10) -> List[Investigation]:
        """Get recent investigations"""
        return self.db.query(Investigation).order_by(
            desc(Investigation.created_at)
        ).limit(limit).all()
    
    def get_by_user(self, user_id: int) -> List[Investigation]:
        """Get investigations by user"""
        return self.db.query(Investigation).filter(
            Investigation.created_by_id == user_id
        ).all()
    
    def get_with_findings(self, investigation_id: int) -> Optional[Investigation]:
        """Get investigation with all findings"""
        return self.db.query(Investigation).filter(
            Investigation.id == investigation_id
        ).first()
    
    def update_progress(self, investigation_id: int, progress: int, current_step: str = None) -> bool:
        """Update investigation progress"""
        investigation = self.get(investigation_id)
        if investigation:
            investigation.progress = progress
            if current_step:
                investigation.current_step = current_step
            investigation.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def start_investigation(self, investigation_id: int) -> bool:
        """Mark investigation as started"""
        investigation = self.get(investigation_id)
        if investigation:
            investigation.status = "running"
            investigation.started_at = datetime.utcnow()
            investigation.progress = 0
            self.db.commit()
            return True
        return False
    
    def complete_investigation(self, investigation_id: int) -> bool:
        """Mark investigation as completed"""
        investigation = self.get(investigation_id)
        if investigation:
            investigation.status = "completed"
            investigation.completed_at = datetime.utcnow()
            investigation.progress = 100
            self.db.commit()
            return True
        return False
    
    def fail_investigation(self, investigation_id: int, error_message: str = None) -> bool:
        """Mark investigation as failed"""
        investigation = self.get(investigation_id)
        if investigation:
            investigation.status = "failed"
            investigation.completed_at = datetime.utcnow()
            if error_message:
                # Store error in analysis_options
                if not investigation.analysis_options:
                    investigation.analysis_options = {}
                investigation.analysis_options["error_message"] = error_message
            self.db.commit()
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get investigation statistics"""
        total = self.count()
        pending = len(self.get_by_status("pending"))
        running = len(self.get_by_status("running"))
        completed = len(self.get_by_status("completed"))
        failed = len(self.get_by_status("failed"))
        
        return {
            "total": total,
            "pending": pending,
            "running": running,
            "completed": completed,
            "failed": failed,
            "success_rate": (completed / total * 100) if total > 0 else 0
        } 