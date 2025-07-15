"""
Type hints and type definitions for Kali OSINT Investigation Platform
"""

from typing import (
    Dict, List, Optional, Union, Any, Tuple, Callable, 
    Generator, AsyncGenerator, TypeVar, Protocol, Literal
)
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Request, Response

# Type variables for generic functions
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# Common type aliases
JSON = Dict[str, Any]
JSONList = List[JSON]
Headers = Dict[str, str]
QueryParams = Dict[str, Union[str, int, float, bool]]

# Database types
DB = Session
DBResult = Union[T, None]

# API types
APIResponse = Union[JSON, BaseModel]
APIError = Dict[str, str]

# Investigation types
class InvestigationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class InvestigationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AnalysisDepth(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    DEEP = "deep"

class TargetType(str, Enum):
    DOMAIN = "domain"
    IP = "ip"
    EMAIL = "email"
    USERNAME = "username"
    PHONE = "phone"
    PERSON = "person"
    ORGANIZATION = "organization"

# Social media types
class PlatformType(str, Enum):
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    GITHUB = "github"
    REDDIT = "reddit"
    TELEGRAM = "telegram"
    DISCORD = "discord"

# Threat analysis types
class ThreatLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatCategory(str, Enum):
    MALWARE = "malware"
    PHISHING = "phishing"
    SCAM = "scam"
    HACKING = "hacking"
    TERRORISM = "terrorism"
    EXTREMISM = "extremism"
    CYBERCRIME = "cybercrime"
    OTHER = "other"

# Network analysis types
class NodeType(str, Enum):
    DOMAIN = "domain"
    IP = "ip"
    EMAIL = "email"
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"

class EdgeType(str, Enum):
    OWNS = "owns"
    CONTROLS = "controls"
    CONNECTS_TO = "connects_to"
    COMMUNICATES_WITH = "communicates_with"
    LOCATED_AT = "located_at"
    WORKS_FOR = "works_for"

# Data collection types
class DataSource(str, Enum):
    WHOIS = "whois"
    DNS = "dns"
    SSL = "ssl"
    SOCIAL_MEDIA = "social_media"
    DARK_WEB = "dark_web"
    PUBLIC_RECORDS = "public_records"
    NEWS = "news"
    FORUMS = "forums"

# Validation types
ValidationResult = Tuple[bool, Optional[str]]

# Service types
class ServiceProtocol(Protocol):
    """Protocol for service classes"""
    async def initialize(self) -> None: ...
    async def cleanup(self) -> None: ...

class ScraperProtocol(Protocol):
    """Protocol for scraper classes"""
    async def scrape(self, target: str, options: Dict[str, Any]) -> JSON: ...
    async def validate_target(self, target: str) -> ValidationResult: ...

# Middleware types
class MiddlewareProtocol(Protocol):
    """Protocol for middleware classes"""
    async def process_request(self, request: Request) -> Request: ...
    async def process_response(self, response: Response) -> Response: ...

# Repository types
class RepositoryProtocol(Protocol[T]):
    """Protocol for repository classes"""
    async def create(self, data: Dict[str, Any]) -> T: ...
    async def get_by_id(self, id: int) -> Optional[T]: ...
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[T]: ...
    async def update(self, id: int, data: Dict[str, Any]) -> Optional[T]: ...
    async def delete(self, id: int) -> bool: ...

# Task types
class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

TaskResult = Tuple[bool, Optional[str], Optional[JSON]]

# Cache types
class CacheKey(str):
    """Type for cache keys"""
    pass

CacheValue = Union[str, bytes, JSON]

# Logging types
class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

LogContext = Dict[str, Any]

# Configuration types
class ConfigSection(str, Enum):
    DATABASE = "database"
    SECURITY = "security"
    SCRAPING = "scraping"
    ANALYSIS = "analysis"
    CACHE = "cache"
    LOGGING = "logging"

# Export types
class ExportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"
    HTML = "html"
    XML = "xml"

ExportOptions = Dict[str, Any]

# Rate limiting types
RateLimitConfig = Tuple[int, int]
RateLimitInfo = Tuple[int, int, int]

# Authentication types
class AuthMethod(str, Enum):
    API_KEY = "api_key"
    JWT = "jwt"
    OAUTH = "oauth"
    BASIC = "basic"

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

# Report types
class ReportFormat(str, Enum):
    SUMMARY = "summary"
    DETAILED = "detailed"
    EXECUTIVE = "executive"
    TECHNICAL = "technical"

class ReportSection(str, Enum):
    EXECUTIVE_SUMMARY = "executive_summary"
    METHODOLOGY = "methodology"
    FINDINGS = "findings"
    THREAT_ASSESSMENT = "threat_assessment"
    RECOMMENDATIONS = "recommendations"
    APPENDIX = "appendix"

# Utility type functions
def is_valid_json(data: Any) -> bool:
    """Type guard to check if data is valid JSON"""
    return isinstance(data, (dict, list, str, int, float, bool)) or data is None

def is_valid_dict(data: Any) -> bool:
    """Type guard to check if data is a valid dictionary"""
    return isinstance(data, dict)

def is_valid_list(data: Any) -> bool:
    """Type guard to check if data is a valid list"""
    return isinstance(data, list)

def is_valid_string(data: Any) -> bool:
    """Type guard to check if data is a valid string"""
    return isinstance(data, str)

def is_valid_integer(data: Any) -> bool:
    """Type guard to check if data is a valid integer"""
    return isinstance(data, int)

def is_valid_float(data: Any) -> bool:
    """Type guard to check if data is a valid float"""
    return isinstance(data, (int, float))

def is_valid_boolean(data: Any) -> bool:
    """Type guard to check if data is a valid boolean"""
    return isinstance(data, bool)

def is_valid_datetime(data: Any) -> bool:
    """Type guard to check if data is a valid datetime"""
    return isinstance(data, datetime)

def is_valid_timedelta(data: Any) -> bool:
    """Type guard to check if data is a valid timedelta"""
    return isinstance(data, timedelta)

# Type conversion utilities
def to_json(data: Any) -> JSON:
    """Convert data to JSON-compatible format"""
    if isinstance(data, dict):
        return {str(k): to_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_json(item) for item in data]
    elif isinstance(data, (datetime, timedelta)):
        return str(data)
    elif isinstance(data, Enum):
        return data.value
    else:
        return data

def from_json(data: JSON, target_type: type) -> Any:
    """Convert JSON data to target type"""
    if target_type == dict:
        return data
    elif target_type == list:
        return list(data.values()) if isinstance(data, dict) else data
    elif target_type == str:
        return str(data)
    elif target_type == int:
        return int(str(data))
    elif target_type == float:
        return float(str(data))
    elif target_type == bool:
        return bool(data)
    else:
        return data

# Type checking utilities
def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
    """Validate that all required fields are present"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, None

def validate_field_types(data: Dict[str, Any], field_types: Dict[str, type]) -> ValidationResult:
    """Validate field types"""
    for field, expected_type in field_types.items():
        if field in data:
            if not isinstance(data[field], expected_type):
                return False, f"Field '{field}' must be of type {expected_type.__name__}"
    return True, None

def validate_enum_values(data: Dict[str, Any], enum_fields: Dict[str, type]) -> ValidationResult:
    """Validate enum field values"""
    for field, enum_class in enum_fields.items():
        if field in data:
            try:
                # Check if the value is valid for the enum
                valid_values = [e.value for e in enum_class]
                if data[field] not in valid_values:
                    return False, f"Field '{field}' must be one of: {', '.join(valid_values)}"
            except (AttributeError, TypeError):
                return False, f"Invalid enum class for field '{field}'"
    return True, None 