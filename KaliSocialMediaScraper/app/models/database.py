"""
SQLAlchemy database models for Kali OSINT Investigation Platform
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON, ForeignKey, Table, Index, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()

# Association tables for many-to-many relationships
investigation_platforms = Table(
    'investigation_platforms',
    Base.metadata,
    Column('investigation_id', Integer, ForeignKey('investigations.id', ondelete='CASCADE'), primary_key=True),
    Column('platform_id', Integer, ForeignKey('platforms.id', ondelete='CASCADE'), primary_key=True)
)

investigation_tags = Table(
    'investigation_tags',
    Base.metadata,
    Column('investigation_id', Integer, ForeignKey('investigations.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class User(Base):
    """User model for authentication and access control"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    investigations = relationship("Investigation", back_populates="created_by", cascade="all, delete-orphan")
    reports = relationship("InvestigationReport", back_populates="created_by", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_email', 'email'),
        Index('idx_users_active', 'is_active'),
        Index('idx_users_created_at', 'created_at'),
    )

class Investigation(Base):
    """Main investigation model"""
    __tablename__ = "investigations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    target_type = Column(String(50), nullable=False, index=True)  # domain, email, username, etc.
    target_value = Column(String(500), nullable=False, index=True)
    status = Column(String(20), default="pending", index=True)  # pending, running, completed, failed
    priority = Column(String(20), default="medium", index=True)  # low, medium, high, critical
    analysis_depth = Column(String(20), default="standard", index=True)  # basic, standard, deep, comprehensive
    
    # Analysis options
    include_network_analysis = Column(Boolean, default=True)
    include_timeline_analysis = Column(Boolean, default=True)
    include_threat_assessment = Column(Boolean, default=True)
    analysis_options = Column(JSON, default=dict)
    
    # Progress tracking
    progress = Column(Integer, default=0, index=True)  # 0-100
    current_step = Column(String(100))
    estimated_completion = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    started_at = Column(DateTime(timezone=True), index=True)
    completed_at = Column(DateTime(timezone=True), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    
    # Foreign keys
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    created_by = relationship("User", back_populates="investigations")
    platforms = relationship("Platform", secondary=investigation_platforms, back_populates="investigations")
    tags = relationship("Tag", secondary=investigation_tags, back_populates="investigations")
    findings = relationship("InvestigationFinding", back_populates="investigation", cascade="all, delete-orphan")
    reports = relationship("InvestigationReport", back_populates="investigation", cascade="all, delete-orphan")
    social_media_data = relationship("SocialMediaData", back_populates="investigation", cascade="all, delete-orphan")
    domain_data = relationship("DomainData", back_populates="investigation", cascade="all, delete-orphan")
    network_data = relationship("NetworkData", back_populates="investigation", cascade="all, delete-orphan")
    github_data = Column(JSON, default=list)
    
    # Indexes
    __table_args__ = (
        Index('idx_investigations_target_type', 'target_type'),
        Index('idx_investigations_target_value', 'target_value'),
        Index('idx_investigations_status', 'status'),
        Index('idx_investigations_priority', 'priority'),
        Index('idx_investigations_progress', 'progress'),
        Index('idx_investigations_created_at', 'created_at'),
        Index('idx_investigations_updated_at', 'updated_at'),
        Index('idx_investigations_created_by', 'created_by_id'),
        UniqueConstraint('target_type', 'target_value', name='uq_investigation_target'),
    )

class Platform(Base):
    """Platform model for social media and data sources"""
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)  # github, twitter, instagram, etc.
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    api_available = Column(Boolean, default=False, index=True)
    scraping_enabled = Column(Boolean, default=True, index=True)
    rate_limit = Column(Integer)  # requests per hour
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    investigations = relationship("Investigation", secondary=investigation_platforms, back_populates="platforms")
    social_media_data = relationship("SocialMediaData", back_populates="platform", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_platforms_name', 'name'),
        Index('idx_platforms_active', 'is_active'),
        Index('idx_platforms_api_available', 'api_available'),
        Index('idx_platforms_scraping_enabled', 'scraping_enabled'),
    )

class Tag(Base):
    """Tag model for categorizing investigations"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(7))  # hex color code
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    investigations = relationship("Investigation", secondary=investigation_tags, back_populates="tags")
    
    # Indexes
    __table_args__ = (
        Index('idx_tags_name', 'name'),
        Index('idx_tags_created_at', 'created_at'),
    )

class InvestigationFinding(Base):
    """Individual findings within an investigation"""
    __tablename__ = "investigations_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    finding_type = Column(String(50), nullable=False, index=True)  # threat, network, timeline, etc.
    title = Column(String(200), nullable=False)
    description = Column(Text)
    severity = Column(String(20), default="low", index=True)  # low, medium, high, critical
    confidence = Column(Float, default=0.0, index=True)  # 0.0-1.0
    data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    investigation = relationship("Investigation", back_populates="findings")
    
    # Indexes
    __table_args__ = (
        Index('idx_findings_investigation_id', 'investigation_id'),
        Index('idx_findings_type', 'finding_type'),
        Index('idx_findings_severity', 'severity'),
        Index('idx_findings_confidence', 'confidence'),
        Index('idx_findings_created_at', 'created_at'),
    )

class InvestigationReport(Base):
    """Investigation reports and exports"""
    __tablename__ = "investigation_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    report_type = Column(String(50), nullable=False, index=True)  # pdf, csv, json, html
    title = Column(String(200), nullable=False)
    description = Column(Text)
    file_path = Column(String(500))
    file_size = Column(Integer)  # bytes
    status = Column(String(20), default="pending", index=True)  # pending, generating, completed, failed
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True), index=True)
    
    # Relationships
    investigation = relationship("Investigation", back_populates="reports")
    created_by = relationship("User", back_populates="reports")
    
    # Indexes
    __table_args__ = (
        Index('idx_reports_investigation_id', 'investigation_id'),
        Index('idx_reports_type', 'report_type'),
        Index('idx_reports_status', 'status'),
        Index('idx_reports_created_at', 'created_at'),
        Index('idx_reports_created_by', 'created_by_id'),
    )

class SocialMediaData(Base):
    """Social media data collected during investigations"""
    __tablename__ = "social_media_data"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete="CASCADE"), nullable=False, index=True)
    username = Column(String(100), nullable=False, index=True)
    display_name = Column(String(200))
    bio = Column(Text)
    followers_count = Column(Integer, default=0, index=True)
    following_count = Column(Integer, default=0, index=True)
    posts_count = Column(Integer, default=0, index=True)
    profile_url = Column(String(500))
    is_verified = Column(Boolean, default=False, index=True)
    is_private = Column(Boolean, default=False, index=True)
    threat_score = Column(Float, default=0.0, index=True)
    threat_indicators = Column(JSON, default=list)
    sentiment_score = Column(Float, default=0.0, index=True)
    collected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    investigation = relationship("Investigation", back_populates="social_media_data")
    platform = relationship("Platform", back_populates="social_media_data")
    posts = relationship("SocialMediaPost", back_populates="profile", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_social_media_investigation_id', 'investigation_id'),
        Index('idx_social_media_platform_id', 'platform_id'),
        Index('idx_social_media_username', 'username'),
        Index('idx_social_media_threat_score', 'threat_score'),
        Index('idx_social_media_sentiment_score', 'sentiment_score'),
        Index('idx_social_media_collected_at', 'collected_at'),
        UniqueConstraint('investigation_id', 'platform_id', 'username', name='uq_social_media_profile'),
    )

class SocialMediaPost(Base):
    """Individual social media posts"""
    __tablename__ = "social_media_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("social_media_data.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(String(100), nullable=False, index=True)  # Original platform post ID
    content = Column(Text)
    post_url = Column(String(500))
    posted_at = Column(DateTime(timezone=True), index=True)
    likes_count = Column(Integer, default=0, index=True)
    shares_count = Column(Integer, default=0, index=True)
    comments_count = Column(Integer, default=0, index=True)
    threat_score = Column(Float, default=0.0, index=True)
    sentiment_score = Column(Float, default=0.0, index=True)
    collected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    profile = relationship("SocialMediaData", back_populates="posts")
    
    # Indexes
    __table_args__ = (
        Index('idx_posts_profile_id', 'profile_id'),
        Index('idx_posts_post_id', 'post_id'),
        Index('idx_posts_posted_at', 'posted_at'),
        Index('idx_posts_threat_score', 'threat_score'),
        Index('idx_posts_sentiment_score', 'sentiment_score'),
        Index('idx_posts_collected_at', 'collected_at'),
        UniqueConstraint('profile_id', 'post_id', name='uq_social_media_post'),
    )

class DomainData(Base):
    """Domain intelligence data"""
    __tablename__ = "domain_data"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    domain = Column(String(255), nullable=False, index=True)
    ip_addresses = Column(JSON, default=list)
    subdomains = Column(JSON, default=list)
    dns_records = Column(JSON, default=dict)
    whois_data = Column(JSON, default=dict)
    ssl_certificate = Column(JSON, default=dict)
    technologies = Column(JSON, default=list)
    threat_indicators = Column(JSON, default=list)
    threat_score = Column(Float, default=0.0, index=True)
    collected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    investigation = relationship("Investigation", back_populates="domain_data")
    
    # Indexes
    __table_args__ = (
        Index('idx_domain_data_investigation_id', 'investigation_id'),
        Index('idx_domain_data_domain', 'domain'),
        Index('idx_domain_data_threat_score', 'threat_score'),
        Index('idx_domain_data_collected_at', 'collected_at'),
        UniqueConstraint('investigation_id', 'domain', name='uq_domain_data'),
    )

class NetworkData(Base):
    """Network analysis data"""
    __tablename__ = "network_data"
    
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    nodes = Column(JSON, default=list)
    edges = Column(JSON, default=list)
    communities = Column(JSON, default=list)
    centrality_scores = Column(JSON, default=dict)
    threat_hotspots = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    investigation = relationship("Investigation", back_populates="network_data")
    
    # Indexes
    __table_args__ = (
        Index('idx_network_data_investigation_id', 'investigation_id'),
        Index('idx_network_data_created_at', 'created_at'),
        UniqueConstraint('investigation_id', name='uq_network_data'),
    )

class TaskQueue(Base):
    """Background task queue management"""
    __tablename__ = "task_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(100), unique=True, nullable=False, index=True)
    task_type = Column(String(50), nullable=False, index=True)  # investigation, scraping, analysis, export
    status = Column(String(20), default="pending", index=True)  # pending, running, completed, failed
    priority = Column(Integer, default=0, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=True, index=True)
    parameters = Column(JSON, default=dict)
    result = Column(JSON, default=dict)
    error_message = Column(Text)
    progress = Column(Integer, default=0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    started_at = Column(DateTime(timezone=True), index=True)
    completed_at = Column(DateTime(timezone=True), index=True)
    
    # Relationships
    investigation = relationship("Investigation")
    
    # Indexes
    __table_args__ = (
        Index('idx_task_queue_task_id', 'task_id'),
        Index('idx_task_queue_task_type', 'task_type'),
        Index('idx_task_queue_status', 'status'),
        Index('idx_task_queue_priority', 'priority'),
        Index('idx_task_queue_investigation_id', 'investigation_id'),
        Index('idx_task_queue_progress', 'progress'),
        Index('idx_task_queue_created_at', 'created_at'),
    )

class SystemLog(Base):
    """System activity logging"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False, index=True)  # info, warning, error, critical
    module = Column(String(100), nullable=False, index=True)
    message = Column(Text, nullable=False)
    details = Column(JSON, default=dict)
    investigation_id = Column(Integer, ForeignKey("investigations.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    investigation = relationship("Investigation")
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_system_logs_level', 'level'),
        Index('idx_system_logs_module', 'module'),
        Index('idx_system_logs_investigation_id', 'investigation_id'),
        Index('idx_system_logs_user_id', 'user_id'),
        Index('idx_system_logs_created_at', 'created_at'),
    ) 