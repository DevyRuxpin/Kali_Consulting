#!/usr/bin/env python3
"""
Comprehensive test script for Kali OSINT Social Media Scraper Platform
Tests all real functionality including scraping, analysis, and report generation
"""

import asyncio
import aiohttp
import json
import time
import logging
from typing import Dict, Any, List
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.social_media_scraper import SocialMediaScraper
from app.services.github_scraper import GitHubScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.threat_analyzer import ThreatAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlatformTester:
    """Comprehensive platform testing class"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = []
        
    async def test_api_health(self) -> bool:
        """Test API health endpoint"""
        logger.info("Testing API health...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"API Health: {data}")
                        self.test_results.append(("API Health", "PASS", "API is healthy"))
                        return True
                    else:
                        logger.error(f"API Health failed: {response.status}")
                        self.test_results.append(("API Health", "FAIL", f"Status: {response.status}"))
                        return False
        except Exception as e:
            logger.error(f"API Health test failed: {e}")
            self.test_results.append(("API Health", "FAIL", str(e)))
            return False
    
    async def test_social_media_scraping(self) -> bool:
        """Test real social media scraping"""
        logger.info("Testing social media scraping...")
        
        try:
            async with SocialMediaScraper() as scraper:
                # Test GitHub scraping (most reliable for testing)
                result = await scraper.scrape_platform(
                    platform="github",
                    target="microsoft",  # Use a well-known organization
                    include_metadata=True,
                    max_posts=5
                )
                
                if "error" not in result:
                    logger.info(f"GitHub scraping successful: {len(result.get('repositories', []))} repos found")
                    self.test_results.append(("Social Media Scraping", "PASS", f"Found {len(result.get('repositories', []))} repositories"))
                    return True
                else:
                    logger.error(f"GitHub scraping failed: {result['error']}")
                    self.test_results.append(("Social Media Scraping", "FAIL", result['error']))
                    return False
        except Exception as e:
            logger.error(f"Social media scraping test failed: {e}")
            self.test_results.append(("Social Media Scraping", "FAIL", str(e)))
            return False
    
    async def test_github_scraping(self) -> bool:
        """Test GitHub-specific scraping"""
        logger.info("Testing GitHub scraping...")
        
        try:
            async with GitHubScraper() as scraper:
                # Test repository analysis
                result = await scraper.analyze_repository_async(
                    repo_url="https://github.com/microsoft/vscode",
                    analysis_depth="basic"
                )
                
                if "error" not in result:
                    logger.info(f"GitHub analysis successful: {result.get('repository', {}).get('name', 'Unknown')}")
                    self.test_results.append(("GitHub Scraping", "PASS", "Repository analysis successful"))
                    return True
                else:
                    logger.error(f"GitHub analysis failed: {result['error']}")
                    self.test_results.append(("GitHub Scraping", "FAIL", result['error']))
                    return False
        except Exception as e:
            logger.error(f"GitHub scraping test failed: {e}")
            self.test_results.append(("GitHub Scraping", "FAIL", str(e)))
            return False
    
    async def test_domain_analysis(self) -> bool:
        """Test domain analysis functionality"""
        logger.info("Testing domain analysis...")
        
        try:
            analyzer = DomainAnalyzer()
            result = await analyzer.analyze_domain("google.com")
            
            if result and "error" not in result:
                logger.info(f"Domain analysis successful: {result.get('domain', 'Unknown')}")
                self.test_results.append(("Domain Analysis", "PASS", "Domain analysis successful"))
                return True
            else:
                error_msg = result.get('error', 'Unknown error') if result else 'No result'
                logger.error(f"Domain analysis failed: {error_msg}")
                self.test_results.append(("Domain Analysis", "FAIL", error_msg))
                return False
        except Exception as e:
            logger.error(f"Domain analysis test failed: {e}")
            self.test_results.append(("Domain Analysis", "FAIL", str(e)))
            return False
    
    async def test_threat_analysis(self) -> bool:
        """Test threat analysis functionality"""
        logger.info("Testing threat analysis...")
        
        try:
            analyzer = ThreatAnalyzer()
            result = await analyzer.analyze_threat("test@example.com", "comprehensive")
            
            if result and hasattr(result, 'threat_level'):
                logger.info(f"Threat analysis successful: {result.threat_level}")
                self.test_results.append(("Threat Analysis", "PASS", f"Threat level: {result.threat_level}"))
                return True
            else:
                error_msg = str(result) if result else 'No result'
                logger.error(f"Threat analysis failed: {error_msg}")
                self.test_results.append(("Threat Analysis", "FAIL", error_msg))
                return False
        except Exception as e:
            logger.error(f"Threat analysis test failed: {e}")
            self.test_results.append(("Threat Analysis", "FAIL", str(e)))
            return False
    
    async def test_report_generation(self) -> bool:
        """Test report generation functionality"""
        logger.info("Testing report generation...")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Create a test investigation first
                investigation_data = {
                    "target_type": "domain",
                    "target_value": "example.com",
                    "analysis_depth": "standard",
                    "platforms": ["github", "twitter"],
                    "include_network_analysis": True,
                    "include_timeline_analysis": True,
                    "include_threat_assessment": True,
                    "analysis_options": {}
                }
                
                # Create investigation
                async with session.post(
                    f"{self.base_url}/api/v1/investigations",
                    json=investigation_data
                ) as response:
                    if response.status == 201:
                        investigation = await response.json()
                        investigation_id = investigation['id']
                        
                        # Test PDF report generation
                        async with session.post(
                            f"{self.base_url}/api/v1/exports/investigation/{investigation_id}/pdf"
                        ) as report_response:
                            if report_response.status == 200:
                                report_data = await report_response.json()
                                logger.info(f"Report generation successful: {report_data}")
                                self.test_results.append(("Report Generation", "PASS", "PDF report generation started"))
                                return True
                            else:
                                logger.error(f"Report generation failed: {report_response.status}")
                                self.test_results.append(("Report Generation", "FAIL", f"Status: {report_response.status}"))
                                return False
                    else:
                        logger.error(f"Investigation creation failed: {response.status}")
                        self.test_results.append(("Report Generation", "FAIL", f"Investigation creation failed: {response.status}"))
                        return False
        except Exception as e:
            logger.error(f"Report generation test failed: {e}")
            self.test_results.append(("Report Generation", "FAIL", str(e)))
            return False
    
    async def test_settings_api(self) -> bool:
        """Test settings API functionality"""
        logger.info("Testing settings API...")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test getting settings
                async with session.get(f"{self.base_url}/api/v1/settings") as response:
                    if response.status == 200:
                        settings = await response.json()
                        logger.info("Settings API working")
                        
                        # Test updating settings
                        test_settings = {
                            "enableUserAgentRotation": True,
                            "enableProxyRotation": False,
                            "enableRandomDelays": True,
                            "defaultDelayMin": 2,
                            "defaultDelayMax": 5,
                            "maxRetries": 3,
                            "timeoutSeconds": 30
                        }
                        
                        async with session.put(
                            f"{self.base_url}/api/v1/settings/scraping",
                            json=test_settings
                        ) as update_response:
                            if update_response.status == 200:
                                logger.info("Settings update successful")
                                self.test_results.append(("Settings API", "PASS", "Settings API working"))
                                return True
                            else:
                                logger.error(f"Settings update failed: {update_response.status}")
                                self.test_results.append(("Settings API", "FAIL", f"Update failed: {update_response.status}"))
                                return False
                    else:
                        logger.error(f"Settings API failed: {response.status}")
                        self.test_results.append(("Settings API", "FAIL", f"Status: {response.status}"))
                        return False
        except Exception as e:
            logger.error(f"Settings API test failed: {e}")
            self.test_results.append(("Settings API", "FAIL", str(e)))
            return False
    
    def print_results(self):
        """Print test results summary"""
        logger.info("\n" + "="*60)
        logger.info("TEST RESULTS SUMMARY")
        logger.info("="*60)
        
        passed = 0
        failed = 0
        
        for test_name, status, message in self.test_results:
            status_icon = "✅" if status == "PASS" else "❌"
            logger.info(f"{status_icon} {test_name}: {message}")
            if status == "PASS":
                passed += 1
            else:
                failed += 1
        
        logger.info("="*60)
        logger.info(f"Total Tests: {len(self.test_results)}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        logger.info("="*60)
        
        return failed == 0
    
    async def run_all_tests(self):
        """Run all platform tests"""
        logger.info("Starting comprehensive platform testing...")
        
        # Test API health first
        if not await self.test_api_health():
            logger.error("API health check failed. Make sure the backend is running.")
            return False
        
        # Run all tests
        tests = [
            self.test_social_media_scraping,
            self.test_github_scraping,
            self.test_domain_analysis,
            self.test_threat_analysis,
            self.test_report_generation,
            self.test_settings_api
        ]
        
        for test in tests:
            try:
                await test()
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                logger.error(f"Test failed with exception: {e}")
        
        # Print results
        return self.print_results()

async def main():
    """Main test function"""
    tester = PlatformTester()
    success = await tester.run_all_tests()
    
    if success:
        logger.info("🎉 All tests passed! Platform is working correctly.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 