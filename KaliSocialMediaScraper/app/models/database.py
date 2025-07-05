"""
SQLAlchemy database models for Kali OSINT Investigation Platform
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()

# Association tables for many-to-many relationships
investigation_platforms = Table(
    'investigation_platforms',
    Base.metadata,
    Column('investigation_id', Integer, ForeignKey('investigations.id'), primary_key=True),
    Column('platform_id', Integer, ForeignKey('platforms.id'), primary_key=True)
)

investigation_tags = Table(
    'investigation_tags',
    Base.metadata,
    Column('investigation_id', Integer, ForeignKey('investigations.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class User(Base):
    """User model for authentication and access control"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    investigations = relationship("Investigation", back_populates="created_by")
    reports = relationship("InvestigationReport", back_populates="created_by")

class Investigation(Base):
    """Main investigation model"""
    __tablename__ = "investigations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    target_type = Column(String(50), nullable=False)  # domain, email, username, etc.
    target_value = Column(String(500), nullable=False)
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    analysis_depth = Column(String(20), default="standard")  # basic, standard, deep, comprehensive
    
    # Analysis options
    include_network_analysis = Column(Boolean, default=True)
    include_timeline_analysis = Column(Boolean, default=True)
    include_threat_assessment = Column(Boolean, default=True)
    analysis_options = Column(JSON, default=dict)
    
    # Progress tracking
    progress = Column(Integer, default=0)  # 0-100
    current_step = Column(String(100))
    estimated_completion = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User", back_populates="investigations")
    platforms = relationship("Platform", secondary=investigation_platforms, back_populates="investigations")
    tags = relationship("Tag", secondary=investigation_tags, back_populates="investigations")
    findings = relationship("InvestigationFinding", back_populates="investigation")
    reports = relationship("InvestigationReport", back_populates="investigation")
    social_media_data = relationship("SocialMediaData", back_populates="investigation")
    domain_data = relationship("DomainData", back_populates="investigation")
    network_data = relationship("NetworkData", back_populates="investigation")

class Platform(Base):
    """Platform model for social media and data sources"""
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # github, twitter, instagram, etc.
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    api_available = Column(Boolean, default=False)
    scraping_enabled = Column(Boolean, default=True)
    rate_limit = Column(Integer)  # requests per hour
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigations = relationship("Investigation", secondary=investigation_platforms, back_populates="platforms")
    social_media_data = relationship("SocialMediaData", back_populates="platform")

class Tag(Base):
    """Tag model for categorizing investigations"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(7))  # hex color code
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigations = relationship("Investigation", secondary=investigation_tags, back_populates="tags")

class InvestigationFinding(Base):
    """Individual findings within an investigation"""
    __tablename__ = "investigations_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    finding_type = Column(String(50), nullable=False)  # threat, network, timeline, etc.
    title = Column(String(200), nullable=False)
    description = Column(Text)
    severity = Column(String(20), default="low")  # low, medium, high, critical
    confidence = Column(Float, default=0.0)  # 0.0-1.0
    data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigation = relationship("Investigation", back_populates="findings")

class InvestigationReport(Base):
    """Investigation reports and exports"""
    __tablename__ = "investigation_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    report_type = Column(String(50), nullable=False)  # pdf, csv, json, html
    title = Column(String(200), nullable=False)
    description = Column(Text)
    file_path = Column(String(500))
    file_size = Column(Integer)  # bytes
    status = Column(String(20), default="pending")  # pending, generating, completed, failed
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    investigation = relationship("Investigation", back_populates="reports")
    created_by = relationship("User", back_populates="reports")

class SocialMediaData(Base):
    """Social media data collected during investigations"""
    __tablename__ = "social_media_data"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    username = Column(String(100), nullable=False)
    display_name = Column(String(200))
    bio = Column(Text)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    profile_url = Column(String(500))
    is_verified = Column(Boolean, default=False)
    is_private = Column(Boolean, default=False)
    threat_score = Column(Float, default=0.0)
    threat_indicators = Column(JSON, default=list)
    sentiment_score = Column(Float, default=0.0)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigation = relationship("Investigation", back_populates="social_media_data")
    platform = relationship("Platform", back_populates="social_media_data")
    posts = relationship("SocialMediaPost", back_populates="profile")

class SocialMediaPost(Base):
    """Individual social media posts"""
    __tablename__ = "social_media_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("social_media_data.id"), nullable=False)
    post_id = Column(String(100), nullable=False)  # Original platform post ID
    content = Column(Text)
    post_url = Column(String(500))
    posted_at = Column(DateTime(timezone=True))
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    threat_score = Column(Float, default=0.0)
    sentiment_score = Column(Float, default=0.0)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile = relationship("SocialMediaData", back_populates="posts")

class DomainData(Base):
    """Domain intelligence data"""
    __tablename__ = "domain_data"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    domain = Column(String(255), nullable=False)
    ip_addresses = Column(JSON, default=list)
    subdomains = Column(JSON, default=list)
    dns_records = Column(JSON, default=dict)
    whois_data = Column(JSON, default=dict)
    ssl_certificate = Column(JSON, default=dict)
    technologies = Column(JSON, default=list)
    threat_indicators = Column(JSON, default=list)
    threat_score = Column(Float, default=0.0)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigation = relationship("Investigation", back_populates="domain_data")

class NetworkData(Base):
    """Network analysis data"""
    __tablename__ = "network_data"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    nodes = Column(JSON, default=list)
    edges = Column(JSON, default=list)
    communities = Column(JSON, default=list)
    centrality_scores = Column(JSON, default=dict)
    threat_hotspots = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigation = relationship("Investigation", back_populates="network_data")

class TaskQueue(Base):
    """Background task queue management"""
    __tablename__ = "task_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(100), unique=True, nullable=False)
    task_type = Column(String(50), nullable=False)  # investigation, scraping, analysis, export
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    priority = Column(Integer, default=0)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    parameters = Column(JSON, default=dict)
    result = Column(JSON, default=dict)
    error_message = Column(Text)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    investigation = relationship("Investigation")

class SystemLog(Base):
    """System activity logging"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # info, warning, error, critical
    module = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, default=dict)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigation = relationship("Investigation")
    user = relationship("User") 