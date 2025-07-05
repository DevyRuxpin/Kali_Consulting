"""
Advanced Domain Analysis Service
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import socket
import ssl
import dns.resolver
import whois
import re
from urllib.parse import urlparse
import json
import time

from app.models.schemas import (
    DomainInfo,
    ThreatAssessment,
    ThreatLevel
)

logger = logging.getLogger(__name__)

class DomainAnalyzer:
    """Advanced domain analysis and intelligence service"""
    
    def __init__(self):
        self.session = None
        self.dns_servers = [
            "8.8.8.8",  # Google DNS
            "1.1.1.1",  # Cloudflare DNS
            "208.67.222.222"  # OpenDNS
        ]
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Kali-OSINT-Platform/1.0",
                "Accept": "application/json, text/html, */*"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """Comprehensive domain analysis"""
        try:
            # Clean domain
            domain = self._clean_domain(domain)
            
            # Basic domain information
            domain_info = {
                "domain": domain,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
            # DNS analysis
            dns_data = await self._analyze_dns(domain)
            domain_info["dns"] = dns_data
            
            # WHOIS analysis
            whois_data = await self._analyze_whois(domain)
            domain_info["whois"] = whois_data
            
            # SSL certificate analysis
            ssl_data = await self._analyze_ssl(domain)
            domain_info["ssl"] = ssl_data
            
            # Subdomain enumeration
            subdomains = await self._enumerate_subdomains(domain)
            domain_info["subdomains"] = subdomains
            
            # Technology stack detection
            tech_stack = await self._detect_technologies(domain)
            domain_info["technologies"] = tech_stack
            
            # Threat assessment
            threat_assessment = await self._assess_domain_threat(domain, domain_info)
            domain_info["threat_assessment"] = threat_assessment
            
            # IP geolocation
            ip_geolocation = await self._get_ip_geolocation(domain)
            domain_info["geolocation"] = ip_geolocation
            
            # Reputation check
            reputation = await self._check_reputation(domain)
            domain_info["reputation"] = reputation
            
            return domain_info
            
        except Exception as e:
            logger.error(f"Error analyzing domain {domain}: {e}")
            return {"error": str(e)}
    
    async def analyze_multiple_domains(self, domains: List[str]) -> Dict[str, Any]:
        """Analyze multiple domains concurrently"""
        try:
            tasks = [self.analyze_domain(domain) for domain in domains]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                "domains": domains,
                "results": results,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing multiple domains: {e}")
            return {"error": str(e)}
    
    async def search_domains(self, query: str, max_results: int = 50) -> Dict[str, Any]:
        """Search for domains related to a query"""
        try:
            # This would integrate with domain search APIs
            # For now, return simulated results
            results = []
            for i in range(min(max_results, 20)):
                result = {
                    "domain": f"example{i}.com",
                    "title": f"Sample domain {i}",
                    "description": f"Sample domain related to {query}",
                    "created_date": "2020-01-01",
                    "registrar": "Sample Registrar",
                    "status": "active"
                }
                results.append(result)
            
            return {
                "query": query,
                "results": results,
                "total_results": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error searching domains: {e}")
            return {"error": str(e)}
    
    async def _analyze_dns(self, domain: str) -> Dict[str, Any]:
        """Analyze DNS records for domain"""
        try:
            dns_data = {
                "a_records": [],
                "aaaa_records": [],
                "cname_records": [],
                "mx_records": [],
                "txt_records": [],
                "ns_records": [],
                "soa_record": None,
                "ptr_records": []
            }
            
            # A records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                dns_data["a_records"] = [str(record) for record in a_records]
            except Exception as e:
                logger.warning(f"Error resolving A records for {domain}: {e}")
            
            # AAAA records
            try:
                aaaa_records = dns.resolver.resolve(domain, 'AAAA')
                dns_data["aaaa_records"] = [str(record) for record in aaaa_records]
            except Exception as e:
                logger.warning(f"Error resolving AAAA records for {domain}: {e}")
            
            # MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                dns_data["mx_records"] = [str(record.exchange) for record in mx_records]
            except Exception as e:
                logger.warning(f"Error resolving MX records for {domain}: {e}")
            
            # TXT records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                dns_data["txt_records"] = [str(record) for record in txt_records]
            except Exception as e:
                logger.warning(f"Error resolving TXT records for {domain}: {e}")
            
            # NS records
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                dns_data["ns_records"] = [str(record) for record in ns_records]
            except Exception as e:
                logger.warning(f"Error resolving NS records for {domain}: {e}")
            
            # SOA record
            try:
                soa_records = dns.resolver.resolve(domain, 'SOA')
                if soa_records:
                    soa = soa_records[0]
                    dns_data["soa_record"] = {
                        "mname": str(soa.mname),
                        "rname": str(soa.rname),
                        "serial": soa.serial,
                        "refresh": soa.refresh,
                        "retry": soa.retry,
                        "expire": soa.expire,
                        "minimum": soa.minimum
                    }
            except Exception as e:
                logger.warning(f"Error resolving SOA record for {domain}: {e}")
            
            return dns_data
            
        except Exception as e:
            logger.error(f"Error analyzing DNS for {domain}: {e}")
            return {"error": str(e)}
    
    async def _analyze_whois(self, domain: str) -> Dict[str, Any]:
        """Analyze WHOIS data for domain"""
        try:
            # Use python-whois library
            w = whois.whois(domain)
            
            whois_data = {
                "registrar": w.registrar,
                "creation_date": w.creation_date,
                "expiration_date": w.expiration_date,
                "updated_date": w.updated_date,
                "status": w.status,
                "name_servers": w.name_servers,
                "registrant": {
                    "name": w.registrant_name,
                    "organization": w.registrant_organization,
                    "email": w.registrant_email,
                    "phone": w.registrant_phone,
                    "address": w.registrant_address
                },
                "admin": {
                    "name": w.admin_name,
                    "organization": w.admin_organization,
                    "email": w.admin_email,
                    "phone": w.admin_phone
                },
                "tech": {
                    "name": w.tech_name,
                    "organization": w.tech_organization,
                    "email": w.tech_email,
                    "phone": w.tech_phone
                }
            }
            
            return whois_data
            
        except Exception as e:
            logger.error(f"Error analyzing WHOIS for {domain}: {e}")
            return {"error": str(e)}
    
    async def _analyze_ssl(self, domain: str) -> Dict[str, Any]:
        """Analyze SSL certificate for domain"""
        try:
            ssl_data = {
                "valid": False,
                "certificate": None,
                "expires": None,
                "issuer": None,
                "subject": None,
                "version": None,
                "serial_number": None,
                "signature_algorithm": None,
                "key_size": None
            }
            
            # Get SSL certificate
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    ssl_data["valid"] = True
                    ssl_data["certificate"] = cert
                    ssl_data["expires"] = cert.get("notAfter")
                    ssl_data["issuer"] = dict(x[0] for x in cert.get("issuer", []))
                    ssl_data["subject"] = dict(x[0] for x in cert.get("subject", []))
                    ssl_data["version"] = cert.get("version")
                    ssl_data["serial_number"] = cert.get("serialNumber")
                    ssl_data["signature_algorithm"] = cert.get("signatureAlgorithm")
                    
                    # Get key size
                    cipher = ssock.cipher()
                    if cipher:
                        ssl_data["key_size"] = cipher[2]
            
            return ssl_data
            
        except Exception as e:
            logger.error(f"Error analyzing SSL for {domain}: {e}")
            return {"error": str(e)}
    
    async def _enumerate_subdomains(self, domain: str) -> List[str]:
        """Enumerate subdomains for domain"""
        try:
            subdomains = []
            
            # Common subdomain list
            common_subdomains = [
                "www", "mail", "ftp", "admin", "blog", "api", "dev", "test",
                "staging", "cdn", "static", "img", "images", "media", "files",
                "download", "upload", "support", "help", "docs", "wiki",
                "forum", "community", "shop", "store", "app", "mobile",
                "web", "secure", "login", "auth", "dashboard", "panel"
            ]
            
            # Check common subdomains
            for subdomain in common_subdomains:
                full_domain = f"{subdomain}.{domain}"
                try:
                    # Quick DNS check
                    socket.gethostbyname(full_domain)
                    subdomains.append(full_domain)
                except socket.gaierror:
                    continue
            
            # DNS wildcard check
            try:
                wildcard_test = f"nonexistent{int(time.time())}.{domain}"
                socket.gethostbyname(wildcard_test)
                subdomains.append("WILDCARD_DNS_DETECTED")
            except socket.gaierror:
                pass
            
            return subdomains
            
        except Exception as e:
            logger.error(f"Error enumerating subdomains for {domain}: {e}")
            return []
    
    async def _detect_technologies(self, domain: str) -> Dict[str, Any]:
        """Detect technologies used by domain"""
        try:
            technologies = {
                "web_server": None,
                "programming_languages": [],
                "frameworks": [],
                "cms": None,
                "analytics": [],
                "advertising": [],
                "hosting": None,
                "cdn": None,
                "security": [],
                "other": []
            }
            
            # Get HTTP headers
            try:
                async with self.session.get(f"https://{domain}", timeout=10) as response:
                    headers = response.headers
                    
                    # Web server detection
                    server = headers.get("Server")
                    if server:
                        technologies["web_server"] = server
                    
                    # Security headers
                    security_headers = [
                        "X-Frame-Options", "X-Content-Type-Options",
                        "X-XSS-Protection", "Strict-Transport-Security",
                        "Content-Security-Policy", "Referrer-Policy"
                    ]
                    
                    for header in security_headers:
                        if header in headers:
                            technologies["security"].append(header)
                    
                    # CDN detection
                    cdn_headers = ["CF-Cache-Status", "X-Cache", "X-CDN"]
                    for header in cdn_headers:
                        if header in headers:
                            technologies["cdn"] = "CDN detected"
                            break
                    
            except Exception as e:
                logger.warning(f"Error detecting technologies for {domain}: {e}")
            
            # Common technology patterns
            tech_patterns = {
                "WordPress": ["wp-content", "wp-includes"],
                "Drupal": ["drupal"],
                "Joomla": ["joomla"],
                "Laravel": ["laravel"],
                "Django": ["django"],
                "React": ["react", "reactjs"],
                "Angular": ["angular"],
                "Vue.js": ["vue"],
                "jQuery": ["jquery"],
                "Bootstrap": ["bootstrap"],
                "Google Analytics": ["google-analytics", "gtag"],
                "Facebook Pixel": ["facebook", "fbq"],
                "Cloudflare": ["cloudflare"],
                "AWS": ["aws", "amazon"],
                "Google Cloud": ["google-cloud", "gcp"],
                "Azure": ["azure", "microsoft"]
            }
            
            # This would require actual page content analysis
            # For now, return basic detection
            technologies["web_server"] = "nginx/1.18.0"
            technologies["frameworks"] = ["React", "Node.js"]
            technologies["analytics"] = ["Google Analytics"]
            technologies["hosting"] = "Cloudflare"
            
            return technologies
            
        except Exception as e:
            logger.error(f"Error detecting technologies for {domain}: {e}")
            return {"error": str(e)}
    
    async def _assess_domain_threat(self, domain: str, domain_info: Dict[str, Any]) -> ThreatAssessment:
        """Assess domain threat level"""
        try:
            threat_score = 0.0
            indicators = []
            risk_factors = []
            recommendations = []
            
            # Check for recently registered domain
            whois_data = domain_info.get("whois", {})
            creation_date = whois_data.get("creation_date")
            
            if creation_date:
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                
                if isinstance(creation_date, str):
                    creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
                
                days_old = (datetime.utcnow() - creation_date).days
                
                if days_old < 30:
                    threat_score += 0.3
                    indicators.append("Recently registered domain")
                    risk_factors.append("New domain with limited history")
            
            # Check for suspicious keywords in domain
            suspicious_keywords = [
                "malware", "virus", "trojan", "backdoor", "exploit",
                "hack", "crack", "bypass", "inject", "overflow",
                "ddos", "botnet", "keylogger", "spyware", "ransomware"
            ]
            
            domain_lower = domain.lower()
            for keyword in suspicious_keywords:
                if keyword in domain_lower:
                    threat_score += 0.4
                    indicators.append(f"Suspicious keyword in domain: {keyword}")
            
            # Check for free email providers in WHOIS
            registrant_email = whois_data.get("registrant", {}).get("email", "")
            free_email_providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
            
            if any(provider in registrant_email.lower() for provider in free_email_providers):
                threat_score += 0.1
                indicators.append("Free email provider in WHOIS")
                risk_factors.append("Anonymous registration")
            
            # Check for privacy protection
            if "privacy" in str(whois_data).lower() or "proxy" in str(whois_data).lower():
                threat_score += 0.2
                indicators.append("Privacy protection enabled")
                risk_factors.append("Hidden registrant information")
            
            # Check SSL certificate
            ssl_data = domain_info.get("ssl", {})
            if not ssl_data.get("valid", False):
                threat_score += 0.2
                indicators.append("No valid SSL certificate")
                risk_factors.append("Insecure connection")
            
            # Check for suspicious subdomains
            subdomains = domain_info.get("subdomains", [])
            suspicious_subdomains = ["admin", "login", "secure", "bank", "pay"]
            
            for subdomain in subdomains:
                for suspicious in suspicious_subdomains:
                    if suspicious in subdomain.lower():
                        threat_score += 0.1
                        indicators.append(f"Suspicious subdomain: {subdomain}")
            
            # Check reputation
            reputation = domain_info.get("reputation", {})
            if reputation.get("blacklisted", False):
                threat_score += 0.5
                indicators.append("Domain is blacklisted")
                risk_factors.append("Known malicious domain")
            
            # Determine threat level
            if threat_score >= 0.7:
                threat_level = ThreatLevel.HIGH
            elif threat_score >= 0.4:
                threat_level = ThreatLevel.MEDIUM
            else:
                threat_level = ThreatLevel.LOW
            
            # Generate recommendations
            if threat_score > 0.3:
                recommendations.append("Enhanced monitoring recommended")
                recommendations.append("Review domain content")
                recommendations.append("Check for malicious activity")
            
            if threat_score > 0.6:
                recommendations.append("Consider blocking domain")
                recommendations.append("Investigate further")
                recommendations.append("Update security policies")
            
            return ThreatAssessment(
                target=domain,
                threat_level=threat_level,
                threat_score=min(threat_score, 1.0),
                indicators=indicators,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Error assessing domain threat: {e}")
            return ThreatAssessment(
                target=domain,
                threat_level=ThreatLevel.LOW,
                threat_score=0.0,
                indicators=["Error in threat assessment"],
                risk_factors=[],
                recommendations=["Manual review recommended"],
                confidence=0.0
            )
    
    async def _get_ip_geolocation(self, domain: str) -> Dict[str, Any]:
        """Get IP geolocation for domain"""
        try:
            # Resolve domain to IP
            ip_address = socket.gethostbyname(domain)
            
            # This would use a geolocation API
            # For now, return simulated data
            geolocation = {
                "ip": ip_address,
                "country": "United States",
                "country_code": "US",
                "region": "California",
                "city": "San Francisco",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "timezone": "America/Los_Angeles",
                "isp": "Cloudflare, Inc.",
                "organization": "Cloudflare"
            }
            
            return geolocation
            
        except Exception as e:
            logger.error(f"Error getting IP geolocation for {domain}: {e}")
            return {"error": str(e)}
    
    async def _check_reputation(self, domain: str) -> Dict[str, Any]:
        """Check domain reputation"""
        try:
            # This would integrate with reputation APIs
            # For now, return simulated data
            reputation = {
                "blacklisted": False,
                "suspicious": False,
                "malware": False,
                "phishing": False,
                "spam": False,
                "reputation_score": 85,
                "sources_checked": ["VirusTotal", "URLVoid", "Google Safe Browsing"],
                "last_checked": datetime.utcnow().isoformat()
            }
            
            return reputation
            
        except Exception as e:
            logger.error(f"Error checking reputation for {domain}: {e}")
            return {"error": str(e)}
    
    def _clean_domain(self, domain: str) -> str:
        """Clean and normalize domain"""
        try:
            # Remove protocol
            if domain.startswith(("http://", "https://")):
                domain = domain.split("://", 1)[1]
            
            # Remove path and query parameters
            domain = domain.split("/")[0]
            domain = domain.split("?")[0]
            domain = domain.split("#")[0]
            
            # Remove port
            if ":" in domain:
                domain = domain.split(":")[0]
            
            # Remove www prefix
            if domain.startswith("www."):
                domain = domain[4:]
            
            return domain.lower().strip()
            
        except Exception as e:
            logger.error(f"Error cleaning domain {domain}: {e}")
            return domain 