#!/usr/bin/env python3
"""
Comprehensive functionality test for Kali OSINT Social Media Scraper Platform
Tests all major features and endpoints to ensure everything is working correctly.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test backend health and basic connectivity"""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_frontend_health():
    """Test frontend health"""
    print("🔍 Testing Frontend Health...")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend health check failed: {e}")
        return False

def test_investigation_endpoints():
    """Test investigation creation and management"""
    print("🔍 Testing Investigation Endpoints...")
    
    # Test creating an investigation
    investigation_data = {
        "title": "Test Investigation",
        "target_type": "DOMAIN",
        "target_value": "example.com",
        "analysis_options": {
            "include_network_analysis": True,
            "include_threat_assessment": True
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/investigations", json=investigation_data)
        if response.status_code == 200:
            investigation = response.json()
            print(f"✅ Investigation created: {investigation['id']}")
            
            # Test getting investigations list
            response = requests.get(f"{BASE_URL}/api/v1/investigations")
            if response.status_code == 200:
                investigations = response.json()
                print(f"✅ Investigations list retrieved: {len(investigations)} investigations")
                return True
            else:
                print(f"❌ Failed to get investigations list: {response.status_code}")
                return False
        else:
            print(f"❌ Failed to create investigation: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Investigation test failed: {e}")
        return False

def test_analysis_endpoints():
    """Test analysis endpoints"""
    print("🔍 Testing Analysis Endpoints...")
    
    # Test threat analysis
    try:
        response = requests.post(f"{BASE_URL}/api/v1/analysis/run", 
                               json={"type": "threat", "target": "example.com"})
        if response.status_code == 200:
            result = response.json()
            print("✅ Threat analysis completed")
        else:
            print(f"❌ Threat analysis failed: {response.status_code}")
            return False
            
        # Test network analysis
        response = requests.get(f"{BASE_URL}/api/v1/analysis/network-graph/summary")
        if response.status_code == 200:
            print("✅ Network analysis endpoint working")
        else:
            print(f"❌ Network analysis failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_social_media_endpoints():
    """Test social media scraping endpoints"""
    print("🔍 Testing Social Media Endpoints...")
    
    try:
        # Test platforms list
        response = requests.get(f"{BASE_URL}/api/v1/social-media/platforms")
        if response.status_code == 200:
            platforms = response.json()
            print(f"✅ Social media platforms retrieved: {len(platforms['platforms'])} platforms")
        else:
            print(f"❌ Failed to get platforms: {response.status_code}")
            return False
            
        # Test profile analysis
        response = requests.post(f"{BASE_URL}/api/v1/social-media/analyze",
                               json={"platform": "github", "username": "test"})
        if response.status_code == 200:
            print("✅ Profile analysis completed")
        else:
            print(f"❌ Profile analysis failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Social media test failed: {e}")
        return False

def test_dashboard_endpoints():
    """Test dashboard endpoints"""
    print("🔍 Testing Dashboard Endpoints...")
    
    try:
        # Test dashboard stats
        response = requests.get(f"{BASE_URL}/api/v1/dashboard/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Dashboard stats retrieved: {stats['total_investigations']} investigations")
        else:
            print(f"❌ Dashboard stats failed: {response.status_code}")
            return False
            
        # Test recent activity
        response = requests.get(f"{BASE_URL}/api/v1/dashboard/activity")
        if response.status_code == 200:
            activity = response.json()
            print(f"✅ Recent activity retrieved: {len(activity['activity'])} activities")
        else:
            print(f"❌ Recent activity failed: {response.status_code}")
            return False
            
        # Test real-time data
        response = requests.get(f"{BASE_URL}/api/v1/dashboard/real-time")
        if response.status_code == 200:
            realtime = response.json()
            print("✅ Real-time data retrieved")
        else:
            print(f"❌ Real-time data failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_report_endpoints():
    """Test report generation endpoints"""
    print("🔍 Testing Report Endpoints...")
    
    try:
        # Test report generation
        response = requests.post(f"{BASE_URL}/api/v1/exports/report",
                               json={"investigation_id": 1, "report_type": "pdf"})
        if response.status_code == 200:
            report = response.json()
            print(f"✅ Report generated: {report['id']}")
        else:
            print(f"❌ Report generation failed: {response.status_code}")
            return False
            
        # Test reports list
        response = requests.get(f"{BASE_URL}/api/v1/exports/reports")
        if response.status_code == 200:
            reports = response.json()
            print(f"✅ Reports list retrieved: {len(reports)} reports")
        else:
            print(f"❌ Reports list failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Report test failed: {e}")
        return False

def test_intelligence_endpoints():
    """Test intelligence endpoints"""
    print("🔍 Testing Intelligence Endpoints...")
    
    try:
        # Test threat intelligence
        response = requests.get(f"{BASE_URL}/api/v1/intelligence/threats")
        if response.status_code == 200:
            threats = response.json()
            print("✅ Threat intelligence retrieved")
        else:
            print(f"❌ Threat intelligence failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Intelligence test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide a comprehensive report"""
    print("🚀 Starting Comprehensive Platform Test")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend Health", test_frontend_health),
        ("Investigation Endpoints", test_investigation_endpoints),
        ("Analysis Endpoints", test_analysis_endpoints),
        ("Social Media Endpoints", test_social_media_endpoints),
        ("Dashboard Endpoints", test_dashboard_endpoints),
        ("Report Endpoints", test_report_endpoints),
        ("Intelligence Endpoints", test_intelligence_endpoints),
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            success = test_func()
            results[test_name] = success
            if success:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Print comprehensive results
    print("\n" + "=" * 50)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 50)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Platform is fully operational.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    run_comprehensive_test() 