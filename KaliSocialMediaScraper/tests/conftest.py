"""
Pytest configuration and fixtures for comprehensive testing suite
"""

import pytest
import asyncio
import aiohttp
import tempfile
import os
import sys
from pathlib import Path
from typing import Dict, Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

# Add app to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import engine
from sqlalchemy import create_engine
from app.models.database import Base
from app.services.social_media_scraper import SocialMediaScraper
from app.services.github_scraper import GitHubScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.threat_analyzer import ThreatAnalyzer
from app.services.intelligence_engine import IntelligenceEngine

# Test configuration
pytest_plugins = ["pytest_asyncio"]

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_settings():
    """Test settings configuration"""
    return settings

@pytest.fixture(scope="session")
async def test_database():
    """Test database setup"""
    # Use in-memory SQLite for testing
    database_url = "sqlite:///:memory:"
    
    # Create tables
    test_engine = create_engine(database_url)
    Base.metadata.create_all(bind=test_engine)
    
    yield test_engine
    
    # Cleanup
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
async def mock_session():
    """Mock aiohttp session for testing"""
    session = AsyncMock(spec=aiohttp.ClientSession)
    session.get = AsyncMock()
    session.post = AsyncMock()
    session.put = AsyncMock()
    session.delete = AsyncMock()
    session.close = AsyncMock()
    return session

@pytest.fixture
async def mock_social_media_scraper():
    """Mock social media scraper"""
    scraper = AsyncMock(spec=SocialMediaScraper)
    scraper.scrape_platform = AsyncMock()
    scraper.analyze_profile = AsyncMock()
    scraper.search_content = AsyncMock()
    return scraper

@pytest.fixture
async def mock_github_scraper():
    """Mock GitHub scraper"""
    scraper = AsyncMock(spec=GitHubScraper)
    scraper.scrape_user = AsyncMock()
    scraper.scrape_repository = AsyncMock()
    scraper.search_repositories = AsyncMock()
    return scraper

@pytest.fixture
async def mock_domain_analyzer():
    """Mock domain analyzer"""
    analyzer = AsyncMock(spec=DomainAnalyzer)
    analyzer.analyze_domain = AsyncMock()
    analyzer.get_domain_info = AsyncMock()
    analyzer.check_domain_reputation = AsyncMock()
    return analyzer

@pytest.fixture
async def mock_threat_analyzer():
    """Mock threat analyzer"""
    analyzer = AsyncMock(spec=ThreatAnalyzer)
    analyzer.analyze_threat = AsyncMock()
    analyzer.correlate_threats = AsyncMock()
    analyzer.generate_threat_report = AsyncMock()
    return analyzer

@pytest.fixture
async def mock_intelligence_engine():
    """Mock intelligence engine"""
    engine = AsyncMock(spec=IntelligenceEngine)
    engine.process_intelligence = AsyncMock()
    engine.generate_report = AsyncMock()
    engine.correlate_data = AsyncMock()
    return engine

@pytest.fixture(autouse=True)
def mock_proxy_rotator():
    """Mock proxy rotator for tests"""
    with patch('app.services.social_media_scraper.proxy_rotator') as mock_proxy:
        # Create a proper AsyncMock that returns None
        mock_session = AsyncMock()
        mock_session.return_value = None
        mock_proxy.create_session_with_proxy = mock_session
        yield mock_proxy

@pytest.fixture
def sample_investigation_data():
    """Sample investigation data for testing"""
    return {
        "title": "Test Investigation",
        "description": "Test investigation for comprehensive testing",
        "target": "test-target.com",
        "platforms": ["twitter", "github", "reddit"],
        "priority": "medium",
        "status": "active"
    }

@pytest.fixture
def sample_social_media_data():
    """Sample social media data for testing"""
    return {
        "platform": "twitter",
        "username": "test_user",
        "profile": {
            "username": "test_user",
            "display_name": "Test User",
            "bio": "Test bio",
            "followers_count": 1000,
            "following_count": 500,
            "posts_count": 100,
            "verified": False
        },
        "posts": [
            {
                "id": "post_1",
                "content": "Test post content",
                "posted_at": "2024-01-01T00:00:00Z",
                "likes_count": 10,
                "retweets_count": 5,
                "replies_count": 3
            }
        ]
    }

@pytest.fixture
def sample_github_data():
    """Sample GitHub data for testing"""
    return {
        "username": "test_user",
        "profile": {
            "login": "test_user",
            "name": "Test User",
            "bio": "Test bio",
            "followers": 100,
            "following": 50,
            "public_repos": 25
        },
        "repositories": [
            {
                "id": 1,
                "name": "test-repo",
                "description": "Test repository",
                "language": "Python",
                "stars": 10,
                "forks": 5
            }
        ]
    }

@pytest.fixture
def sample_threat_data():
    """Sample threat data for testing"""
    return {
        "threat_level": "medium",
        "threat_score": 45,
        "threat_indicators": [
            "Suspicious activity detected",
            "Multiple failed login attempts"
        ],
        "correlated_threats": [
            {
                "source": "twitter",
                "threat_type": "suspicious_behavior",
                "confidence": 0.8
            }
        ]
    }

@pytest.fixture
def temp_test_dir():
    """Temporary directory for test files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture(scope="session")
def client():
    """FastAPI test client for integration tests"""
    with TestClient(app) as c:
        yield c

# Coverage configuration
def pytest_configure(config):
    """Configure pytest for comprehensive testing"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security tests"
    )

# Test collection configuration
def pytest_collection_modifyitems(config, items):
    """Modify test collection for better organization"""
    for item in items:
        # Add default markers based on test name
        if "test_api" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_service" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "test_e2e" in item.nodeid:
            item.add_marker(pytest.mark.e2e)
        elif "test_performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        elif "test_security" in item.nodeid:
            item.add_marker(pytest.mark.security) 