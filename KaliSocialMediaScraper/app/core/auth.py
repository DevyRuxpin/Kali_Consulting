"""
Simplified API Key Authentication for Single User
"""

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging
from datetime import timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# API Key authentication
security = HTTPBearer()

class APIKeyAuth:
    """Simple API Key authentication for single user"""
    
    def __init__(self):
        self.api_key = settings.API_KEY
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def verify_api_key(self, api_key: str) -> bool:
        """Verify API key"""
        return api_key == self.api_key
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_user(self, db: Session, username: str, email: str, password: str, full_name: Optional[str] = None):
        """Create a new user"""
        from app.models.database import User
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Username already registered"
            )
        
        # Create new user
        hashed_password = self.get_password_hash(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_superuser=False
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def authenticate_user(self, db: Session, username: str, password: str):
        """Authenticate a user"""
        from app.models.database import User
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, str(user.hashed_password)):
            return None
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create an access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = expires_delta
        else:
            expire = timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Get current user (always returns admin user)"""
        if not self.verify_api_key(credentials.credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Return a simple user object for single-user system
        return {
            "id": 1,
            "username": "admin",
            "email": "admin@kali-osint.local",
            "is_active": True,
            "is_superuser": True
        }

# Global auth instance
auth_service = APIKeyAuth()

# Dependency functions
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user dependency"""
    return auth_service.get_current_user(credentials)

def get_current_active_user(current_user = Depends(get_current_user)):
    """Get current active user dependency"""
    if not current_user.get("is_active", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_superuser(current_user = Depends(get_current_user)):
    """Get current superuser dependency"""
    if not current_user.get("is_superuser", False):
        raise HTTPException(
            status_code=400, 
            detail="The user doesn't have enough privileges"
        )
    return current_user 