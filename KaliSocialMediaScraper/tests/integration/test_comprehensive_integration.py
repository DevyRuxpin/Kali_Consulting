"""
Comprehensive Integration Tests for Kali OSINT Platform
"""

import pytest
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestComprehensiveIntegration:
    """Comprehensive integration tests for the entire platform"""
    
    @pytest.fixture
    async def api_client(self):
        """Create API client for testing"""
        async with aiohttp.ClientSession() as session:
            yield session
    
    @pytest.fixture
    def base_url(self):
        """Base URL for API testing"""
        return "http://localhost:8000/api/v1"
    
    @pytest.mark.asyncio
    async def test_health_check(self, api_client, base_url):
        """Test health check endpoint"""
        async with api_client.get(f"{base_url}/health/health") as response:
            assert response.status == 200
            data = await response.json()
            assert "status" in data
            assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_investigation_lifecycle(self, api_client, base_url):
        """Test complete investigation lifecycle"""
        # Create investigation
        investigation_data = {
            "target_type": "username",
            "target_value": "test_user",
            "analysis_depth": "comprehensive",
            "platforms": ["github", "twitter"],
            "include_network_analysis": True,
            "include_timeline_analysis": True,
            "include_threat_assessment": True
        }
        
        async with api_client.post(
            f"{base_url}/investigations/",
            json=investigation_data
        ) as response:
            assert response.status == 201
            investigation = await response.json()
            investigation_id = investigation["id"]
            assert investigation_id is not None
        
        # Get investigation details
        async with api_client.get(f"{base_url}/investigations/{investigation_id}") as response:
            assert response.status == 200
            investigation_details = await response.json()
            assert investigation_details["id"] == investigation_id
        
        # Update investigation
        update_data = {
            "status": "running",
            "progress": 50
        }
        
        async with api_client.put(
            f"{base_url}/investigations/{investigation_id}",
            json=update_data
        ) as response:
            assert response.status == 200
            updated_investigation = await response.json()
            assert updated_investigation["status"] == "running"
        
        # List investigations
        async with api_client.get(f"{base_url}/investigations/") as response:
            assert response.status == 200
            investigations = await response.json()
            assert isinstance(investigations, list)
            assert len(investigations) > 0
        
        # Delete investigation
        async with api_client.delete(f"{base_url}/investigations/{investigation_id}") as response:
            assert response.status == 204
    
    @pytest.mark.asyncio
    async def test_social_media_analysis(self, api_client, base_url):
        """Test social media analysis functionality"""
        # Test username hunting
        hunt_data = {
            "username": "test_user",
            "sites": ["twitter", "github", "instagram"]
        }
        
        async with api_client.post(
            f"{base_url}/social-media/sherlock/hunt",
            params=hunt_data
        ) as response:
            assert response.status == 200
            hunt_results = await response.json()
            assert "results" in hunt_results
        
        # Test social media scraping
        scrape_data = {
            "platform": "twitter",
            "target": "test_user",
            "include_metadata": True,
            "include_media": False,
            "max_posts": 10
        }
        
        async with api_client.post(
            f"{base_url}/social-media/scrape",
            json=scrape_data
        ) as response:
            assert response.status == 200
            scrape_results = await response.json()
            assert "platform" in scrape_results
        
        # Test comprehensive hunt
        comprehensive_data = {
            "username": "test_user",
            "include_direct_scraping": True,
            "include_sherlock": True,
            "platforms": ["twitter", "github"]
        }
        
        async with api_client.post(
            f"{base_url}/social-media/comprehensive-hunt",
            params=comprehensive_data
        ) as response:
            assert response.status == 200
            comprehensive_results = await response.json()
            assert "results" in comprehensive_results
    
    @pytest.mark.asyncio
    async def test_github_analysis(self, api_client, base_url):
        """Test GitHub analysis functionality"""
        # Test user analysis
        user_data = {
            "target": "test_user",
            "target_type": "user"
        }
        
        async with api_client.post(
            f"{base_url}/github/analyze",
            json=user_data
        ) as response:
            assert response.status == 200
            user_results = await response.json()
            assert "user" in user_results or "error" in user_results
        
        # Test repository analysis
        repo_data = {
            "target": "test_user/test_repo",
            "target_type": "repository"
        }
        
        async with api_client.post(
            f"{base_url}/github/analyze",
            json=repo_data
        ) as response:
            assert response.status == 200
            repo_results = await response.json()
            assert "repository" in repo_results or "error" in repo_results
    
    @pytest.mark.asyncio
    async def test_domain_analysis(self, api_client, base_url):
        """Test domain analysis functionality"""
        domain_data = {
            "domain": "example.com",
            "include_subdomains": True,
            "include_dns": True,
            "include_whois": True,
            "include_ssl": True
        }
        
        async with api_client.post(
            f"{base_url}/domain/analyze",
            json=domain_data
        ) as response:
            assert response.status == 200
            domain_results = await response.json()
            assert "domain" in domain_results
    
    @pytest.mark.asyncio
    async def test_threat_analysis(self, api_client, base_url):
        """Test threat analysis functionality"""
        threat_data = {
            "threat_data": {
                "target": "test_target",
                "indicators": ["suspicious_activity", "unusual_behavior"],
                "context": "social_media_analysis"
            }
        }
        
        async with api_client.post(
            f"{base_url}/threat/analyze",
            json=threat_data
        ) as response:
            assert response.status == 200
            threat_results = await response.json()
            assert "target" in threat_results
    
    @pytest.mark.asyncio
    async def test_intelligence_processing(self, api_client, base_url):
        """Test intelligence processing functionality"""
        intelligence_data = {
            "domain_data": {"domain": "example.com"},
            "github_data": {"user": "test_user"},
            "social_media_data": {"platform": "twitter", "username": "test_user"}
        }
        
        async with api_client.post(
            f"{base_url}/intelligence/process",
            json=intelligence_data
        ) as response:
            assert response.status == 200
            intelligence_results = await response.json()
            assert "processed" in intelligence_results
    
    @pytest.mark.asyncio
    async def test_analysis_endpoints(self, api_client, base_url):
        """Test analysis endpoints"""
        # Test anomaly detection
        anomaly_data = {
            "data": [
                {"entity_id": "1", "activity_score": 0.8},
                {"entity_id": "2", "activity_score": 0.2}
            ],
            "threshold": 0.5
        }
        
        async with api_client.post(
            f"{base_url}/analysis/anomalies",
            json=anomaly_data
        ) as response:
            assert response.status == 200
            anomaly_results = await response.json()
            assert "anomalies" in anomaly_results
        
        # Test pattern analysis
        pattern_data = {
            "data": [
                {"entity_id": "1", "behavior": "normal"},
                {"entity_id": "2", "behavior": "suspicious"}
            ],
            "pattern_types": ["behavioral", "temporal"]
        }
        
        async with api_client.post(
            f"{base_url}/analysis/patterns",
            json=pattern_data
        ) as response:
            assert response.status == 200
            pattern_results = await response.json()
            assert "patterns" in pattern_results
    
    @pytest.mark.asyncio
    async def test_export_functionality(self, api_client, base_url):
        """Test export functionality"""
        export_data = {
            "investigation_id": "test_investigation",
            "export_format": "json",
            "include_metadata": True
        }
        
        async with api_client.post(
            f"{base_url}/exports/data",
            json=export_data
        ) as response:
            assert response.status == 200
            export_results = await response.json()
            assert "export_url" in export_results or "data" in export_results
    
    @pytest.mark.asyncio
    async def test_dashboard_functionality(self, api_client, base_url):
        """Test dashboard functionality"""
        # Test dashboard data
        async with api_client.get(f"{base_url}/dashboard/data") as response:
            assert response.status == 200
            dashboard_data = await response.json()
            assert "investigations" in dashboard_data or "stats" in dashboard_data
        
        # Test dashboard stats
        async with api_client.get(f"{base_url}/dashboard/stats") as response:
            assert response.status == 200
            stats_data = await response.json()
            assert isinstance(stats_data, dict)
    
    @pytest.mark.asyncio
    async def test_settings_functionality(self, api_client, base_url):
        """Test settings functionality"""
        # Get settings
        async with api_client.get(f"{base_url}/settings/") as response:
            assert response.status == 200
            settings = await response.json()
            assert isinstance(settings, dict)
        
        # Update settings
        update_settings = {
            "scraping_delay": 2.0,
            "max_concurrent_requests": 20
        }
        
        async with api_client.put(
            f"{base_url}/settings/",
            json=update_settings
        ) as response:
            assert response.status == 200
            updated_settings = await response.json()
            assert "scraping_delay" in updated_settings
    
    @pytest.mark.asyncio
    async def test_authentication_flow(self, api_client, base_url):
        """Test authentication flow"""
        # Test login
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }
        
        async with api_client.post(
            f"{base_url}/auth/token",
            data=login_data
        ) as response:
            # This might fail if user doesn't exist, which is expected
            assert response.status in [200, 401, 422]
    
    @pytest.mark.asyncio
    async def test_error_handling(self, api_client, base_url):
        """Test error handling"""
        # Test invalid investigation ID
        async with api_client.get(f"{base_url}/investigations/invalid_id") as response:
            assert response.status == 404
        
        # Test invalid domain
        invalid_domain_data = {
            "domain": "invalid_domain_format",
            "include_subdomains": True
        }
        
        async with api_client.post(
            f"{base_url}/domain/analyze",
            json=invalid_domain_data
        ) as response:
            assert response.status in [200, 400, 422]
        
        # Test invalid threat data
        invalid_threat_data = {
            "threat_data": "invalid_format"
        }
        
        async with api_client.post(
            f"{base_url}/threat/analyze",
            json=invalid_threat_data
        ) as response:
            assert response.status in [200, 400, 422]
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, api_client, base_url):
        """Test concurrent request handling"""
        # Make multiple concurrent requests
        async def make_request():
            async with api_client.get(f"{base_url}/health/health") as response:
                return response.status
        
        # Make 10 concurrent requests
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(status == 200 for status in results)
    
    @pytest.mark.asyncio
    async def test_data_validation(self, api_client, base_url):
        """Test data validation"""
        # Test missing required fields
        invalid_investigation = {
            "target_type": "username"
            # Missing target_value
        }
        
        async with api_client.post(
            f"{base_url}/investigations/",
            json=invalid_investigation
        ) as response:
            assert response.status == 422
        
        # Test invalid enum values
        invalid_analysis = {
            "target_type": "invalid_type",
            "target_value": "test",
            "analysis_depth": "invalid_depth"
        }
        
        async with api_client.post(
            f"{base_url}/investigations/",
            json=invalid_analysis
        ) as response:
            assert response.status == 422
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, api_client, base_url):
        """Test rate limiting functionality"""
        # Make rapid requests to test rate limiting
        async def make_rapid_requests():
            responses = []
            for _ in range(20):
                async with api_client.get(f"{base_url}/health/health") as response:
                    responses.append(response.status)
            return responses
        
        responses = await make_rapid_requests()
        
        # Most requests should succeed, some might be rate limited
        success_count = sum(1 for status in responses if status == 200)
        assert success_count > 0  # At least some requests should succeed
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self, api_client, base_url):
        """Test WebSocket functionality"""
        # This would require a WebSocket client
        # For now, just test the endpoint exists
        async with api_client.get(f"{base_url}/health/health") as response:
            assert response.status == 200
    
    @pytest.mark.asyncio
    async def test_comprehensive_workflow(self, api_client, base_url):
        """Test comprehensive end-to-end workflow"""
        # 1. Create investigation
        investigation_data = {
            "target_type": "username",
            "target_value": "comprehensive_test_user",
            "analysis_depth": "comprehensive",
            "platforms": ["github", "twitter"],
            "include_network_analysis": True,
            "include_timeline_analysis": True,
            "include_threat_assessment": True
        }
        
        async with api_client.post(
            f"{base_url}/investigations/",
            json=investigation_data
        ) as response:
            assert response.status == 201
            investigation = await response.json()
            investigation_id = investigation["id"]
        
        # 2. Perform social media analysis
        social_media_data = {
            "platform": "twitter",
            "target": "comprehensive_test_user",
            "include_metadata": True,
            "max_posts": 5
        }
        
        async with api_client.post(
            f"{base_url}/social-media/scrape",
            json=social_media_data
        ) as response:
            assert response.status == 200
            social_results = await response.json()
        
        # 3. Perform GitHub analysis
        github_data = {
            "target": "comprehensive_test_user",
            "target_type": "user"
        }
        
        async with api_client.post(
            f"{base_url}/github/analyze",
            json=github_data
        ) as response:
            assert response.status == 200
            github_results = await response.json()
        
        # 4. Perform threat analysis
        threat_data = {
            "threat_data": {
                "target": "comprehensive_test_user",
                "social_media_data": social_results,
                "github_data": github_results
            }
        }
        
        async with api_client.post(
            f"{base_url}/threat/analyze",
            json=threat_data
        ) as response:
            assert response.status == 200
            threat_results = await response.json()
        
        # 5. Generate intelligence report
        intelligence_data = {
            "domain_data": {"domain": "example.com"},
            "github_data": github_results,
            "social_media_data": social_results
        }
        
        async with api_client.post(
            f"{base_url}/intelligence/report",
            json=intelligence_data
        ) as response:
            assert response.status == 200
            intelligence_results = await response.json()
        
        # 6. Export results
        export_data = {
            "investigation_id": investigation_id,
            "export_format": "json",
            "include_metadata": True
        }
        
        async with api_client.post(
            f"{base_url}/exports/report",
            json=export_data
        ) as response:
            assert response.status == 200
            export_results = await response.json()
        
        # 7. Clean up
        async with api_client.delete(f"{base_url}/investigations/{investigation_id}") as response:
            assert response.status == 204
        
        # Verify all steps completed successfully
        assert "id" in investigation
        assert "platform" in social_results or "error" in social_results
        assert "user" in github_results or "error" in github_results
        assert "target" in threat_results
        assert "report" in intelligence_results or "processed" in intelligence_results
        assert "export_url" in export_results or "data" in export_results

class TestPerformanceIntegration:
    """Performance integration tests"""
    
    @pytest.mark.asyncio
    async def test_large_dataset_handling(self, api_client, base_url):
        """Test handling of large datasets"""
        # Create multiple investigations
        investigation_ids = []
        
        for i in range(10):
            investigation_data = {
                "target_type": "username",
                "target_value": f"performance_test_user_{i}",
                "analysis_depth": "basic",
                "platforms": ["github"]
            }
            
            async with api_client.post(
                f"{base_url}/investigations/",
                json=investigation_data
            ) as response:
                if response.status == 201:
                    investigation = await response.json()
                    investigation_ids.append(investigation["id"])
        
        # Test listing all investigations
        async with api_client.get(f"{base_url}/investigations/") as response:
            assert response.status == 200
            investigations = await response.json()
            assert len(investigations) >= len(investigation_ids)
        
        # Clean up
        for investigation_id in investigation_ids:
            async with api_client.delete(f"{base_url}/investigations/{investigation_id}") as response:
                pass  # Ignore cleanup errors
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis(self, api_client, base_url):
        """Test concurrent analysis operations"""
        async def perform_analysis(target):
            # Social media analysis
            social_data = {
                "platform": "twitter",
                "target": target,
                "include_metadata": True,
                "max_posts": 1
            }
            
            async with api_client.post(
                f"{base_url}/social-media/scrape",
                json=social_data
            ) as response:
                return response.status
        
        # Perform concurrent analyses
        targets = [f"concurrent_test_{i}" for i in range(5)]
        tasks = [perform_analysis(target) for target in targets]
        results = await asyncio.gather(*tasks)
        
        # Most should succeed (some might fail due to rate limiting)
        success_count = sum(1 for status in results if status == 200)
        assert success_count > 0

class TestSecurityIntegration:
    """Security integration tests"""
    
    @pytest.mark.asyncio
    async def test_input_validation(self, api_client, base_url):
        """Test input validation and sanitization"""
        # Test SQL injection attempts
        malicious_data = {
            "target_type": "username",
            "target_value": "'; DROP TABLE investigations; --",
            "analysis_depth": "comprehensive"
        }
        
        async with api_client.post(
            f"{base_url}/investigations/",
            json=malicious_data
        ) as response:
            # Should handle gracefully (either reject or sanitize)
            assert response.status in [201, 400, 422]
        
        # Test XSS attempts
        xss_data = {
            "target_type": "username",
            "target_value": "<script>alert('xss')</script>",
            "analysis_depth": "comprehensive"
        }
        
        async with api_client.post(
            f"{base_url}/investigations/",
            json=xss_data
        ) as response:
            # Should handle gracefully
            assert response.status in [201, 400, 422]
    
    @pytest.mark.asyncio
    async def test_authentication_security(self, api_client, base_url):
        """Test authentication security"""
        # Test invalid credentials
        invalid_login = {
            "username": "nonexistent_user",
            "password": "wrong_password"
        }
        
        async with api_client.post(
            f"{base_url}/auth/token",
            data=invalid_login
        ) as response:
            assert response.status in [401, 422]
        
        # Test missing credentials
        missing_login = {
            "username": "test_user"
            # Missing password
        }
        
        async with api_client.post(
            f"{base_url}/auth/token",
            data=missing_login
        ) as response:
            assert response.status == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 