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
    DATABASE_URL: str = "sqlite:///./database/kali_osint.db"
    DATABASE_TEST_URL: str = "sqlite:///./database/kali_osint_test.db"
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
    
    # Security - All secrets now from environment variables
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    API_KEY: str = os.getenv("API_KEY", "your-api-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "1000"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hour
    
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
    
    # GitHub Scraping
    GITHUB_BASE_URL: str = "https://github.com"
    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_RATE_LIMIT: int = 5000
    
    # Social Media APIs (Optional)
    TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET: Optional[str] = os.getenv("TWITTER_ACCESS_SECRET")
    
    INSTAGRAM_USERNAME: Optional[str] = os.getenv("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD: Optional[str] = os.getenv("INSTAGRAM_PASSWORD")
    
    TELEGRAM_API_ID: Optional[str] = os.getenv("TELEGRAM_API_ID")
    TELEGRAM_API_HASH: Optional[str] = os.getenv("TELEGRAM_API_HASH")
    
    # OSINT Tools
    SHODAN_API_KEY: Optional[str] = os.getenv("SHODAN_API_KEY")
    CENSYS_API_ID: Optional[str] = os.getenv("CENSYS_API_ID")
    CENSYS_API_SECRET: Optional[str] = os.getenv("CENSYS_API_SECRET")
    VIRUSTOTAL_API_KEY: Optional[str] = os.getenv("VIRUSTOTAL_API_KEY")
    ABUSEIPDB_API_KEY: Optional[str] = os.getenv("ABUSEIPDB_API_KEY")
    
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
    MAP_API_KEY: Optional[str] = os.getenv("MAP_API_KEY")
    
    # Dark Web (Optional)
    TOR_ENABLED: bool = False
    TOR_SOCKS_PORT: int = 9050
    TOR_CONTROL_PORT: int = 9051
    
    # Frontend Settings
    REACT_APP_API_URL: str = "http://localhost:8000"
    REACT_APP_WS_URL: str = "ws://localhost:8000/ws"
    REACT_APP_ENVIRONMENT: str = "development"
    
    model_config = {
        "env_file": "config/.env",
        "case_sensitive": True,
        "extra": "ignore"
    }

# Create settings instance
settings = Settings() 