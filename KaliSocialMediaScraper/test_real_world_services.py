#!/usr/bin/env python3
"""
Real-world service functionality test
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_domain_analyzer():
    """Test domain analyzer with real data"""
    print("🔍 Testing Domain Analyzer...")
    try:
        from app.services.domain_analyzer import DomainAnalyzer
        
        async with DomainAnalyzer() as analyzer:
            # Test with a real domain
            result = await analyzer.analyze_domain("google.com")
            
            if "error" in result:
                print(f"❌ Domain analyzer error: {result['error']}")
                return False
            
            print(f"✅ Domain analyzer working - analyzed {result.get('domain', 'unknown')}")
            print(f"   - DNS records: {len(result.get('dns', {}))}")
            print(f"   - Risk score: {result.get('risk_score', 0)}")
            return True
            
    except Exception as e:
        print(f"❌ Domain analyzer failed: {e}")
        return False

async def test_github_scraper():
    """Test GitHub scraper with real data"""
    print("🐙 Testing GitHub Scraper...")
    try:
        from app.services.github_scraper import GitHubScraper
        
        async with GitHubScraper() as scraper:
            # Test with a real GitHub user
            result = await scraper.analyze_user_profile("torvalds")
            
            if "error" in result:
                print(f"❌ GitHub scraper error: {result['error']}")
                return False
            
            print(f"✅ GitHub scraper working - analyzed user: {result.get('user', {}).get('login', 'unknown')}")
            print(f"   - Repositories: {len(result.get('repositories', []))}")
            print(f"   - Threat level: {result.get('threat_assessment', {}).get('threat_level', 'unknown')}")
            return True
            
    except Exception as e:
        print(f"❌ GitHub scraper failed: {e}")
        return False

async def test_social_media_scraper():
    """Test social media scraper with real data"""
    print("📱 Testing Social Media Scraper...")
    try:
        from app.services.social_media_scraper import SocialMediaScraper
        from app.models.schemas import PlatformType
        
        async with SocialMediaScraper() as scraper:
            # Test with a real platform (GitHub as it's most reliable)
            result = await scraper.scrape_platform(
                PlatformType.GITHUB,
                "torvalds",
                include_metadata=True,
                max_posts=10
            )
            
            if "error" in result:
                print(f"❌ Social media scraper error: {result['error']}")
                return False
            
            print(f"✅ Social media scraper working - analyzed platform: GitHub")
            print(f"   - Profile data: {'profile' in result}")
            print(f"   - Threat level: {result.get('threat_level', 'unknown')}")
            return True
            
    except Exception as e:
        print(f"❌ Social media scraper failed: {e}")
        return False

async def test_threat_analyzer():
    """Test threat analyzer with real data"""
    print("⚠️ Testing Threat Analyzer...")
    try:
        from app.services.threat_analyzer import ThreatAnalyzer
        
        analyzer = ThreatAnalyzer()
        
        # Test with a sample target
        result = await analyzer.analyze_threat("test-target", "comprehensive")
        
        if not result:
            print("❌ Threat analyzer returned no result")
            return False
        
        print(f"✅ Threat analyzer working")
        print(f"   - Threat level: {result.threat_level}")
        print(f"   - Threat score: {result.threat_score}")
        print(f"   - Confidence: {result.confidence}")
        return True
        
    except Exception as e:
        print(f"❌ Threat analyzer failed: {e}")
        return False

async def test_proxy_rotator():
    """Test proxy rotator functionality"""
    print("🔄 Testing Proxy Rotator...")
    try:
        from app.services.proxy_rotator import ProxyRotator
        
        rotator = ProxyRotator()
        
        # Test proxy functionality
        proxy = await rotator.get_next_proxy()
        
        if proxy:
            print(f"✅ Proxy rotator working - found proxy: {proxy.host}:{proxy.port}")
        else:
            print("⚠️ No proxies available (this is normal for testing)")
        
        # Test session creation
        session = await rotator.create_session_with_proxy()
        if session:
            print("✅ Proxy session creation working")
            await session.close()
        else:
            print("⚠️ No proxy session available (this is normal for testing)")
        
        return True
        
    except Exception as e:
        print(f"❌ Proxy rotator failed: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoints"""
    print("🌐 Testing API Endpoints...")
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints failed: {e}")
        return False

async def test_database_connection():
    """Test database connection"""
    print("🗄️ Testing Database Connection...")
    try:
        from app.core.database import engine
        from sqlalchemy import text
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("✅ Database connection working")
                return True
            else:
                print("❌ Database connection failed")
                return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def main():
    """Run all service tests"""
    print("🚀 Starting Real-World Service Tests")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("API Endpoints", test_api_endpoints),
        ("Domain Analyzer", test_domain_analyzer),
        ("GitHub Scraper", test_github_scraper),
        ("Social Media Scraper", test_social_media_scraper),
        ("Threat Analyzer", test_threat_analyzer),
        ("Proxy Rotator", test_proxy_rotator),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All services are ready for real-world data!")
    elif passed >= total * 0.7:
        print("⚠️ Most services are ready, but some need attention")
    else:
        print("❌ Many services need configuration or fixes")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main()) 