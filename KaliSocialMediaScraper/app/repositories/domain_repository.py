"""
Domain repository for database operations
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime

from .base_repository import BaseRepository
from app.models.database import DomainData

class DomainRepository(BaseRepository[DomainData]):
    """Repository for domain data operations"""
    
    def __init__(self, db: Session):
        super().__init__(DomainData, db)
    
    def get_by_investigation(self, investigation_id: int) -> List[DomainData]:
        """Get domain data by investigation"""
        return self.db.query(DomainData).filter(
            DomainData.investigation_id == investigation_id
        ).all()
    
    def get_by_domain(self, domain: str) -> List[DomainData]:
        """Get domain data by domain name"""
        return self.db.query(DomainData).filter(
            DomainData.domain == domain
        ).all()
    
    def get_high_threat_domains(self, threshold: float = 0.7) -> List[DomainData]:
        """Get domains with high threat scores"""
        return self.db.query(DomainData).filter(
            DomainData.threat_score >= threshold
        ).all()
    
    def get_recent_domains(self, limit: int = 50) -> List[DomainData]:
        """Get recently analyzed domains"""
        return self.db.query(DomainData).order_by(
            desc(DomainData.collected_at)
        ).limit(limit).all()
    
    def update_threat_score(self, domain_id: int, threat_score: float, indicators: List[str]) -> bool:
        """Update domain threat score and indicators"""
        domain = self.get(domain_id)
        if domain:
            domain.threat_score = threat_score
            domain.threat_indicators = indicators
            domain.collected_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def get_domain_statistics(self) -> Dict[str, Any]:
        """Get domain data statistics"""
        total_domains = self.count()
        high_threat_domains = len(self.get_high_threat_domains())
        
        return {
            "total_domains": total_domains,
            "high_threat_domains": high_threat_domains,
            "threat_rate": (high_threat_domains / total_domains * 100) if total_domains > 0 else 0
        } 