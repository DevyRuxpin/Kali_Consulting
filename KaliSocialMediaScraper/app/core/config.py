"""
Configuration settings for Kali OSINT Investigation Platform
"""

from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Any
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Kali OSINT Investigation Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/kali_osint"
    DATABASE_TEST_URL: str = "postgresql://kali_user:kali_pass@localhost:5432/kali_osint_test"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_DB: str = "0"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Kali OSINT Platform"
    BACKEND_CORS_ORIGINS: str = '["http://localhost:3000", "http://localhost:8000"]'
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Celery Settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: str = "json"
    CELERY_TIMEZONE: str = "UTC"
    CELERY_ENABLE_UTC: str = "True"
    
    # Scraping Settings
    SCRAPING_DELAY: float = 1.0
    MAX_CONCURRENT_REQUESTS: int = 16
    USER_AGENT_ROTATION: bool = True
    REQUEST_TIMEOUT: int = 30
    PROXY_ROTATION: bool = True
    SCRAPING_TIMEOUT: str = "30"
    MAX_CONCURRENT_SCRAPERS: str = "5"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: str = "true"
    RATE_LIMIT_REQUESTS: str = "100"
    RATE_LIMIT_WINDOW: str = "3600"
    
    # GitHub Scraping
    GITHUB_BASE_URL: str = "https://github.com"
    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_RATE_LIMIT: int = 5000
    
    # Social Media APIs (Optional)
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_SECRET: Optional[str] = None
    
    INSTAGRAM_USERNAME: Optional[str] = None
    INSTAGRAM_PASSWORD: Optional[str] = None
    
    TELEGRAM_API_ID: Optional[str] = None
    TELEGRAM_API_HASH: Optional[str] = None
    
    # OSINT Tools
    SHODAN_API_KEY: Optional[str] = None
    CENSYS_API_ID: Optional[str] = None
    CENSYS_API_SECRET: Optional[str] = None
    VIRUSTOTAL_API_KEY: Optional[str] = None
    ABUSEIPDB_API_KEY: Optional[str] = None
    
    # Network Analysis
    WHOIS_SERVER: str = "whois.iana.org"
    DNS_SERVERS: str = "8.8.8.8,1.1.1.1"
    SSL_VERIFY: str = "true"
    
    # Analysis Settings
    MAX_ANALYSIS_DEPTH: int = 3
    NETWORK_GRAPH_MAX_NODES: int = 1000
    TIMELINE_MAX_EVENTS: int = 10000
    THREAT_SCORE_THRESHOLD: float = 0.7
    THREAT_INTELLIGENCE_ENABLED: str = "true"
    ANOMALY_DETECTION_ENABLED: str = "true"
    
    # Machine Learning
    ML_MODEL_PATH: str = "models/"
    SENTIMENT_ANALYSIS_ENABLED: bool = True
    FACE_RECOGNITION_ENABLED: bool = True
    THREAT_CLASSIFICATION_ENABLED: bool = True
    
    # File Storage
    UPLOAD_DIR: str = "uploads/"
    EXPORT_DIR: str = "exports/"
    CACHE_DIR: str = "cache/"
    EXPORT_PATH: str = "./exports"
    REPORT_TEMPLATE_PATH: str = "./templates/reports"
    REPORT_FORMATS: str = "pdf,html,json"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    LOG_MAX_SIZE: str = "10MB"
    LOG_BACKUP_COUNT: str = "5"
    
    # Investigation Settings
    MAX_INVESTIGATION_DURATION: int = 24 * 60 * 60  # 24 hours in seconds
    AUTO_ARCHIVE_DAYS: int = 30
    MAX_CONCURRENT_INVESTIGATIONS: int = 10
    
    # Health Check & Metrics
    HEALTH_CHECK_ENABLED: str = "true"
    METRICS_ENABLED: str = "true"
    PROMETHEUS_ENABLED: str = "false"
    
    # Geolocation
    GEOLOCATION_ENABLED: bool = True
    MAP_API_KEY: Optional[str] = None
    
    # Dark Web (Optional)
    TOR_ENABLED: bool = False
    TOR_SOCKS_PORT: int = 9050
    TOR_CONTROL_PORT: int = 9051
    
    # Frontend Settings
    REACT_APP_API_URL: str = "http://localhost:8000"
    REACT_APP_WS_URL: str = "ws://localhost:8000/ws"
    REACT_APP_ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings() 