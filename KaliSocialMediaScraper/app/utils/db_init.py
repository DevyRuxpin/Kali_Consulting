"""
Database initialization utilities
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.models.database import Platform, Tag, User
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def init_platforms(db: Session):
    """Initialize default platforms"""
    platforms = [
        {
            "name": "github",
            "display_name": "GitHub",
            "description": "Git repository hosting platform",
            "is_active": True,
            "api_available": True,
            "scraping_enabled": True,
            "rate_limit": 5000
        },
        {
            "name": "twitter",
            "display_name": "Twitter",
            "description": "Social media platform",
            "is_active": True,
            "api_available": False,
            "scraping_enabled": True,
            "rate_limit": 300
        },
        {
            "name": "instagram",
            "display_name": "Instagram",
            "description": "Photo and video sharing platform",
            "is_active": True,
            "api_available": False,
            "scraping_enabled": True,
            "rate_limit": 200
        },
        {
            "name": "telegram",
            "display_name": "Telegram",
            "description": "Messaging platform",
            "is_active": True,
            "api_available": True,
            "scraping_enabled": True,
            "rate_limit": 1000
        },
        {
            "name": "discord",
            "display_name": "Discord",
            "description": "Communication platform",
            "is_active": True,
            "api_available": True,
            "scraping_enabled": True,
            "rate_limit": 500
        },
        {
            "name": "reddit",
            "display_name": "Reddit",
            "description": "Social news and discussion platform",
            "is_active": True,
            "api_available": True,
            "scraping_enabled": True,
            "rate_limit": 1000
        }
    ]
    
    for platform_data in platforms:
        existing = db.query(Platform).filter(Platform.name == platform_data["name"]).first()
        if not existing:
            platform = Platform(**platform_data)
            db.add(platform)
            logger.info(f"Created platform: {platform_data['name']}")
    
    db.commit()

def init_tags(db: Session):
    """Initialize default tags"""
    tags = [
        {
            "name": "threat-intelligence",
            "color": "#ff4444",
            "description": "Threat intelligence investigations"
        },
        {
            "name": "social-media",
            "color": "#4444ff",
            "description": "Social media analysis"
        },
        {
            "name": "domain-analysis",
            "color": "#44ff44",
            "description": "Domain intelligence gathering"
        },
        {
            "name": "network-analysis",
            "color": "#ff8844",
            "description": "Network relationship analysis"
        },
        {
            "name": "timeline-analysis",
            "color": "#8844ff",
            "description": "Temporal pattern analysis"
        },
        {
            "name": "high-priority",
            "color": "#ff0000",
            "description": "High priority investigations"
        },
        {
            "name": "completed",
            "color": "#00ff00",
            "description": "Completed investigations"
        }
    ]
    
    for tag_data in tags:
        existing = db.query(Tag).filter(Tag.name == tag_data["name"]).first()
        if not existing:
            tag = Tag(**tag_data)
            db.add(tag)
            logger.info(f"Created tag: {tag_data['name']}")
    
    db.commit()

def init_admin_user(db: Session):
    """Initialize admin user"""
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Check if admin user exists
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@kali-osint.com",
            hashed_password=pwd_context.hash("admin123"),  # Change in production
            full_name="System Administrator",
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        logger.info("Created admin user")
    else:
        logger.info("Admin user already exists")

def init_database():
    """Initialize database with default data"""
    try:
        # Create tables
        create_tables()
        logger.info("Database tables created")
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Initialize default data
            init_platforms(db)
            init_tags(db)
            init_admin_user(db)
            
            logger.info("Database initialization completed successfully")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    init_database() 