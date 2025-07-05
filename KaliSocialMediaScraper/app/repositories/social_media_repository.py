"""
Social media repository for database operations
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime

from .base_repository import BaseRepository
from app.models.database import SocialMediaData, SocialMediaPost, Platform

class SocialMediaRepository(BaseRepository[SocialMediaData]):
    """Repository for social media data operations"""
    
    def __init__(self, db: Session):
        super().__init__(SocialMediaData, db)
    
    def get_by_investigation(self, investigation_id: int) -> List[SocialMediaData]:
        """Get social media data by investigation"""
        return self.db.query(SocialMediaData).filter(
            SocialMediaData.investigation_id == investigation_id
        ).all()
    
    def get_by_platform(self, platform_name: str) -> List[SocialMediaData]:
        """Get social media data by platform"""
        return self.db.query(SocialMediaData).join(Platform).filter(
            Platform.name == platform_name
        ).all()
    
    def get_by_username(self, username: str) -> List[SocialMediaData]:
        """Get social media data by username"""
        return self.db.query(SocialMediaData).filter(
            SocialMediaData.username == username
        ).all()
    
    def get_high_threat_profiles(self, threshold: float = 0.7) -> List[SocialMediaData]:
        """Get profiles with high threat scores"""
        return self.db.query(SocialMediaData).filter(
            SocialMediaData.threat_score >= threshold
        ).all()
    
    def get_verified_profiles(self) -> List[SocialMediaData]:
        """Get verified profiles"""
        return self.db.query(SocialMediaData).filter(
            SocialMediaData.is_verified == True
        ).all()
    
    def get_recent_posts(self, limit: int = 100) -> List[SocialMediaPost]:
        """Get recent social media posts"""
        return self.db.query(SocialMediaPost).order_by(
            desc(SocialMediaPost.collected_at)
        ).limit(limit).all()
    
    def get_posts_by_profile(self, profile_id: int) -> List[SocialMediaPost]:
        """Get posts by profile"""
        return self.db.query(SocialMediaPost).filter(
            SocialMediaPost.profile_id == profile_id
        ).all()
    
    def get_high_engagement_posts(self, min_likes: int = 100) -> List[SocialMediaPost]:
        """Get posts with high engagement"""
        return self.db.query(SocialMediaPost).filter(
            SocialMediaPost.likes_count >= min_likes
        ).all()
    
    def update_threat_score(self, profile_id: int, threat_score: float, indicators: List[str]) -> bool:
        """Update profile threat score and indicators"""
        profile = self.get(profile_id)
        if profile:
            profile.threat_score = threat_score
            profile.threat_indicators = indicators
            profile.collected_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def get_social_media_statistics(self) -> Dict[str, Any]:
        """Get social media data statistics"""
        total_profiles = self.count()
        verified_profiles = len(self.get_verified_profiles())
        high_threat_profiles = len(self.get_high_threat_profiles())
        
        return {
            "total_profiles": total_profiles,
            "verified_profiles": verified_profiles,
            "high_threat_profiles": high_threat_profiles,
            "verification_rate": (verified_profiles / total_profiles * 100) if total_profiles > 0 else 0
        } 