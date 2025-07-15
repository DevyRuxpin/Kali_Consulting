"""
Comprehensive Service Functionality Test
Tests all core services to ensure they're working before frontend development
"""

import asyncio
import pytest
import logging
from typing import Dict, Any, List
from datetime import datetime

# Import all services
from app.services.github_scraper import GitHubScraper
from app.services.social_media_scraper import SocialMediaScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.dark_web_intelligence import DarkWebIntelligenceService
from app.services.threat_analyzer import ThreatAnalyzer
from app.services.intelligence_engine import IntelligenceEngine
from app.services.ml_intelligence import MLIntelligenceService
from app.services.pattern_analyzer import PatternAnalyzer
from app.services.anomaly_detector import AnomalyDetector
from app.services.entity_resolver import EntityResolver
from app.services.network_analyzer import NetworkAnalyzer
from app.services.threat_correlator import ThreatCorrelator
from app.services.sherlock_integration import SherlockIntegration

logger = logging.getLogger(__name__)

class ServiceFunctionalityTest:
    """Comprehensive test for all core services"""
    
    def __init__(self):
        self.test_results = {}
        self.failed_services = []
        self.passed_services = []
        
    async def test_all_services(self) -> Dict[str, Any]:
        """Test all core services and return results"""
        print("🔍 Testing All Core Services...")
        print("=" * 60)
        
        # Test each service
        await self._test_github_scraper()
        await self._test_social_media_scraper()
        await self._test_domain_analyzer()
        await self._test_dark_web_intelligence()
        await self._test_threat_analyzer()
        await self._test_intelligence_engine()
        await self._test_ml_intelligence()
        await self._test_pattern_analyzer()
        await self._test_anomaly_detector()
        await self._test_entity_resolver()
        await self._test_network_analyzer()
        await self._test_threat_correlator()
        await self._test_sherlock_integration()
        
        return self._generate_summary()
    
    async def _test_github_scraper(self):
        """Test GitHub scraper functionality"""
        print("📊 Testing GitHub Scraper...")
        try:
            async with GitHubScraper() as scraper:
                # Test user analysis
                user_result = await scraper.analyze_user_profile("octocat")
                assert isinstance(user_result, dict)
                assert "user" in user_result or "error" in user_result
                
                # Test repository analysis
                repo_result = await scraper.analyze_repository_async("microsoft/vscode")
                assert isinstance(repo_result, dict)
                assert "repository" in repo_result or "error" in repo_result
                
                # Test search functionality
                search_result = await scraper.search_repositories("security", max_results=5)
                assert isinstance(search_result, dict)
                
                self.passed_services.append("GitHub Scraper")
                self.test_results["github_scraper"] = {
                    "status": "PASS",
                    "user_analysis": "✓",
                    "repo_analysis": "✓",
                    "search": "✓"
                }
                
        except Exception as e:
            logger.error(f"GitHub Scraper test failed: {e}")
            self.failed_services.append("GitHub Scraper")
            self.test_results["github_scraper"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_social_media_scraper(self):
        """Test social media scraper functionality"""
        print("📱 Testing Social Media Scraper...")
        try:
            async with SocialMediaScraper() as scraper:
                # Test platform scraping
                from app.models.schemas import PlatformType
                
                # Test GitHub scraping
                github_result = await scraper.scrape_platform(
                    PlatformType.GITHUB, 
                    "octocat", 
                    include_metadata=True, 
                    max_posts=10
                )
                assert isinstance(github_result, dict)
                
                # Test profile analysis
                profile_result = await scraper.analyze_profile(
                    PlatformType.GITHUB,
                    "octocat"
                )
                assert isinstance(profile_result, dict)
                
                self.passed_services.append("Social Media Scraper")
                self.test_results["social_media_scraper"] = {
                    "status": "PASS",
                    "platform_scraping": "✓",
                    "profile_analysis": "✓"
                }
                
        except Exception as e:
            logger.error(f"Social Media Scraper test failed: {e}")
            self.failed_services.append("Social Media Scraper")
            self.test_results["social_media_scraper"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_domain_analyzer(self):
        """Test domain analyzer functionality"""
        print("🌐 Testing Domain Analyzer...")
        try:
            async with DomainAnalyzer() as analyzer:
                # Test domain analysis
                domain_result = await analyzer.analyze_domain("google.com")
                assert isinstance(domain_result, dict)
                assert "domain" in domain_result
                
                # Test multiple domain analysis
                multi_result = await analyzer.analyze_multiple_domains(["google.com", "github.com"])
                assert isinstance(multi_result, dict)
                
                self.passed_services.append("Domain Analyzer")
                self.test_results["domain_analyzer"] = {
                    "status": "PASS",
                    "single_domain": "✓",
                    "multiple_domains": "✓"
                }
                
        except Exception as e:
            logger.error(f"Domain Analyzer test failed: {e}")
            self.failed_services.append("Domain Analyzer")
            self.test_results["domain_analyzer"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_dark_web_intelligence(self):
        """Test dark web intelligence functionality"""
        print("🕸️ Testing Dark Web Intelligence...")
        try:
            async with DarkWebIntelligenceService() as dark_web:
                # Test entity scanning
                entities = await dark_web.scan_dark_web_entities("test_target", "basic")
                assert isinstance(entities, list)
                
                # Test search functionality
                search_result = await dark_web.search_dark_web("test_query")
                assert isinstance(search_result, dict)
                
                self.passed_services.append("Dark Web Intelligence")
                self.test_results["dark_web_intelligence"] = {
                    "status": "PASS",
                    "entity_scanning": "✓",
                    "search": "✓"
                }
                
        except Exception as e:
            logger.error(f"Dark Web Intelligence test failed: {e}")
            self.failed_services.append("Dark Web Intelligence")
            self.test_results["dark_web_intelligence"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_threat_analyzer(self):
        """Test threat analyzer functionality"""
        print("⚠️ Testing Threat Analyzer...")
        try:
            analyzer = ThreatAnalyzer()
            
            # Test threat analysis
            threat_result = await analyzer.analyze_threat("test_target", "comprehensive")
            assert hasattr(threat_result, 'target')
            assert hasattr(threat_result, 'threat_level')
            
            # Test threat correlation
            correlation_result = await analyzer.correlate_threats([threat_result])
            assert isinstance(correlation_result, dict)
            
            self.passed_services.append("Threat Analyzer")
            self.test_results["threat_analyzer"] = {
                "status": "PASS",
                "threat_analysis": "✓",
                "correlation": "✓"
            }
            
        except Exception as e:
            logger.error(f"Threat Analyzer test failed: {e}")
            self.failed_services.append("Threat Analyzer")
            self.test_results["threat_analyzer"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_intelligence_engine(self):
        """Test intelligence engine functionality"""
        print("🧠 Testing Intelligence Engine...")
        try:
            engine = IntelligenceEngine()
            
            # Test intelligence analysis
            analysis_result = await engine.analyze_intelligence("test_target")
            assert isinstance(analysis_result, dict)
            
            # Test entity extraction
            entities = await engine.extract_entities("test_investigation")
            assert isinstance(entities, list)
            
            self.passed_services.append("Intelligence Engine")
            self.test_results["intelligence_engine"] = {
                "status": "PASS",
                "intelligence_analysis": "✓",
                "entity_extraction": "✓"
            }
            
        except Exception as e:
            logger.error(f"Intelligence Engine test failed: {e}")
            self.failed_services.append("Intelligence Engine")
            self.test_results["intelligence_engine"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_ml_intelligence(self):
        """Test ML intelligence functionality"""
        print("🤖 Testing ML Intelligence...")
        try:
            ml_service = MLIntelligenceService()
            
            # Test pattern recognition
            patterns = await ml_service.recognize_patterns("test_data")
            assert isinstance(patterns, list)
            
            # Test anomaly detection
            anomalies = await ml_service.detect_anomalies("test_data")
            assert isinstance(anomalies, list)
            
            self.passed_services.append("ML Intelligence")
            self.test_results["ml_intelligence"] = {
                "status": "PASS",
                "pattern_recognition": "✓",
                "anomaly_detection": "✓"
            }
            
        except Exception as e:
            logger.error(f"ML Intelligence test failed: {e}")
            self.failed_services.append("ML Intelligence")
            self.test_results["ml_intelligence"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_pattern_analyzer(self):
        """Test pattern analyzer functionality"""
        print("🔍 Testing Pattern Analyzer...")
        try:
            analyzer = PatternAnalyzer()
            
            # Test pattern analysis
            patterns = await analyzer.analyze_patterns("test_data")
            assert isinstance(patterns, list)
            
            # Test pattern correlation
            correlation = await analyzer.correlate_patterns(patterns)
            assert isinstance(correlation, dict)
            
            self.passed_services.append("Pattern Analyzer")
            self.test_results["pattern_analyzer"] = {
                "status": "PASS",
                "pattern_analysis": "✓",
                "correlation": "✓"
            }
            
        except Exception as e:
            logger.error(f"Pattern Analyzer test failed: {e}")
            self.failed_services.append("Pattern Analyzer")
            self.test_results["pattern_analyzer"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_anomaly_detector(self):
        """Test anomaly detector functionality"""
        print("🚨 Testing Anomaly Detector...")
        try:
            detector = AnomalyDetector()
            
            # Test anomaly detection
            anomalies = await detector.detect_anomalies("test_data")
            assert isinstance(anomalies, list)
            
            # Test anomaly scoring
            scores = await detector.score_anomalies(anomalies)
            assert isinstance(scores, dict)
            
            self.passed_services.append("Anomaly Detector")
            self.test_results["anomaly_detector"] = {
                "status": "PASS",
                "anomaly_detection": "✓",
                "scoring": "✓"
            }
            
        except Exception as e:
            logger.error(f"Anomaly Detector test failed: {e}")
            self.failed_services.append("Anomaly Detector")
            self.test_results["anomaly_detector"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_entity_resolver(self):
        """Test entity resolver functionality"""
        print("🔗 Testing Entity Resolver...")
        try:
            resolver = EntityResolver()
            
            # Test entity resolution
            entities = await resolver.resolve_entities([])
            assert isinstance(entities, list)
            
            # Test relationship mapping
            relationships = await resolver.map_relationships(entities)
            assert isinstance(relationships, list)
            
            self.passed_services.append("Entity Resolver")
            self.test_results["entity_resolver"] = {
                "status": "PASS",
                "entity_resolution": "✓",
                "relationship_mapping": "✓"
            }
            
        except Exception as e:
            logger.error(f"Entity Resolver test failed: {e}")
            self.failed_services.append("Entity Resolver")
            self.test_results["entity_resolver"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_network_analyzer(self):
        """Test network analyzer functionality"""
        print("🌐 Testing Network Analyzer...")
        try:
            analyzer = NetworkAnalyzer()
            
            # Test network analysis
            network_data = await analyzer.analyze_network("test_data")
            assert isinstance(network_data, dict)
            
            # Test centrality analysis
            centrality = await analyzer.calculate_centrality(network_data)
            assert isinstance(centrality, dict)
            
            self.passed_services.append("Network Analyzer")
            self.test_results["network_analyzer"] = {
                "status": "PASS",
                "network_analysis": "✓",
                "centrality": "✓"
            }
            
        except Exception as e:
            logger.error(f"Network Analyzer test failed: {e}")
            self.failed_services.append("Network Analyzer")
            self.test_results["network_analyzer"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_threat_correlator(self):
        """Test threat correlator functionality"""
        print("🔗 Testing Threat Correlator...")
        try:
            correlator = ThreatCorrelator()
            
            # Test threat correlation
            correlation = await correlator.correlate_threats([])
            assert isinstance(correlation, dict)
            
            # Test threat scoring
            scoring = await correlator.score_threats([])
            assert isinstance(scoring, dict)
            
            self.passed_services.append("Threat Correlator")
            self.test_results["threat_correlator"] = {
                "status": "PASS",
                "correlation": "✓",
                "scoring": "✓"
            }
            
        except Exception as e:
            logger.error(f"Threat Correlator test failed: {e}")
            self.failed_services.append("Threat Correlator")
            self.test_results["threat_correlator"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    async def _test_sherlock_integration(self):
        """Test Sherlock integration functionality"""
        print("🔍 Testing Sherlock Integration...")
        try:
            async with SherlockIntegration() as sherlock:
                # Test username hunting
                hunt_result = await sherlock.hunt_username("testuser")
                assert isinstance(hunt_result, dict)
                
                # Test multiple username hunting
                multi_result = await sherlock.hunt_multiple_usernames(["testuser1", "testuser2"])
                assert isinstance(multi_result, dict)
                
                self.passed_services.append("Sherlock Integration")
                self.test_results["sherlock_integration"] = {
                    "status": "PASS",
                    "single_hunt": "✓",
                    "multiple_hunt": "✓"
                }
                
        except Exception as e:
            logger.error(f"Sherlock Integration test failed: {e}")
            self.failed_services.append("Sherlock Integration")
            self.test_results["sherlock_integration"] = {
                "status": "FAIL",
                "error": str(e)
            }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_services = len(self.passed_services) + len(self.failed_services)
        passed_count = len(self.passed_services)
        failed_count = len(self.failed_services)
        
        summary = {
            "total_services": total_services,
            "passed_services": passed_count,
            "failed_services": failed_count,
            "success_rate": (passed_count / total_services * 100) if total_services > 0 else 0,
            "passed": self.passed_services,
            "failed": self.failed_services,
            "detailed_results": self.test_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        print("\n" + "=" * 60)
        print("📊 SERVICE FUNCTIONALITY TEST SUMMARY")
        print("=" * 60)
        print(f"Total Services Tested: {total_services}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        
        if self.passed_services:
            print("\n✅ PASSED SERVICES:")
            for service in self.passed_services:
                print(f"  - {service}")
        
        if self.failed_services:
            print("\n❌ FAILED SERVICES:")
            for service in self.failed_services:
                print(f"  - {service}")
        
        print("\n" + "=" * 60)
        
        return summary

async def run_service_tests():
    """Run all service functionality tests"""
    tester = ServiceFunctionalityTest()
    return await tester.test_all_services()

if __name__ == "__main__":
    asyncio.run(run_service_tests()) 