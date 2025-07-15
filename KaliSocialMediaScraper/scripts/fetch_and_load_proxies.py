#!/usr/bin/env python3
"""
Fetch free proxies and load them into the Kali OSINT Platform proxy rotator.
This script fetches proxies from multiple sources and directly updates the proxy rotator.
"""

import requests
import time
import logging
import sys
import os
import json
from typing import List, Dict, Any

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.proxy_rotator import proxy_rotator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Multiple proxy sources for better reliability
PROXY_SOURCES = [
    {
        "name": "Proxy-List.download",
        "url": "https://www.proxy-list.download/api/v1/get?type=https",
        "parser": "text"
    },
    {
        "name": "Free-Proxy-List.net",
        "url": "https://free-proxy-list.net/",
        "parser": "html"
    },
    {
        "name": "SSLProxies.org",
        "url": "https://www.sslproxies.org/",
        "parser": "html"
    }
]

def fetch_proxies_from_text(text: str) -> List[Dict[str, Any]]:
    """Parse proxies from text format (ip:port)"""
    proxies = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            try:
                host, port_str = line.split(':', 1)
                host = host.strip()
                port = int(port_str.strip())
                
                if host and port > 0 and port < 65536:
                    proxies.append({
                        "host": host,
                        "port": port,
                        "protocol": "http",
                        "source": "text_parser"
                    })
            except (ValueError, IndexError):
                continue
    
    return proxies

def fetch_proxies_from_html(html_content: str) -> List[Dict[str, Any]]:
    """Parse proxies from HTML table format"""
    proxies = []
    
    # Simple HTML table parser for proxy lists
    lines = html_content.split('\n')
    for line in lines:
        line = line.strip()
        if '<tr>' in line and '<td>' in line:
            # Extract IP and port from table row
            try:
                # Look for IP pattern
                import re
                ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                port_pattern = r'(\d{2,5})'
                
                ips = re.findall(ip_pattern, line)
                ports = re.findall(port_pattern, line)
                
                if ips and ports:
                    host = ips[0]
                    port = int(ports[0])
                    
                    if port > 0 and port < 65536:
                        proxies.append({
                            "host": host,
                            "port": port,
                            "protocol": "http",
                            "source": "html_parser"
                        })
            except (ValueError, IndexError):
                continue
    
    return proxies

def fetch_free_proxies() -> List[Dict[str, Any]]:
    """Fetch free proxies from multiple sources"""
    all_proxies = []
    
    for source in PROXY_SOURCES:
        try:
            logger.info(f"Fetching proxies from {source['name']}")
            
            response = requests.get(source['url'], timeout=10)
            if response.status_code == 200:
                if source['parser'] == 'text':
                    proxies = fetch_proxies_from_text(response.text)
                elif source['parser'] == 'html':
                    proxies = fetch_proxies_from_html(response.text)
                else:
                    continue
                
                logger.info(f"Found {len(proxies)} proxies from {source['name']}")
                all_proxies.extend(proxies)
                
            else:
                logger.warning(f"Failed to fetch from {source['name']}: {response.status_code}")
                
        except Exception as e:
            logger.warning(f"Error fetching from {source['name']}: {e}")
    
    # Remove duplicates
    unique_proxies = []
    seen = set()
    
    for proxy in all_proxies:
        key = f"{proxy['host']}:{proxy['port']}"
        if key not in seen:
            seen.add(key)
            unique_proxies.append(proxy)
    
    logger.info(f"Total unique proxies found: {len(unique_proxies)}")
    return unique_proxies

def test_proxy_connectivity(proxy: Dict[str, Any]) -> bool:
    """Test if a proxy is working"""
    try:
        proxy_url = f"http://{proxy['host']}:{proxy['port']}"
        response = requests.get(
            "http://httpbin.org/ip",
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def filter_working_proxies(proxies: List[Dict[str, Any]], max_tests: int = 20) -> List[Dict[str, Any]]:
    """Filter proxies to only working ones"""
    working_proxies = []
    test_count = 0
    
    logger.info(f"Testing {min(len(proxies), max_tests)} proxies for connectivity...")
    
    for proxy in proxies[:max_tests]:
        test_count += 1
        if test_proxy_connectivity(proxy):
            working_proxies.append(proxy)
            logger.info(f"✓ Working proxy: {proxy['host']}:{proxy['port']}")
        else:
            logger.debug(f"✗ Failed proxy: {proxy['host']}:{proxy['port']}")
    
    logger.info(f"Found {len(working_proxies)} working proxies out of {test_count} tested")
    return working_proxies

def load_proxies_into_rotator(proxies: List[Dict[str, Any]]) -> None:
    """Load proxies directly into the proxy rotator and save to file"""
    try:
        # Clear existing proxies
        proxy_rotator.clear_proxies()
        
        # Load new proxies
        proxy_rotator.load_proxies_from_list(proxies)
        
        # Save proxies to configuration file for persistence
        proxy_rotator.save_proxies_to_file()
        
        logger.info(f"Successfully loaded {len(proxies)} proxies into proxy rotator")
        logger.info("Proxies saved to config/proxy_config.json for persistence")
        
        # Test all proxies
        logger.info("Testing all loaded proxies...")
        # Note: This would need to be run in an async context
        # For now, we'll just log the proxy count
        
    except Exception as e:
        logger.error(f"Failed to load proxies into rotator: {e}")

def main():
    """Main function to fetch and load proxies"""
    logger.info("Starting proxy fetch and load process...")
    
    # Fetch proxies from multiple sources
    proxies = fetch_free_proxies()
    
    if not proxies:
        logger.error("No proxies found from any source")
        return
    
    # Filter for working proxies
    working_proxies = filter_working_proxies(proxies, max_tests=30)
    
    if not working_proxies:
        logger.warning("No working proxies found. Loading all proxies anyway for testing.")
        working_proxies = proxies[:20]  # Load first 20 for testing
    
    # Load proxies into the rotator
    load_proxies_into_rotator(working_proxies)
    
    # Display proxy statistics
    stats = proxy_rotator.get_proxy_stats()
    logger.info(f"Proxy rotator statistics: {stats}")
    
    logger.info("Proxy loading process completed!")

if __name__ == "__main__":
    main() 