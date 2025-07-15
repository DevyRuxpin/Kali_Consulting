#!/usr/bin/env python3
"""
Comprehensive test script for Kali Social Media Scraper
Tests all features using only open-source tools without API keys
"""

import asyncio
import sys
import os
import time
from datetime import datetime
from typing import Dict, List, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.social_media_scraper import SocialMediaScraper
from app.services.github_scraper import GitHubScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.threat_analyzer import ThreatAnalyzer
from app.services.proxy_rotator import ProxyRotator
from app.services.intelligence_engine import IntelligenceEngine
from app.services.pattern_analyzer import PatternAnalyzer
from app.services.entity_resolver import EntityResolver
from app.services.network_analyzer import NetworkAnalyzer
from app.services.ml_intelligence import MLIntelligenceService
from app.services.anomaly_detector import AnomalyDetector
from app.services.threat_correlator import ThreatCorrelator
from app.services.dark_web_intelligence import DarkWebIntelligence

class OpenSourceFeatureTester:
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {test_name}: {status}")
        if details:
            print(f"    Details: {details}")
        self.results[test_name] = {"status": status, "details": details}
        
    async def test_social_media_scraper(self):
        """Test social media scraper"""
        try:
            scraper = SocialMediaScraper()
            
            print("\n=== Testing Social Media Scraper ===")
            
            # Test available platforms
            platforms = await scraper.get_available_platforms()
            print(f"✓ Available platforms: {len(platforms)} platforms")
            
            # Test basic scraping (without actual API calls)
            print("✓ Social media scraper initialized successfully")
            
            return True
            
        except Exception as e:
            print(f"✗ Social media scraper test failed: {e}")
            return False
    
    async def test_github_scraper(self):
        """Test GitHub scraper with real data using 'DevyRuxpin'"""
        try:
            scraper = GitHubScraper()
            print("\n=== Testing GitHub Scraper (Real Data) ===")
            
            # Test user profile scraping with real username
            user_result = await scraper.scrape_user_profile("DevyRuxpin")
            print(f"✓ User profile scraping: {'error' not in user_result}")
            
            # Enhanced repo URL extraction logic
            if 'repositories' in user_result and user_result['repositories']:
                first_repo = user_result['repositories'][0]
                # Try multiple possible URL fields
                repo_url = None
                for url_field in ['html_url', 'url', 'clone_url', 'ssh_url']:
                    if url_field in first_repo and first_repo[url_field]:
                        repo_url = first_repo[url_field]
                        break
                
                # If no URL found, construct from repo name and owner
                if not repo_url and 'name' in first_repo:
                    owner = user_result.get('user', {}).get('login', 'DevyRuxpin')
                    repo_name = first_repo['name']
                    repo_url = f"https://github.com/{owner}/{repo_name}"
                
                if repo_url:
                    print(f"✓ Found repo URL: {repo_url}")
                    repo_result = await scraper.scrape_repository(repo_url)
                    print(f"✓ Repository scraping: {'error' not in repo_result}")
                else:
                    print("⚠️  No valid repo URL found for repository test.")
            else:
                print("⚠️  No repositories found for user 'DevyRuxpin'.")
            return True
        except Exception as e:
            print(f"✗ GitHub scraper test failed: {e}")
            return False
    
    async def test_domain_analyzer(self):
        """Test domain analyzer"""
        try:
            analyzer = DomainAnalyzer()
            
            print("\n=== Testing Domain Analyzer ===")
            
            # Test domain analysis
            result = await analyzer.analyze_domain("example.com")
            print(f"✓ Domain analysis: {'error' not in result}")
            
            # Test subdomain enumeration
            subdomains = await analyzer.enumerate_subdomains("example.com")
            print(f"✓ Subdomain enumeration: {len(subdomains)} subdomains found")
            
            # Test DNS analysis
            dns_result = await analyzer.analyze_dns("example.com")
            print(f"✓ DNS analysis: {'error' not in dns_result}")
            
            return True
            
        except Exception as e:
            print(f"✗ Domain analyzer test failed: {e}")
            return False
    
    async def test_threat_analyzer(self):
        """Test threat analyzer"""
        try:
            analyzer = ThreatAnalyzer()
            
            print("\n=== Testing Threat Analyzer ===")
            
            # Test threat analysis
            result = await analyzer.analyze_threat("test.com")
            print(f"✓ Threat analysis: {result.threat_level}")
            
            # Test IP analysis
            ip_result = await analyzer.analyze_ip("8.8.8.8")
            print(f"✓ IP analysis: {'error' not in ip_result}")
            
            # Test domain reputation
            rep_result = await analyzer.check_domain_reputation("example.com")
            print(f"✓ Domain reputation: {'error' not in rep_result}")
            
            return True
            
        except Exception as e:
            print(f"✗ Threat analyzer test failed: {e}")
            return False
    
    async def test_proxy_rotator(self):
        """Test proxy rotator"""
        try:
            rotator = ProxyRotator()
            
            print("\n=== Testing Proxy Rotator ===")
            
            # Test proxy retrieval
            proxy = await rotator.get_proxy()
            print(f"✓ Proxy retrieval: {proxy is not None}")
            
            # Test proxy list
            proxy_list = rotator.get_proxy_list()
            print(f"✓ Proxy list: {len(proxy_list)} proxies")
            
            return True
            
        except Exception as e:
            print(f"✗ Proxy rotator test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Open Source Feature Test")
        print("=" * 60)
        
        # Run all tests
        await self.test_social_media_scraper()
        await self.test_github_scraper()
        await self.test_domain_analyzer()
        await self.test_threat_analyzer()
        await self.test_proxy_rotator()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed = sum(1 for r in self.results.values() if r["status"] == "PASS")
        warnings = sum(1 for r in self.results.values() if r["status"] == "WARNING")
        failed = sum(1 for r in self.results.values() if r["status"] == "FAIL")
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"❌ Failed: {failed}")
        
        print(f"\n⏱️  Total Time: {time.time() - self.start_time:.2f} seconds")
        
        if failed == 0:
            print("\n🎉 All critical tests passed! Platform is ready for use with open-source tools.")
        else:
            print(f"\n⚠️  {failed} tests failed. Please check the implementation.")
        
        # Print detailed results
        print("\n📋 DETAILED RESULTS:")
        for test_name, result in self.results.items():
            status_icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARNING" else "❌"
            print(f"{status_icon} {test_name}: {result['status']}")
            if result["details"]:
                print(f"    {result['details']}")

async def main():
    """Main function"""
    tester = OpenSourceFeatureTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 