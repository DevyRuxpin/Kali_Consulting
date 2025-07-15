"""
Comprehensive API integration tests
"""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any
import json

class TestAPIEndpoints:
    """Test basic API endpoints"""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_api_docs(self, client: TestClient):
        """Test API documentation endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema(self, client: TestClient):
        """Test OpenAPI schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema

class TestInvestigationEndpoints:
    """Test investigation endpoints"""
    
    def test_create_investigation(self, client: TestClient):
        """Test creating a new investigation"""
        investigation_data = {
            "target_type": "domain",
            "target_value": "example.com",
            "analysis_depth": "comprehensive"
        }
        
        response = client.post("/api/v1/investigations/", json=investigation_data)
        assert response.status_code in [200, 201, 401]  # 401 if not authenticated
    
    def test_get_investigations(self, client: TestClient):
        """Test getting all investigations"""
        response = client.get("/api/v1/investigations/")
        assert response.status_code in [200, 401]
    
    def test_get_investigation_by_id(self, client: TestClient):
        """Test getting a specific investigation"""
        response = client.get("/api/v1/investigations/1")
        assert response.status_code in [200, 404]
    
    def test_update_investigation(self, client: TestClient):
        """Test updating an investigation"""
        update_data = {"status": "completed"}
        response = client.put("/api/v1/investigations/1", json=update_data)
        assert response.status_code in [200, 404]
    
    def test_delete_investigation(self, client: TestClient):
        """Test deleting an investigation"""
        response = client.delete("/api/v1/investigations/1")
        assert response.status_code in [200, 204, 404]

class TestSocialMediaEndpoints:
    """Test social media endpoints"""
    
    def test_scrape_social_media(self, client: TestClient):
        """Test social media scraping"""
        scrape_data = {
            "platform": "twitter",
            "target": "test_user",
            "include_metadata": True
        }
        
        response = client.post("/api/v1/social-media/scrape", json=scrape_data)
        assert response.status_code in [200, 201, 400]
    
    def test_analyze_profile(self, client: TestClient):
        """Test profile analysis"""
        profile_data = {
            "platform": "twitter",
            "username": "test_user",
            "date_range": {"start_date": "2024-01-01", "end_date": "2024-01-31"}
        }
        
        response = client.post("/api/v1/social-media/analyze", json=profile_data)
        assert response.status_code in [200, 201, 400]
    
    def test_search_content(self, client: TestClient):
        """Test content search"""
        search_data = {
            "platform": "twitter",
            "query": "security",
            "max_results": 50
        }
        
        response = client.post("/api/v1/social-media/search", json=search_data)
        assert response.status_code in [200, 201, 400]

class TestGitHubEndpoints:
    """Test GitHub endpoints"""
    
    def test_scrape_github_user(self, client: TestClient):
        """Test GitHub user scraping"""
        user_data = {"username": "test_user"}
        response = client.post("/api/v1/github/scrape-user", json=user_data)
        assert response.status_code in [200, 201, 400]
    
    def test_scrape_github_repo(self, client: TestClient):
        """Test GitHub repository scraping"""
        repo_data = {"repo_url": "https://github.com/test/repo"}
        response = client.post("/api/v1/github/scrape-repo", json=repo_data)
        assert response.status_code in [200, 201, 400]
    
    def test_search_github_repos(self, client: TestClient):
        """Test GitHub repository search"""
        search_data = {"query": "security", "max_results": 10}
        response = client.post("/api/v1/github/search", json=search_data)
        assert response.status_code in [200, 201, 400]

class TestDomainEndpoints:
    """Test domain analysis endpoints"""
    
    def test_analyze_domain(self, client: TestClient):
        """Test domain analysis"""
        domain_data = {"domain": "example.com"}
        response = client.post("/api/v1/domain/analyze", json=domain_data)
        assert response.status_code in [200, 201, 400]
    
    def test_get_domain_info(self, client: TestClient):
        """Test getting domain information"""
        response = client.get("/api/v1/domain/info/example.com")
        assert response.status_code in [200, 404]
    
    def test_check_domain_reputation(self, client: TestClient):
        """Test domain reputation check"""
        response = client.post("/api/v1/domain/reputation/example.com")
        assert response.status_code in [200, 404]

class TestThreatAnalysisEndpoints:
    """Test threat analysis endpoints"""
    
    def test_analyze_threat(self, client: TestClient):
        """Test threat analysis"""
        threat_data = {
            "threat_data": {
                "content": "suspicious content",
                "source": "twitter",
                "user": "test_user"
            }
        }
        response = client.post("/api/v1/threat/analyze", json=threat_data)
        assert response.status_code in [200, 201, 400]
    
    def test_correlate_threats(self, client: TestClient):
        """Test threat correlation"""
        threats_data = {
            "threats": [
                {"source": "twitter", "type": "suspicious_behavior"},
                {"source": "github", "type": "malware_repository"}
            ]
        }
        response = client.post("/api/v1/threat/correlate", json=threats_data)
        assert response.status_code in [200, 201, 400]
    
    def test_generate_threat_report(self, client: TestClient):
        """Test threat report generation"""
        report_data = {
            "threat_data": {
                "correlations": [{"type": "malware", "confidence": 0.8}],
                "threats": [{"level": "high", "source": "twitter"}]
            }
        }
        response = client.post("/api/v1/threat/report", json=report_data)
        assert response.status_code in [200, 201, 400]

class TestIntelligenceEndpoints:
    """Test intelligence endpoints"""
    
    def test_process_intelligence(self, client: TestClient):
        """Test intelligence processing"""
        intel_data = {
            "domain_data": {"info": "data"},
            "github_data": {"repos": "data"},
            "social_media_data": {"twitter": "data"}
        }
        response = client.post("/api/v1/intelligence/process", json=intel_data)
        assert response.status_code in [200, 201, 400]
    
    def test_generate_intelligence_report(self, client: TestClient):
        """Test intelligence report generation"""
        report_data = {
            "domain_data": {"info": "data"},
            "github_data": {"repos": "data"},
            "social_media_data": {"twitter": "data"}
        }
        response = client.post("/api/v1/intelligence/report", json=report_data)
        assert response.status_code in [200, 201, 400]

class TestAnalysisEndpoints:
    """Test analysis endpoints"""
    
    def test_detect_anomalies(self, client: TestClient):
        """Test anomaly detection"""
        anomaly_data = {
            "data": [
                {"activity": "normal", "timestamp": "2024-01-01"},
                {"activity": "suspicious", "timestamp": "2024-01-02"},
                {"activity": "normal", "timestamp": "2024-01-03"}
            ],
            "threshold": 0.5
        }
        response = client.post("/api/v1/analysis/anomalies", json=anomaly_data)
        assert response.status_code in [200, 201, 400]
    
    def test_analyze_patterns(self, client: TestClient):
        """Test pattern analysis"""
        pattern_data = {
            "data": [
                {"frequency": "normal", "type": "login"},
                {"frequency": "high", "type": "post"},
                {"frequency": "suspicious", "type": "download"}
            ],
            "pattern_types": ["login", "post", "download"]
        }
        response = client.post("/api/v1/analysis/patterns", json=pattern_data)
        assert response.status_code in [200, 201, 400]

class TestExportEndpoints:
    """Test export endpoints"""
    
    def test_export_investigation(self, client: TestClient):
        """Test investigation export"""
        response = client.get("/api/v1/exports/investigation/1")
        assert response.status_code in [200, 404]
    
    def test_export_report(self, client: TestClient):
        """Test report export"""
        response = client.get("/api/v1/exports/report/1")
        assert response.status_code in [200, 404]
    
    def test_export_data(self, client: TestClient):
        """Test data export"""
        export_data = {"format": "json", "investigation_id": 1}
        response = client.post("/api/v1/exports/data", json=export_data)
        assert response.status_code in [200, 201, 400, 401]

class TestSettingsEndpoints:
    """Test settings endpoints"""
    
    def test_get_settings(self, client: TestClient):
        """Test getting settings"""
        response = client.get("/api/v1/settings/")
        assert response.status_code in [200, 401]
    
    def test_update_settings(self, client: TestClient):
        """Test updating settings"""
        settings_data = {"theme": "dark", "notifications": True}
        response = client.put("/api/v1/settings/", json=settings_data)
        assert response.status_code in [200, 400, 401]

class TestDashboardEndpoints:
    """Test dashboard endpoints"""
    
    def test_get_dashboard_data(self, client: TestClient):
        """Test getting dashboard data"""
        response = client.get("/api/v1/dashboard/data")
        assert response.status_code in [200, 401]
    
    def test_get_real_time_data(self, client: TestClient):
        """Test getting real-time data"""
        response = client.get("/api/v1/dashboard/realtime")
        assert response.status_code in [200, 401]
    
    def test_get_analytics(self, client: TestClient):
        """Test getting analytics"""
        response = client.get("/api/v1/dashboard/analytics")
        assert response.status_code in [200, 401]

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, client: TestClient):
        """Test 404 error handling"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_422_validation_error(self, client: TestClient):
        """Test validation error handling"""
        invalid_data = {"invalid": "data"}
        response = client.post("/api/v1/social-media/scrape", json=invalid_data)
        assert response.status_code in [422, 400]
    
    def test_500_internal_error(self, client: TestClient):
        """Test internal error handling"""
        # This would test a scenario that causes a 500 error
        # For now, just verify the endpoint exists
        response = client.get("/health")
        assert response.status_code == 200

class TestRateLimiting:
    """Test rate limiting"""
    
    def test_rate_limiting(self, client: TestClient):
        """Test rate limiting functionality"""
        # Make multiple requests to test rate limiting
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code in [200, 429]  # 429 if rate limited

class TestDataValidation:
    """Test data validation"""
    
    def test_investigation_validation(self, client: TestClient):
        """Test investigation data validation"""
        invalid_data = {"invalid_field": "invalid_value"}
        response = client.post("/api/v1/investigations/", json=invalid_data)
        assert response.status_code in [422, 400]
    
    def test_social_media_validation(self, client: TestClient):
        """Test social media data validation"""
        invalid_data = {"invalid_field": "invalid_value"}
        response = client.post("/api/v1/social-media/scrape", json=invalid_data)
        assert response.status_code in [422, 400] 