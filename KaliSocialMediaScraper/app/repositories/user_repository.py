"""
User repository for database operations
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime

from .base_repository import BaseRepository
from app.models.database import User

class UserRepository(BaseRepository[User]):
    """Repository for user operations"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.get_by_field("username", username)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.get_by_field("email", email)
    
    def get_active_users(self) -> List[User]:
        """Get all active users"""
        return self.db.query(User).filter(User.is_active == True).all()
    
    def get_superusers(self) -> List[User]:
        """Get all superusers"""
        return self.db.query(User).filter(User.is_superuser == True).all()
    
    def create_user(self, username: str, email: str, hashed_password: str, full_name: str = None) -> User:
        """Create a new user"""
        user_data = {
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "full_name": full_name,
            "is_active": True,
            "is_superuser": False
        }
        return self.create(user_data)
    
    def update_user_status(self, user_id: int, is_active: bool) -> bool:
        """Update user active status"""
        user = self.get(user_id)
        if user:
            user.is_active = is_active
            user.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def promote_to_superuser(self, user_id: int) -> bool:
        """Promote user to superuser"""
        user = self.get(user_id)
        if user:
            user.is_superuser = True
            user.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics"""
        total = self.count()
        active = len(self.get_active_users())
        superusers = len(self.get_superusers())
        
        return {
            "total": total,
            "active": active,
            "superusers": superusers,
            "inactive": total - active
        } 