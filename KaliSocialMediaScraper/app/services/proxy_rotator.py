"""
Proxy Rotation Service for OSINT Platform
"""

import asyncio
import aiohttp
import logging
import random
import time
import os
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class ProxyConfig:
    """Proxy configuration"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"
    country: Optional[str] = None
    last_used: Optional[datetime] = None
    success_count: int = 0
    failure_count: int = 0
    is_active: bool = True

class ProxyRotator:
    """Advanced proxy rotation service for OSINT operations"""
    
    def __init__(self):
        self.proxies: List[ProxyConfig] = []
        self.current_proxy_index = 0
        self.proxy_rotation_interval = 10  # seconds
        self.last_rotation = datetime.now()
        self.proxy_test_url = "http://httpbin.org/ip"
        self.max_failures = 3
        self.min_success_rate = 0.7
        
        # Initialize with common proxy providers
        self._initialize_proxy_pool()
    
    def _initialize_proxy_pool(self):
        """Initialize proxy pool with various sources"""
        # Free proxy list (for testing - replace with paid services in production)
        free_proxies = [
            # Add your proxy list here
            # Example: ProxyConfig("proxy1.example.com", 8080, "user", "pass"),
        ]
        
        # Load from environment variables
        proxy_host = os.getenv("PROXY_HOST")
        proxy_port = os.getenv("PROXY_PORT")
        proxy_user = os.getenv("PROXY_USER")
        proxy_pass = os.getenv("PROXY_PASS")
        
        if proxy_host and proxy_port:
            self.proxies.append(ProxyConfig(
                host=proxy_host,
                port=int(proxy_port),
                username=proxy_user,
                password=proxy_pass
            ))
        
        # Load from proxy configuration file
        self._load_proxies_from_file()
        
        # Add free proxies
        self.proxies.extend(free_proxies)
        
        logger.info(f"Initialized proxy pool with {len(self.proxies)} proxies")
    
    def _load_proxies_from_file(self):
        """Load proxies from configuration file"""
        proxy_file = "config/proxy_config.json"
        if os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r') as f:
                    proxy_data = json.load(f)
                
                for proxy_info in proxy_data.get("proxies", []):
                    self.add_proxy(
                        host=proxy_info["host"],
                        port=proxy_info["port"],
                        username=proxy_info.get("username"),
                        password=proxy_info.get("password"),
                        protocol=proxy_info.get("protocol", "http"),
                        country=proxy_info.get("country")
                    )
                
                logger.info(f"Loaded {len(proxy_data.get('proxies', []))} proxies from {proxy_file}")
            except Exception as e:
                logger.warning(f"Failed to load proxies from {proxy_file}: {e}")
    
    def save_proxies_to_file(self):
        """Save current proxy list to configuration file"""
        proxy_file = "config/proxy_config.json"
        try:
            proxy_data = {
                "proxies": self.get_proxy_list(),
                "last_updated": datetime.now().isoformat()
            }
            
            with open(proxy_file, 'w') as f:
                json.dump(proxy_data, f, indent=2)
            
            logger.info(f"Saved {len(self.proxies)} proxies to {proxy_file}")
        except Exception as e:
            logger.error(f"Failed to save proxies to {proxy_file}: {e}")
    
    async def get_next_proxy(self) -> Optional[ProxyConfig]:
        """Get next available proxy with rotation"""
        if not self.proxies:
            logger.warning("No proxies available")
            return None
        
        # Check if we need to rotate
        if (datetime.now() - self.last_rotation).seconds > self.proxy_rotation_interval:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            self.last_rotation = datetime.now()
        
        # Find active proxy
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_proxy_index]
            
            # Skip failed proxies
            if proxy.failure_count >= self.max_failures:
                self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
                attempts += 1
                continue
            
            # Check success rate
            total_requests = proxy.success_count + proxy.failure_count
            if total_requests > 0:
                success_rate = proxy.success_count / total_requests
                if success_rate < self.min_success_rate:
                    self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
                    attempts += 1
                    continue
            
            proxy.last_used = datetime.now()
            return proxy
        
        logger.warning("No working proxies available")
        return None
    
    async def test_proxy(self, proxy: ProxyConfig) -> bool:
        """Test if proxy is working"""
        try:
            proxy_url = f"{proxy.protocol}://"
            if proxy.username and proxy.password:
                proxy_url += f"{proxy.username}:{proxy.password}@"
            proxy_url += f"{proxy.host}:{proxy.port}"
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    self.proxy_test_url,
                    proxy=proxy_url,
                    headers={"User-Agent": "Kali-OSINT-Platform/1.0"}
                ) as response:
                    if response.status == 200:
                        proxy.success_count += 1
                        return True
                    else:
                        proxy.failure_count += 1
                        return False
                        
        except Exception as e:
            logger.debug(f"Proxy test failed for {proxy.host}:{proxy.port}: {e}")
            proxy.failure_count += 1
            return False
    
    async def test_all_proxies(self):
        """Test all proxies and mark inactive ones"""
        logger.info("Testing all proxies...")
        
        for proxy in self.proxies:
            if proxy.is_active:
                is_working = await self.test_proxy(proxy)
                if not is_working:
                    proxy.is_active = False
                    logger.warning(f"Proxy {proxy.host}:{proxy.port} marked as inactive")
        
        active_count = sum(1 for p in self.proxies if p.is_active)
        logger.info(f"Proxy test complete. {active_count}/{len(self.proxies)} proxies active")
    
    def get_proxy_url(self, proxy: ProxyConfig) -> str:
        """Get proxy URL for aiohttp"""
        if proxy.username and proxy.password:
            return f"{proxy.protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}"
        else:
            return f"{proxy.protocol}://{proxy.host}:{proxy.port}"
    
    async def create_session_with_proxy(self) -> Optional[aiohttp.ClientSession]:
        """Create aiohttp session with rotating proxy"""
        proxy = await self.get_next_proxy()
        if not proxy:
            return None
        
        headers = {
            "User-Agent": "Kali-OSINT-Platform/1.0",
            "Accept": "application/json, text/html, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        
        session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
            connector=connector
        )
        
        # Store proxy info for later use
        session._proxy_config = proxy
        
        return session
    
    async def mark_proxy_success(self, session: aiohttp.ClientSession):
        """Mark proxy as successful"""
        if hasattr(session, '_proxy_config'):
            session._proxy_config.success_count += 1
    
    async def mark_proxy_failure(self, session: aiohttp.ClientSession):
        """Mark proxy as failed"""
        if hasattr(session, '_proxy_config'):
            session._proxy_config.failure_count += 1
    
    def get_proxy_stats(self) -> Dict[str, Any]:
        """Get proxy statistics"""
        total_proxies = len(self.proxies)
        active_proxies = sum(1 for p in self.proxies if p.is_active)
        total_requests = sum(p.success_count + p.failure_count for p in self.proxies)
        total_success = sum(p.success_count for p in self.proxies)
        
        return {
            "total_proxies": total_proxies,
            "active_proxies": active_proxies,
            "total_requests": total_requests,
            "success_rate": total_success / total_requests if total_requests > 0 else 0,
            "current_proxy": self.current_proxy_index,
            "last_rotation": self.last_rotation.isoformat()
        }
    
    def add_proxy(self, host: str, port: int, username: Optional[str] = None, 
                  password: Optional[str] = None, protocol: str = "http", 
                  country: Optional[str] = None) -> None:
        """Add a new proxy to the pool"""
        proxy = ProxyConfig(
            host=host,
            port=port,
            username=username,
            password=password,
            protocol=protocol,
            country=country
        )
        self.proxies.append(proxy)
        logger.info(f"Added proxy: {host}:{port}")
    
    def load_proxies_from_list(self, proxy_list: List[Dict[str, Any]]) -> None:
        """Load proxies from a list of dictionaries"""
        added_count = 0
        for proxy_data in proxy_list:
            try:
                host = proxy_data.get("host") or proxy_data.get("ip")
                port = proxy_data.get("port")
                username = proxy_data.get("username")
                password = proxy_data.get("password")
                protocol = proxy_data.get("protocol", "http")
                country = proxy_data.get("country")
                
                if host and port:
                    self.add_proxy(
                        host=host,
                        port=int(port),
                        username=username,
                        password=password,
                        protocol=protocol,
                        country=country
                    )
                    added_count += 1
            except Exception as e:
                logger.warning(f"Failed to add proxy {proxy_data}: {e}")
        
        logger.info(f"Loaded {added_count} proxies from list")
    
    def clear_proxies(self) -> None:
        """Clear all proxies from the pool"""
        self.proxies.clear()
        self.current_proxy_index = 0
        logger.info("Cleared all proxies from pool")
    
    def get_proxy_list(self) -> List[Dict[str, Any]]:
        """Get list of all proxies as dictionaries"""
        return [
            {
                "host": proxy.host,
                "port": proxy.port,
                "username": proxy.username,
                "password": proxy.password,
                "protocol": proxy.protocol,
                "country": proxy.country,
                "is_active": proxy.is_active,
                "success_count": proxy.success_count,
                "failure_count": proxy.failure_count,
                "last_used": proxy.last_used.isoformat() if proxy.last_used else None
            }
            for proxy in self.proxies
        ]
    
    async def get_proxy(self, *args, **kwargs) -> Optional[ProxyConfig]:
        """Get next available proxy (alias for get_next_proxy)"""
        return await self.get_next_proxy()
    
    async def test_proxy_connection(self, proxy: ProxyConfig, *args, **kwargs) -> bool:
        """Test proxy connection (alias for test_proxy)"""
        return await self.test_proxy(proxy)

# Global proxy rotator instance
proxy_rotator = ProxyRotator() 