#!/usr/bin/env python3

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.domain_analyzer import DomainAnalyzer

async def test_domain_analyzer():
    """Test the domain analyzer"""
    try:
        print("Testing domain analyzer...")
        analyzer = DomainAnalyzer()
        result = await analyzer.analyze_domain('example.com')
        print("Domain analysis result:", result)
        return result
    except Exception as e:
        print(f"Error testing domain analyzer: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_domain_analyzer())
    print("Test completed") 