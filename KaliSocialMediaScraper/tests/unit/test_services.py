"""
Comprehensive Unit Tests for Services
Target: 85-90% coverage for all service modules
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from typing import Dict, Any, List

from app.services.social_media_scraper import SocialMediaScraper
from app.services.github_scraper import GitHubScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.threat_analyzer import ThreatAnalyzer
from app.services.intelligence_engine import IntelligenceEngine
from app.services.anomaly_detector import AnomalyDetector
from app.services.pattern_analyzer import PatternAnalyzer
from app.services.entity_resolver import EntityResolver
from app.services.network_analyzer import NetworkAnalyzer
from app.services.ml_intelligence import MLIntelligenceService
from app.services.dark_web_intelligence import DarkWebIntelligence
from app.services.threat_correlator import ThreatCorrelator
from app.models.schemas import PlatformType, ThreatLevel, ThreatAssessment

class TestSocialMediaScraper:
    """Comprehensive unit tests for SocialMediaScraper"""
    
    @pytest.mark.asyncio
    async def test_scraper_initialization(self):
        """Test scraper initialization"""
        scraper = SocialMediaScraper()
        assert scraper.rate_limits is not None
        assert PlatformType.TWITTER in scraper.rate_limits
        assert PlatformType.GITHUB in scraper.rate_limits
    
    @pytest.mark.asyncio
    async def test_scraper_context_manager(self):
        """Test async context manager functionality"""
        async with SocialMediaScraper() as scraper:
            assert scraper.session is not None
    
    @pytest.mark.asyncio
    async def test_ensure_session_raises_error(self):
        """Test session validation"""
        scraper = SocialMediaScraper()
        with pytest.raises(RuntimeError):
            scraper._ensure_session()
    
    @pytest.mark.asyncio
    @patch('app.services.social_media_scraper.proxy_rotator')
    async def test_session_creation_with_proxy(self, mock_proxy_rotator):
        """Test session creation with proxy"""
        mock_session = AsyncMock()
        mock_proxy_rotator.create_session_with_proxy = AsyncMock(return_value=mock_session)
        
        async with SocialMediaScraper() as scraper:
            assert scraper.session == mock_session
    
    @pytest.mark.asyncio
    @patch('app.services.social_media_scraper.proxy_rotator')
    async def test_session_creation_fallback(self, mock_proxy_rotator):
        """Test session creation fallback when no proxy available"""
        mock_proxy_rotator.create_session_with_proxy = AsyncMock(return_value=None)
        
        async with SocialMediaScraper() as scraper:
            assert scraper.session is not None
            assert hasattr(scraper.session, 'headers')
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting functionality"""
        scraper = SocialMediaScraper()
        
        # Test rate limiting for different platforms
        start_time = datetime.now()
        await scraper._respect_rate_limit(PlatformType.TWITTER)
        end_time = datetime.now()
        
        # Should not take too long for rate limiting
        assert (end_time - start_time).total_seconds() < 1
    
    @pytest.mark.asyncio
    async def test_scrape_platform_unsupported(self):
        """Test scraping unsupported platform"""
        async with SocialMediaScraper() as scraper:
            result = await scraper.scrape_platform("UNSUPPORTED_PLATFORM", "test")
            assert "error" in result
            assert "Unsupported platform" in result["error"]
    
    @pytest.mark.asyncio
    @patch('app.services.social_media_scraper.SocialMediaScraper._scrape_twitter')
    async def test_scrape_platform_twitter(self, mock_twitter_scrape):
        """Test Twitter platform scraping"""
        mock_twitter_scrape.return_value = {"platform": "twitter", "data": "test"}
        
        async with SocialMediaScraper() as scraper:
            result = await scraper.scrape_platform(PlatformType.TWITTER, "test_user")
            assert result == {"platform": "twitter", "data": "test"}
            mock_twitter_scrape.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_profile_error_handling(self):
        """Test profile analysis error handling"""
        async with SocialMediaScraper() as scraper:
            # Mock _get_profile_data to return None
            scraper._get_profile_data = AsyncMock(return_value=None)
            
            result = await scraper.analyze_profile(PlatformType.TWITTER, "test_user")
            assert "error" in result
            assert "Profile not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_search_content_unsupported_platform(self):
        """Test search content for unsupported platform"""
        async with SocialMediaScraper() as scraper:
            result = await scraper.search_content(PlatformType.TELEGRAM, "test")
            assert "error" in result
            assert "Search not supported" in result["error"]
    
    @pytest.mark.asyncio
    async def test_assess_profile_threat(self):
        """Test threat assessment functionality"""
        async with SocialMediaScraper() as scraper:
            profile_data = {
                "followers_count": 15000,
                "posts_count": 1500,
                "bio": "nazi extremist content"
            }
            posts = [{"content": "white power content"}]
            
            result = await scraper._assess_profile_threat(
                PlatformType.TWITTER, profile_data, posts
            )
            
            assert "threat_level" in result
            assert "threat_score" in result
            assert "threat_indicators" in result
            assert result["threat_score"] > 0
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment(self):
        """Test sentiment analysis"""
        async with SocialMediaScraper() as scraper:
            posts = [
                {"content": "I love this platform, it's great!"},
                {"content": "This is terrible and awful"},
                {"content": "Neutral content here"}
            ]
            
            result = await scraper._analyze_sentiment(posts)
            
            assert "total_posts" in result
            assert "positive_posts" in result
            assert "negative_posts" in result
            assert "neutral_posts" in result
            assert "overall_sentiment" in result
            assert "sentiment_score" in result
            assert result["total_posts"] == 3

class TestGitHubScraper:
    """Comprehensive unit tests for GitHubScraper"""
    
    @pytest.mark.asyncio
    async def test_github_scraper_initialization(self):
        """Test GitHub scraper initialization"""
        scraper = GitHubScraper()
        assert scraper is not None
    
    @pytest.mark.asyncio
    @patch('app.services.github_scraper.aiohttp.ClientSession')
    async def test_scrape_user_success(self, mock_session):
        """Test successful user scraping"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "login": "test_user",
            "name": "Test User",
            "bio": "Test bio",
            "followers": 100,
            "following": 50,
            "public_repos": 10,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "avatar_url": "https://example.com/avatar.jpg",
            "html_url": "https://github.com/test_user"
        }
        
        # Setup the session mock properly
        mock_session_instance = AsyncMock()
        mock_session_instance.close = AsyncMock()
        
        # Setup the get method to return a proper async context manager
        mock_get_context = AsyncMock()
        mock_get_context.__aenter__.return_value = mock_response
        mock_get_context.__aexit__.return_value = None
        mock_session_instance.get.return_value = mock_get_context
        
        # Setup the session constructor to return our mock instance
        mock_session.return_value = mock_session_instance
        
        # Mock the _get_user_data method to return the expected data
        with patch('app.services.github_scraper.GitHubScraper._get_user_data', return_value={
            "login": "test_user",
            "name": "Test User",
            "bio": "Test bio",
            "followers": 100,
            "following": 50,
            "public_repos": 10,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "avatar_url": "https://example.com/avatar.jpg",
            "html_url": "https://github.com/test_user"
        }):
            from app.services.github_scraper import GitHubScraper
            async with GitHubScraper() as scraper:
                result = await scraper.scrape_user("test_user")
                assert "user" in result
                assert result["user"]["login"] == "test_user"
    
    @pytest.mark.asyncio
    @patch('app.services.github_scraper.aiohttp.ClientSession')
    async def test_scrape_user_error(self, mock_session):
        """Test user scraping error handling"""
        mock_response = AsyncMock()
        mock_response.status = 404
        
        mock_session.return_value.__aenter__.return_value.get.return_value = mock_response
        
        scraper = GitHubScraper()
        result = await scraper.scrape_user("nonexistent_user")
        
        assert "error" in result
        assert "User not found" in result["error"]

class TestDomainAnalyzer:
    """Comprehensive unit tests for DomainAnalyzer"""
    
    @pytest.mark.asyncio
    async def test_domain_analyzer_initialization(self):
        """Test domain analyzer initialization"""
        analyzer = DomainAnalyzer()
        assert analyzer is not None
    
    @pytest.mark.asyncio
    async def test_analyze_domain_basic(self):
        """Test basic domain analysis"""
        analyzer = DomainAnalyzer()
        result = await analyzer.analyze_domain("example.com")
        
        assert "domain" in result
        assert "analysis" in result
        assert result["domain"] == "example.com"
    
    @pytest.mark.asyncio
    async def test_get_domain_info(self):
        """Test domain info retrieval"""
        analyzer = DomainAnalyzer()
        result = await analyzer.get_domain_info("example.com")
        
        assert "domain" in result
        assert "info" in result
    
    @pytest.mark.asyncio
    async def test_check_domain_reputation(self):
        """Test domain reputation checking"""
        analyzer = DomainAnalyzer()
        result = await analyzer.check_domain_reputation("example.com")
        
        assert "domain" in result
        assert "reputation" in result

class TestThreatAnalyzer:
    """Comprehensive unit tests for ThreatAnalyzer"""
    
    @pytest.mark.asyncio
    async def test_threat_analyzer_initialization(self):
        """Test threat analyzer initialization"""
        analyzer = ThreatAnalyzer()
        assert analyzer is not None
    
    @pytest.mark.asyncio
    async def test_analyze_threat(self):
        """Test threat analysis"""
        analyzer = ThreatAnalyzer()
        threat_data = {
            "source": "twitter",
            "content": "suspicious content",
            "user": "test_user"
        }
        
        result = await analyzer.analyze_threat(threat_data)
        
        assert "threat_level" in result
        assert "confidence" in result
        assert "indicators" in result
    
    @pytest.mark.asyncio
    async def test_correlate_threats(self):
        """Test threat correlation"""
        analyzer = ThreatAnalyzer()
        threats = [
            {"source": "twitter", "threat_type": "suspicious"},
            {"source": "github", "threat_type": "malware"}
        ]
        
        result = await analyzer.correlate_threats(threats)
        
        assert "correlated_threats" in result
        assert "correlation_score" in result
    
    @pytest.mark.asyncio
    async def test_generate_threat_report(self):
        """Test threat report generation"""
        analyzer = ThreatAnalyzer()
        threat_data = {
            "threats": [{"source": "twitter", "level": "high"}],
            "correlations": [{"type": "malware", "confidence": 0.8}]
        }
        
        result = await analyzer.generate_threat_report(threat_data)
        
        assert "report" in result
        assert "summary" in result
        assert "recommendations" in result

class TestIntelligenceEngine:
    """Comprehensive unit tests for IntelligenceEngine"""
    
    @pytest.mark.asyncio
    async def test_intelligence_engine_initialization(self):
        """Test intelligence engine initialization"""
        engine = IntelligenceEngine()
        assert engine is not None
    
    @pytest.mark.asyncio
    async def test_process_intelligence(self):
        """Test intelligence processing"""
        engine = IntelligenceEngine()
        data = {
            "social_media": {"twitter": "data"},
            "github": {"repos": "data"},
            "domain": {"info": "data"}
        }
        
        result = await engine.process_intelligence(data)
        
        assert "processed_data" in result
        assert "insights" in result
    
    @pytest.mark.asyncio
    async def test_generate_report(self):
        """Test report generation"""
        engine = IntelligenceEngine()
        intelligence_data = {
            "threats": [{"level": "high"}],
            "correlations": [{"type": "malware"}],
            "insights": ["suspicious activity"]
        }
        
        result = await engine.generate_report(intelligence_data)
        
        assert "report" in result
        assert "executive_summary" in result
        assert "detailed_analysis" in result
    
    @pytest.mark.asyncio
    async def test_correlate_data(self):
        """Test data correlation"""
        engine = IntelligenceEngine()
        data_sources = [
            {"source": "twitter", "data": "user posts"},
            {"source": "github", "data": "repository activity"},
            {"source": "domain", "data": "domain info"}
        ]
        
        result = await engine.correlate_data(data_sources)
        
        assert "correlations" in result
        assert "confidence_scores" in result

class TestAnomalyDetector:
    """Comprehensive unit tests for AnomalyDetector"""
    
    @pytest.mark.asyncio
    async def test_anomaly_detector_initialization(self):
        """Test anomaly detector initialization"""
        detector = AnomalyDetector()
        assert detector is not None
    
    @pytest.mark.asyncio
    async def test_detect_anomalies(self):
        """Test anomaly detection"""
        detector = AnomalyDetector()
        data = [
            {"timestamp": "2024-01-01", "activity": "normal"},
            {"timestamp": "2024-01-02", "activity": "suspicious"},
            {"timestamp": "2024-01-03", "activity": "normal"}
        ]
        
        result = await detector.detect_anomalies(data)
        
        assert "anomalies" in result
        assert "anomaly_score" in result
    
    @pytest.mark.asyncio
    async def test_analyze_patterns(self):
        """Test pattern analysis"""
        detector = AnomalyDetector()
        patterns = [
            {"type": "login", "frequency": "normal"},
            {"type": "post", "frequency": "high"},
            {"type": "download", "frequency": "suspicious"}
        ]
        
        result = await detector.analyze_patterns(patterns)
        
        assert "pattern_analysis" in result
        assert "risk_assessment" in result

class TestPatternAnalyzer:
    """Comprehensive unit tests for PatternAnalyzer"""
    
    @pytest.mark.asyncio
    async def test_pattern_analyzer_initialization(self):
        """Test pattern analyzer initialization"""
        analyzer = PatternAnalyzer()
        assert analyzer is not None
    
    @pytest.mark.asyncio
    async def test_analyze_patterns(self):
        """Test pattern analysis"""
        analyzer = PatternAnalyzer()
        data = [
            {"content": "normal content"},
            {"content": "suspicious pattern content"},
            {"content": "another normal content"}
        ]
        
        result = await analyzer.analyze_patterns(data)
        
        assert "patterns" in result
        assert "pattern_types" in result
        assert "confidence" in result
    
    @pytest.mark.asyncio
    async def test_extract_entities(self):
        """Test entity extraction"""
        analyzer = PatternAnalyzer()
        text = "User @john_doe posted about #security on example.com"
        
        result = await analyzer.extract_entities(text)
        
        assert "entities" in result
        assert "entity_types" in result

class TestEntityResolver:
    """Comprehensive unit tests for EntityResolver"""
    
    @pytest.mark.asyncio
    async def test_entity_resolver_initialization(self):
        """Test entity resolver initialization"""
        resolver = EntityResolver()
        assert resolver is not None
    
    @pytest.mark.asyncio
    async def test_resolve_entities(self):
        """Test entity resolution"""
        resolver = EntityResolver()
        entities = [
            {"type": "username", "value": "john_doe"},
            {"type": "domain", "value": "example.com"},
            {"type": "email", "value": "john@example.com"}
        ]
        
        result = await resolver.resolve_entities(entities)
        
        assert "resolved_entities" in result
        assert "entity_relationships" in result
    
    @pytest.mark.asyncio
    async def test_correlate_entities(self):
        """Test entity correlation"""
        resolver = EntityResolver()
        entity_data = [
            {"id": "1", "type": "user", "platform": "twitter"},
            {"id": "2", "type": "user", "platform": "github"},
            {"id": "3", "type": "domain", "platform": "web"}
        ]
        
        result = await resolver.correlate_entities(entity_data)
        
        assert "correlations" in result
        assert "confidence_scores" in result

class TestNetworkAnalyzer:
    """Comprehensive unit tests for NetworkAnalyzer"""
    
    @pytest.mark.asyncio
    async def test_network_analyzer_initialization(self):
        """Test network analyzer initialization"""
        analyzer = NetworkAnalyzer()
        assert analyzer is not None
    
    @pytest.mark.asyncio
    async def test_analyze_network(self):
        """Test network analysis"""
        analyzer = NetworkAnalyzer()
        network_data = {
            "nodes": [{"id": "1", "type": "user"}, {"id": "2", "type": "domain"}],
            "edges": [{"from": "1", "to": "2", "type": "mentions"}]
        }
        
        result = await analyzer.analyze_network(network_data)
        
        assert "network_analysis" in result
        assert "centrality_scores" in result
        assert "community_detection" in result
    
    @pytest.mark.asyncio
    async def test_detect_communities(self):
        """Test community detection"""
        analyzer = NetworkAnalyzer()
        nodes = [
            {"id": "1", "connections": ["2", "3"]},
            {"id": "2", "connections": ["1", "3"]},
            {"id": "3", "connections": ["1", "2"]}
        ]
        
        result = await analyzer.detect_communities(nodes)
        
        assert "communities" in result
        assert "community_scores" in result

class TestMLIntelligenceService:
    """Comprehensive unit tests for MLIntelligenceService"""
    
    @pytest.mark.asyncio
    async def test_ml_intelligence_initialization(self):
        """Test ML intelligence initialization"""
        ml_intel = MLIntelligenceService()
        assert ml_intel is not None
    
    @pytest.mark.asyncio
    async def test_predict_threat(self):
        """Test threat prediction"""
        ml_intel = MLIntelligenceService()
        features = {
            "user_activity": "high",
            "content_sentiment": "negative",
            "network_connections": "suspicious"
        }
        
        result = await ml_intel.predict_threat(features)
        
        assert "prediction" in result
        assert "confidence" in result
        assert "explanation" in result
    
    @pytest.mark.asyncio
    async def test_classify_content(self):
        """Test content classification"""
        ml_intel = MLIntelligenceService()
        content = "This is suspicious content that needs classification"
        
        result = await ml_intel.classify_content(content)
        
        assert "classification" in result
        assert "confidence" in result
        assert "categories" in result

class TestDarkWebIntelligence:
    """Comprehensive unit tests for DarkWebIntelligence"""
    
    @pytest.mark.asyncio
    async def test_dark_web_intelligence_initialization(self):
        """Test dark web intelligence initialization"""
        dark_intel = DarkWebIntelligence()
        assert dark_intel is not None
    
    @pytest.mark.asyncio
    async def test_search_dark_web(self):
        """Test dark web search"""
        dark_intel = DarkWebIntelligence()
        query = "test target"
        
        result = await dark_intel.search_dark_web(query)
        
        assert "search_results" in result
        assert "sources" in result
        assert "relevance_scores" in result
    
    @pytest.mark.asyncio
    async def test_monitor_dark_web(self):
        """Test dark web monitoring"""
        dark_intel = DarkWebIntelligence()
        targets = ["target1", "target2"]
        
        result = await dark_intel.monitor_dark_web(targets)
        
        assert "monitoring_results" in result
        assert "alerts" in result

class TestThreatCorrelator:
    """Comprehensive unit tests for ThreatCorrelator"""
    
    @pytest.mark.asyncio
    async def test_threat_correlator_initialization(self):
        """Test threat correlator initialization"""
        correlator = ThreatCorrelator()
        assert correlator is not None
    
    @pytest.mark.asyncio
    async def test_correlate_threats(self):
        """Test threat correlation"""
        correlator = ThreatCorrelator()
        threats = [
            {"source": "twitter", "type": "suspicious_behavior"},
            {"source": "github", "type": "malware_repository"},
            {"source": "domain", "type": "malicious_domain"}
        ]
        
        result = await correlator.correlate_threats(threats)
        
        assert "correlations" in result
        assert "correlation_matrix" in result
        assert "confidence_scores" in result
    
    @pytest.mark.asyncio
    async def test_generate_correlation_report(self):
        """Test correlation report generation"""
        correlator = ThreatCorrelator()
        correlation_data = {
            "correlations": [{"type": "malware", "confidence": 0.8}],
            "threats": [{"source": "twitter", "level": "high"}]
        }
        
        result = await correlator.generate_correlation_report(correlation_data)
        
        assert "report" in result
        assert "summary" in result
        assert "recommendations" in result 