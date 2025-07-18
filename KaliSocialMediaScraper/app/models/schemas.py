"""
Pydantic schemas for OSINT investigation platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from enum import Enum

def utc_now() -> datetime:
    """Get current UTC time with timezone info"""
    return datetime.now(timezone.utc)

class InvestigationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TargetType(str, Enum):
    DOMAIN = "domain"
    EMAIL = "email"
    USERNAME = "username"
    PHONE = "phone"
    IP_ADDRESS = "ip_address"
    ORGANIZATION = "organization"
    PERSON = "person"
    REPOSITORY = "repository"
    GITHUB_REPOSITORY = "github_repository"
    SOCIAL_MEDIA = "social_media"

class AnalysisDepth(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    DEEP = "deep"
    COMPREHENSIVE = "comprehensive"

class ThreatLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PlatformType(str, Enum):
    GITHUB = "github"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    REDDIT = "reddit"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"

# Request Models
class InvestigationRequest(BaseModel):
    target_type: TargetType = Field(..., description="Type of investigation target")
    target_value: str = Field(..., description="Target value (domain, email, username, etc.)")
    analysis_depth: AnalysisDepth = Field(AnalysisDepth.STANDARD, description="Analysis depth level")
    platforms: List[PlatformType] = Field(default_factory=list, description="Platforms to investigate")
    include_network_analysis: bool = Field(True, description="Include network analysis")
    include_timeline_analysis: bool = Field(True, description="Include timeline analysis")
    include_threat_assessment: bool = Field(True, description="Include threat assessment")
    analysis_options: Dict[str, Any] = Field(default_factory=dict, description="Additional analysis options")
    search_timeframe: str = Field("all", description="Search timeframe (all, last_24h, last_7d, last_30d, last_90d, last_year, custom)")
    date_range_start: Optional[str] = Field(None, description="Start date for custom date range (YYYY-MM-DD)")
    date_range_end: Optional[str] = Field(None, description="End date for custom date range (YYYY-MM-DD)")

class SocialMediaScrapingRequest(BaseModel):
    platform: PlatformType = Field(..., description="Social media platform")
    target: str = Field(..., description="Target account or hashtag")
    include_metadata: bool = Field(True, description="Include metadata analysis")
    include_media: bool = Field(False, description="Include media analysis")
    max_posts: int = Field(100, description="Maximum number of posts to scrape")

class DomainAnalysisRequest(BaseModel):
    domain: str = Field(..., description="Domain to analyze")
    include_subdomains: bool = Field(True, description="Include subdomain enumeration")
    include_dns: bool = Field(True, description="Include DNS analysis")
    include_whois: bool = Field(True, description="Include WHOIS data")
    include_ssl: bool = Field(True, description="Include SSL certificate analysis")

class AnalyzeProfileRequest(BaseModel):
    platform: PlatformType
    username: str
    date_range: Optional[Dict[str, str]] = None

class SearchContentRequest(BaseModel):
    platform: PlatformType
    query: str
    max_results: int = 50

# Response Models
class InvestigationResult(BaseModel):
    status: InvestigationStatus = Field(..., description="Investigation status")
    message: str = Field(..., description="Status message")
    task_id: str = Field(..., description="Task identifier")
    progress: Optional[int] = Field(None, description="Progress percentage")
    created_at: datetime = Field(default_factory=utc_now, description="Creation timestamp")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")

class InvestigationResponse(BaseModel):
    id: int = Field(..., description="Investigation ID")
    title: str = Field(..., description="Investigation title")
    description: Optional[str] = Field(None, description="Investigation description")
    target_type: str = Field(..., description="Target type")
    target_value: str = Field(..., description="Target value")
    status: str = Field(..., description="Investigation status")
    progress: int = Field(..., description="Progress percentage")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

class AnalysisResult(BaseModel):
    status: str = Field(..., description="Analysis status")
    message: str = Field(..., description="Status message")
    task_id: str = Field(..., description="Task identifier")
    created_at: datetime = Field(default_factory=utc_now, description="Creation timestamp")

class ThreatAssessment(BaseModel):
    target: str = Field(..., description="Target identifier")
    threat_level: ThreatLevel = Field(..., description="Overall threat level")
    threat_score: float = Field(..., description="Threat score (0-1)")
    indicators: List[str] = Field(default_factory=list, description="Threat indicators")
    risk_factors: List[str] = Field(default_factory=list, description="Risk factors")
    recommendations: List[str] = Field(default_factory=list, description="Security recommendations")
    confidence: float = Field(..., description="Assessment confidence (0-1)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Assessment timestamp")

# Network Analysis Models
class NetworkNode(BaseModel):
    id: str = Field(..., description="Node identifier")
    label: str = Field(..., description="Node label")
    type: str = Field(..., description="Node type")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Node properties")
    threat_level: Optional[ThreatLevel] = Field(None, description="Node threat level")
    confidence: float = Field(1.0, description="Node confidence score")

class NetworkEdge(BaseModel):
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    type: str = Field(..., description="Edge type")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Edge properties")
    strength: float = Field(1.0, description="Relationship strength")

class NetworkGraph(BaseModel):
    nodes: List[NetworkNode] = Field(default_factory=list, description="Network nodes")
    edges: List[NetworkEdge] = Field(default_factory=list, description="Network edges")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Graph metadata")
    communities: List[List[str]] = Field(default_factory=list, description="Detected communities")

# Timeline Analysis Models
class TimelineEvent(BaseModel):
    timestamp: datetime = Field(..., description="Event timestamp")
    event_type: str = Field(..., description="Event type")
    description: str = Field(..., description="Event description")
    source: str = Field(..., description="Event source")
    platform: Optional[PlatformType] = Field(None, description="Platform where event occurred")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Event properties")
    threat_level: Optional[ThreatLevel] = Field(None, description="Event threat level")

class TimelineData(BaseModel):
    events: List[TimelineEvent] = Field(default_factory=list, description="Timeline events")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Timeline metadata")
    patterns: List[str] = Field(default_factory=list, description="Detected patterns")
    anomalies: List[str] = Field(default_factory=list, description="Detected anomalies")

# Social Media Models
class SocialMediaPost(BaseModel):
    id: str = Field(..., description="Post identifier")
    platform: PlatformType = Field(..., description="Platform")
    author: str = Field(..., description="Author username")
    content: str = Field(..., description="Post content")
    timestamp: datetime = Field(..., description="Post timestamp")
    engagement: Dict[str, int] = Field(default_factory=dict, description="Engagement metrics")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Post metadata")
    threat_indicators: List[str] = Field(default_factory=list, description="Threat indicators")

class SocialMediaProfile(BaseModel):
    username: str = Field(..., description="Profile username")
    platform: PlatformType = Field(..., description="Platform")
    display_name: Optional[str] = Field(None, description="Display name")
    bio: Optional[str] = Field(None, description="Profile bio")
    followers: int = Field(0, description="Number of followers")
    following: int = Field(0, description="Number of following")
    posts: List[SocialMediaPost] = Field(default_factory=list, description="Recent posts")
    threat_assessment: Optional[ThreatAssessment] = Field(None, description="Threat assessment")

# Domain Intelligence Models
class DomainInfo(BaseModel):
    domain: str = Field(..., description="Domain name")
    ip_addresses: List[str] = Field(default_factory=list, description="IP addresses")
    subdomains: List[str] = Field(default_factory=list, description="Subdomains")
    dns_records: Dict[str, List[str]] = Field(default_factory=dict, description="DNS records")
    whois_data: Dict[str, Any] = Field(default_factory=dict, description="WHOIS data")
    ssl_certificate: Dict[str, Any] = Field(default_factory=dict, description="SSL certificate")
    technologies: List[str] = Field(default_factory=list, description="Detected technologies")
    threat_indicators: List[str] = Field(default_factory=list, description="Threat indicators")

class EmailIntelligence(BaseModel):
    email: str = Field(..., description="Email address")
    domain: str = Field(..., description="Email domain")
    breach_exposure: List[str] = Field(default_factory=list, description="Data breach exposures")
    social_media_accounts: List[str] = Field(default_factory=list, description="Linked social media")
    threat_assessment: Optional[ThreatAssessment] = Field(None, description="Threat assessment")

# Technology Stack Models
class TechnologyStack(BaseModel):
    languages: List[str] = Field(default_factory=list, description="Programming languages")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks and libraries")
    tools: List[str] = Field(default_factory=list, description="Development tools")
    databases: List[str] = Field(default_factory=list, description="Databases")
    platforms: List[str] = Field(default_factory=list, description="Platforms")
    services: List[str] = Field(default_factory=list, description="Cloud services")

class RepositoryData(BaseModel):
    name: str = Field(..., description="Repository name")
    description: Optional[str] = Field(None, description="Repository description")
    language: Optional[str] = Field(None, description="Primary language")
    stars: int = Field(0, description="Number of stars")
    forks: int = Field(0, description="Number of forks")
    contributors: List[str] = Field(default_factory=list, description="Contributor usernames")
    technologies: TechnologyStack = Field(default_factory=TechnologyStack, description="Technology stack")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")
    threat_indicators: List[str] = Field(default_factory=list, description="Threat indicators")

# User Profile Models
class UserProfile(BaseModel):
    username: str = Field(..., description="Username")
    display_name: Optional[str] = Field(None, description="Display name")
    bio: Optional[str] = Field(None, description="User bio")
    location: Optional[str] = Field(None, description="Location")
    company: Optional[str] = Field(None, description="Company")
    website: Optional[str] = Field(None, description="Website")
    repositories: List[RepositoryData] = Field(default_factory=list, description="User repositories")
    organizations: List[str] = Field(default_factory=list, description="Organization memberships")
    followers: int = Field(0, description="Number of followers")
    following: int = Field(0, description="Number of following")
    created_at: datetime = Field(..., description="Account creation date")
    threat_assessment: Optional[ThreatAssessment] = Field(None, description="Threat assessment")

class OrganizationData(BaseModel):
    name: str = Field(..., description="Organization name")
    description: Optional[str] = Field(None, description="Organization description")
    website: Optional[str] = Field(None, description="Organization website")
    location: Optional[str] = Field(None, description="Organization location")
    members: List[str] = Field(default_factory=list, description="Member usernames")
    repositories: List[RepositoryData] = Field(default_factory=list, description="Organization repositories")
    public_repos: int = Field(0, description="Number of public repositories")
    created_at: datetime = Field(..., description="Organization creation date")
    threat_assessment: Optional[ThreatAssessment] = Field(None, description="Threat assessment")

# Investigation Report Models
class InvestigationReport(BaseModel):
    investigation_id: str = Field(..., description="Investigation identifier")
    target: str = Field(..., description="Investigation target")
    target_type: TargetType = Field(..., description="Target type")
    status: InvestigationStatus = Field(..., description="Investigation status")
    created_at: datetime = Field(..., description="Creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    findings: Dict[str, Any] = Field(default_factory=dict, description="Investigation findings")
    threat_assessment: Optional[ThreatAssessment] = Field(None, description="Threat assessment")
    network_graph: Optional[NetworkGraph] = Field(None, description="Network analysis")
    timeline: Optional[TimelineData] = Field(None, description="Timeline analysis")
    recommendations: List[str] = Field(default_factory=list, description="Security recommendations")

# Intelligence Engine Models
class Entity(BaseModel):
    id: str = Field(..., description="Entity identifier")
    type: str = Field(..., description="Entity type")
    platform: Optional[PlatformType] = Field(None, description="Platform")
    username: Optional[str] = Field(None, description="Username")
    display_name: Optional[str] = Field(None, description="Display name")
    bio: Optional[str] = Field(None, description="Bio")
    followers_count: Optional[int] = Field(None, description="Followers count")
    following_count: Optional[int] = Field(None, description="Following count")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    verified: Optional[bool] = Field(None, description="Verification status")
    location: Optional[str] = Field(None, description="Location")
    content: Optional[str] = Field(None, description="Content")
    posted_at: Optional[datetime] = Field(None, description="Post timestamp")
    likes_count: Optional[int] = Field(None, description="Likes count")
    comments_count: Optional[int] = Field(None, description="Comments count")
    shares_count: Optional[int] = Field(None, description="Shares count")
    hashtags: Optional[List[str]] = Field(None, description="Hashtags")
    mentions: Optional[List[str]] = Field(None, description="Mentions")
    urls: Optional[List[str]] = Field(None, description="URLs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Entity metadata")

class Relationship(BaseModel):
    source_id: str = Field(..., description="Source entity ID")
    target_id: str = Field(..., description="Target entity ID")
    type: str = Field(..., description="Relationship type")
    strength: float = Field(1.0, description="Relationship strength")
    platform: Optional[PlatformType] = Field(None, description="Platform")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Relationship metadata")

class Pattern(BaseModel):
    id: str = Field(..., description="Pattern identifier")
    type: str = Field(..., description="Pattern type")
    description: str = Field(..., description="Pattern description")
    entities: List[str] = Field(default_factory=list, description="Involved entities")
    confidence: float = Field(1.0, description="Pattern confidence")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Pattern metadata")

class Anomaly(BaseModel):
    id: str = Field(..., description="Anomaly identifier")
    type: str = Field(..., description="Anomaly type")
    description: str = Field(..., description="Anomaly description")
    entities: List[str] = Field(default_factory=list, description="Involved entities")
    severity: ThreatLevel = Field(ThreatLevel.MEDIUM, description="Anomaly severity")
    confidence: float = Field(1.0, description="Anomaly confidence")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Anomaly metadata")

class IntelligenceReport(BaseModel):
    investigation_id: str = Field(..., description="Investigation identifier")
    report_type: str = Field(..., description="Report type")
    title: str = Field(..., description="Report title")
    executive_summary: str = Field(..., description="Executive summary")
    key_findings: List[str] = Field(default_factory=list, description="Key findings")
    threat_assessment: Dict[str, Any] = Field(default_factory=dict, description="Threat assessment")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    technical_details: Dict[str, Any] = Field(default_factory=dict, description="Technical details")
    confidence_score: float = Field(..., description="Confidence score")
    generated_at: datetime = Field(..., description="Generation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Report metadata")

# Investigation Model (for backward compatibility)
class Investigation(BaseModel):
    id: str = Field(..., description="Investigation identifier")
    target: str = Field(..., description="Investigation target")
    target_type: TargetType = Field(..., description="Target type")
    status: InvestigationStatus = Field(..., description="Investigation status")
    created_at: datetime = Field(..., description="Creation timestamp")
    social_media_data: List[Dict[str, Any]] = Field(default_factory=list, description="Social media data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Investigation metadata")

# Authentication Schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)

class User(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, description="Full name")
    is_active: bool = Field(True, description="Active status")
    is_superuser: bool = Field(False, description="Superuser status")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str = Field(..., description="Access token")
    token_type: str = Field(..., description="Token type")
    user: User = Field(..., description="User information")

class TokenData(BaseModel):
    username: Optional[str] = Field(None, description="Username from token")

# GitHub API Models
class GitHubUserRequest(BaseModel):
    username: str = Field(..., description="GitHub username to scrape")

class GitHubRepoRequest(BaseModel):
    repo_url: str = Field(..., description="GitHub repository URL")

class GitHubSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(50, description="Maximum number of results")

# Threat Analysis Models
class ThreatAnalysisRequest(BaseModel):
    threat_data: Dict[str, Any] = Field(..., description="Threat data to analyze")

class ThreatCorrelationRequest(BaseModel):
    threats: List[Dict[str, Any]] = Field(..., description="List of threats to correlate")

# Analysis Request Models
class AnalysisRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Data to analyze")
    analysis_type: str = Field("comprehensive", description="Type of analysis to perform")

class AnomalyDetectionRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Data for anomaly detection")
    threshold: float = Field(0.5, description="Anomaly detection threshold")

class PatternAnalysisRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Data for pattern analysis")
    pattern_types: List[str] = Field(default_factory=list, description="Types of patterns to detect")

# Intelligence Request Models
class IntelligenceRequest(BaseModel):
    domain_data: Optional[Dict[str, Any]] = Field(None, description="Domain analysis data")
    github_data: Optional[Dict[str, Any]] = Field(None, description="GitHub analysis data")
    social_media_data: Optional[Dict[str, Any]] = Field(None, description="Social media analysis data") 