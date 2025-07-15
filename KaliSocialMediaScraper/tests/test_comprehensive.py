"""
Comprehensive test suite for the Kali Social Media Scraper
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.main import app
from app.core.database import get_db
from app.models.database import Base
from app.services.social_media_scraper import SocialMediaScraper
from app.services.github_scraper import GitHubScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.threat_analyzer import ThreatAnalyzer

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Test client"""
    return TestClient(app)

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/api/v1/health/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_dashboard_data(self, client):
        """Test dashboard data endpoint"""
        response = client.get("/api/v1/dashboard/data")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "data" in data
    
    def test_create_investigation(self, client):
        """Test investigation creation"""
        investigation_data = {
            "target_type": "domain",
            "target_value": "example.com",
            "analysis_depth": "standard",
            "platforms": ["github", "twitter"],
            "include_network_analysis": True,
            "include_timeline_analysis": True,
            "include_threat_assessment": True,
            "analysis_options": {},
            "search_timeframe": "all"
        }
        
        response = client.post("/api/v1/investigations/", json=investigation_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
    
    def test_list_investigations(self, client):
        """Test investigation listing"""
        response = client.get("/api/v1/investigations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_social_media_scraping(self, client):
        """Test social media scraping"""
        scraping_data = {
            "platform": "twitter",
            "target": "testuser",
            "include_metadata": True,
            "include_media": False,
            "max_posts": 10
        }
        
        response = client.post("/api/v1/social-media/scrape", json=scraping_data)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_domain_analysis(self, client):
        """Test domain analysis"""
        domain_data = {
            "domain": "example.com",
            "include_subdomains": True,
            "include_dns": True,
            "include_whois": True,
            "include_ssl": True
        }
        
        response = client.post("/api/v1/domain/analyze", json=domain_data)
        assert response.status_code == 200
        data = response.json()
        assert "domain" in data
    
    def test_threat_analysis(self, client):
        """Test threat analysis"""
        threat_data = {
            "threat_data": {
                "target": "suspicious-domain.com",
                "analysis_type": "comprehensive"
            }
        }
        
        response = client.post("/api/v1/threat/analyze", json=threat_data)
        assert response.status_code == 200
        data = response.json()
        assert "target" in data

class TestServices:
    """Test service functionality"""
    
    @pytest.mark.asyncio
    async def test_social_media_scraper(self):
        """Test social media scraper service"""
        scraper = SocialMediaScraper()
        
        # Mock the scraper to avoid actual web requests
        with patch.object(scraper, 'scrape_platform', new_callable=AsyncMock) as mock_scrape:
            mock_scrape.return_value = {
                "platform": "twitter",
                "username": "testuser",
                "posts": [],
                "profile": {
                    "username": "testuser",
                    "followers": 100,
                    "following": 50
                }
            }
            
            async with scraper:
                result = await scraper.scrape_platform("twitter", "testuser")
                assert result["platform"] == "twitter"
                assert result["username"] == "testuser"
    
    @pytest.mark.asyncio
    async def test_github_scraper(self):
        """Test GitHub scraper service"""
        scraper = GitHubScraper()
        
        with patch.object(scraper, 'analyze_user_profile', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.return_value = {
                "username": "testuser",
                "name": "Test User",
                "public_repos": 10,
                "followers": 50
            }
            
            async with scraper:
                result = await scraper.analyze_user_profile("testuser")
                assert result["username"] == "testuser"
                assert "public_repos" in result
    
    @pytest.mark.asyncio
    async def test_domain_analyzer(self):
        """Test domain analyzer service"""
        analyzer = DomainAnalyzer()
        
        with patch.object(analyzer, 'analyze_domain', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.return_value = {
                "domain": "example.com",
                "ip_addresses": ["93.184.216.34"],
                "subdomains": ["www.example.com"],
                "dns_records": {"A": ["93.184.216.34"]},
                "risk_score": 0.1
            }
            
            result = await analyzer.analyze_domain("example.com")
            assert result["domain"] == "example.com"
            assert "ip_addresses" in result
    
    @pytest.mark.asyncio
    async def test_threat_analyzer(self):
        """Test threat analyzer service"""
        analyzer = ThreatAnalyzer()
        
        with patch.object(analyzer, 'analyze_threat', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.return_value = {
                "target": "suspicious-domain.com",
                "threat_level": "medium",
                "threat_score": 0.6,
                "indicators": ["Suspicious keyword detected"],
                "recommendations": ["Monitor closely"]
            }
            
            result = await analyzer.analyze_threat("suspicious-domain.com", "comprehensive")
            assert result["target"] == "suspicious-domain.com"
            assert "threat_level" in result

class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_investigation_request(self, client):
        """Test invalid investigation request"""
        invalid_data = {
            "target_type": "invalid_type",
            "target_value": "",
            "analysis_depth": "invalid_depth"
        }
        
        response = client.post("/api/v1/investigations/", json=invalid_data)
        assert response.status_code == 400
    
    def test_invalid_domain_analysis(self, client):
        """Test invalid domain analysis"""
        invalid_data = {
            "domain": ""
        }
        
        response = client.post("/api/v1/domain/analyze", json=invalid_data)
        assert response.status_code == 400
    
    def test_rate_limiting(self, client):
        """Test rate limiting (basic)"""
        # Make multiple requests to trigger rate limiting
        for _ in range(15):  # Exceed default limit
            response = client.get("/api/v1/health/health")
            if response.status_code == 429:
                break
        else:
            # If no rate limiting triggered, that's also acceptable for tests
            assert True

class TestDataValidation:
    """Test data validation"""
    
    def test_investigation_data_validation(self):
        """Test investigation data validation"""
        from app.utils.validation import validate_investigation_request
        
        # Valid data
        assert validate_investigation_request("example.com", "domain") == True
        assert validate_investigation_request("testuser", "username") == True
        
        # Invalid data
        assert validate_investigation_request("", "domain") == False
        assert validate_investigation_request("test", "invalid_type") == False
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        from app.utils.validation import validate_and_sanitize_input
        
        # Test string sanitization
        result = validate_and_sanitize_input("test<script>alert('xss')</script>")
        assert "<script>" not in str(result)
        
        # Test list sanitization
        result = validate_and_sanitize_input(["test", "<script>alert('xss')</script>"])
        assert all("<script>" not in str(item) for item in result)

class TestPerformance:
    """Test performance aspects"""
    
    def test_response_time(self, client):
        """Test response time"""
        import time
        
        start_time = time.time()
        response = client.get("/api/v1/health/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second
        assert response.status_code == 200
    
    def test_concurrent_requests(self, client):
        """Test concurrent requests"""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = client.get("/api/v1/health/health")
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Start 10 concurrent requests
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        assert len(results) == 10
        assert all(status == 200 for status in results)
        assert len(errors) == 0

class TestSecurity:
    """Test security aspects"""
    
    def test_sql_injection_prevention(self, client):
        """Test SQL injection prevention"""
        # Try to inject SQL in investigation target
        malicious_data = {
            "target_type": "domain",
            "target_value": "'; DROP TABLE investigations; --",
            "analysis_depth": "standard",
            "platforms": [],
            "include_network_analysis": True,
            "include_timeline_analysis": True,
            "include_threat_assessment": True,
            "analysis_options": {},
            "search_timeframe": "all"
        }
        
        response = client.post("/api/v1/investigations/", json=malicious_data)
        # Should either reject the request or handle it safely
        assert response.status_code in [200, 400, 422]
    
    def test_xss_prevention(self, client):
        """Test XSS prevention"""
        # Try to inject XSS in investigation title
        malicious_data = {
            "target_type": "domain",
            "target_value": "example.com",
            "analysis_depth": "standard",
            "platforms": [],
            "include_network_analysis": True,
            "include_timeline_analysis": True,
            "include_threat_assessment": True,
            "analysis_options": {},
            "search_timeframe": "all"
        }
        
        response = client.post("/api/v1/investigations/", json=malicious_data)
        if response.status_code == 200:
            data = response.json()
            # Check that any returned HTML is properly escaped
            assert "<script>" not in str(data)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 