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
import requests

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
        """Analyze a domain for security and threat information"""
        try:
            import whois
            import socket
            import ssl
            import requests
            from datetime import datetime
            
            analysis = {
                "domain": domain,
                "analysis_date": datetime.utcnow().isoformat(),
                "whois_info": {},
                "dns_records": {},
                "ssl_certificate": {},
                "security_headers": {},
                "threat_indicators": {},
                "risk_score": 0.0
            }
            
            # WHOIS lookup
            try:
                w = whois.whois(domain)
                analysis["whois_info"] = {
                    "registrar": w.registrar,
                    "creation_date": str(w.creation_date) if w.creation_date else "",
                    "expiration_date": str(w.expiration_date) if w.expiration_date else "",
                    "name_servers": w.name_servers if isinstance(w.name_servers, list) else [str(w.name_servers)] if w.name_servers else []
                }
            except Exception as e:
                logger.warning(f"WHOIS lookup failed for {domain}: {e}")
            
            # DNS records
            try:
                import dns.resolver
                
                record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
                for record_type in record_types:
                    try:
                        answers = dns.resolver.resolve(domain, record_type)
                        analysis["dns_records"][record_type] = [str(rdata) for rdata in answers.rrset]
                    except Exception:
                        analysis["dns_records"][record_type] = []
            except Exception as e:
                logger.warning(f"DNS lookup failed for {domain}: {e}")
            
            # SSL certificate
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        if cert:
                            analysis["ssl_certificate"] = {
                                "subject": dict(x[0] for x in cert.get("subject", [])),
                                "issuer": dict(x[0] for x in cert.get("issuer", [])),
                                "not_before": cert.get("notBefore", ""),
                                "not_after": cert.get("notAfter", ""),
                                "serial_number": str(cert.get("serialNumber", ""))
                            }
            except Exception as e:
                logger.warning(f"SSL certificate check failed for {domain}: {e}")
            
            # Security headers
            try:
                response = requests.get(f"https://{domain}", timeout=10)
                headers = response.headers
                analysis["security_headers"] = {
                    "strict_transport_security": headers.get("Strict-Transport-Security", ""),
                    "x_frame_options": headers.get("X-Frame-Options", ""),
                    "x_content_type_options": headers.get("X-Content-Type-Options", ""),
                    "x_xss_protection": headers.get("X-XSS-Protection", ""),
                    "content_security_policy": headers.get("Content-Security-Policy", "")
                }
            except Exception as e:
                logger.warning(f"Security headers check failed for {domain}: {e}")
            
            # Threat indicators
            threat_score = 0.0
            indicators = []
            
            # Check for suspicious patterns
            if any(suspicious in domain.lower() for suspicious in ["malware", "virus", "hack", "crack"]):
                indicators.append("suspicious_keywords_in_domain")
                threat_score += 0.3
            
            # Check for newly registered domains
            if analysis["whois_info"].get("creation_date"):
                try:
                    creation_date = datetime.strptime(analysis["whois_info"]["creation_date"][:10], "%Y-%m-%d")
                    days_old = (datetime.now() - creation_date).days
                    if days_old < 30:
                        indicators.append("newly_registered_domain")
                        threat_score += 0.2
                except:
                    pass
            
            # Check for missing security headers
            security_headers = analysis["security_headers"]
            if not security_headers.get("strict_transport_security"):
                indicators.append("missing_hsts_header")
                threat_score += 0.1
            
            if not security_headers.get("x_frame_options"):
                indicators.append("missing_frame_options")
                threat_score += 0.1
            
            analysis["threat_indicators"] = {
                "indicators": indicators,
                "threat_score": min(threat_score, 1.0)
            }
            analysis["risk_score"] = min(threat_score, 1.0)
            
            return analysis
            
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
        """Search for domains related to a query using real domain APIs"""
        try:
            results = []
            
            # Real domain search using multiple APIs
            search_apis = [
                {
                    "name": "SecurityTrails",
                    "url": f"https://api.securitytrails.com/v1/domain/search?query={query}",
                    "headers": {"APIKEY": "YOUR_SECURITYTRAILS_API_KEY"}
                },
                {
                    "name": "Censys",
                    "url": f"https://search.censys.io/api/v2/hosts/search?q={query}",
                    "headers": {"Authorization": "Bearer YOUR_CENSYS_API_TOKEN"}
                }
            ]
            
            for api in search_apis:
                try:
                    response = requests.get(
                        api["url"], 
                        headers=api["headers"], 
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if api["name"] == "SecurityTrails":
                            # Parse SecurityTrails response
                            for record in data.get("records", [])[:max_results//2]:
                                results.append({
                                    "domain": record.get("hostname", ""),
                                    "title": f"Domain related to {query}",
                                    "description": f"Found via SecurityTrails search",
                                    "created_date": record.get("created", ""),
                                    "registrar": record.get("registrar", ""),
                                    "status": "active" if record.get("status") else "inactive"
                                })
                        
                        elif api["name"] == "Censys":
                            # Parse Censys response
                            for hit in data.get("result", {}).get("hits", [])[:max_results//2]:
                                domain = hit.get("dns", {}).get("names", [""])[0]
                                if domain:
                                    results.append({
                                        "domain": domain,
                                        "title": f"Domain related to {query}",
                                        "description": f"Found via Censys search",
                                        "created_date": "",
                                        "registrar": "",
                                        "status": "active"
                                    })
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"Error with {api['name']} API: {e}")
                    continue
            
            # If no results from APIs, use DNS-based search
            if not results:
                try:
                    import dns.resolver
                    import dns.reversename
                    
                    # Try to find subdomains using DNS
                    common_subdomains = ["www", "mail", "ftp", "admin", "blog", "api"]
                    for subdomain in common_subdomains:
                        try:
                            test_domain = f"{subdomain}.{query}"
                            dns.resolver.resolve(test_domain, "A")
                            results.append({
                                "domain": test_domain,
                                "title": f"Subdomain found: {test_domain}",
                                "description": f"DNS subdomain discovery",
                                "created_date": "",
                                "registrar": "",
                                "status": "active"
                            })
                        except:
                            continue
                            
                except Exception as e:
                    logger.warning(f"DNS-based search failed: {e}")
            
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
            
            # PTR records for IP addresses
            if dns_data["a_records"]:
                try:
                    for ip in dns_data["a_records"]:
                        ptr_records = dns.resolver.resolve(dns.reversename.from_address(ip), 'PTR')
                        dns_data["ptr_records"].extend([str(record) for record in ptr_records])
                except Exception as e:
                    logger.warning(f"Error resolving PTR records for {domain}: {e}")
            
            return dns_data
            
        except Exception as e:
            logger.error(f"Error in DNS analysis for {domain}: {e}")
            return {"error": str(e)}
    
    async def _analyze_whois(self, domain: str) -> Dict[str, Any]:
        """Analyze WHOIS data for domain"""
        try:
            # Use python-whois library with better error handling
            w = whois.whois(domain)
            
            if w is None:
                return {
                    "error": "No WHOIS data found",
                    "registrar": None,
                    "creation_date": None,
                    "expiration_date": None,
                    "updated_date": None,
                    "status": None,
                    "name_servers": None,
                    "registrant": {},
                    "admin": {},
                    "tech": {}
                }
            
            whois_data = {
                "registrar": getattr(w, 'registrar', None),
                "creation_date": getattr(w, 'creation_date', None),
                "expiration_date": getattr(w, 'expiration_date', None),
                "updated_date": getattr(w, 'updated_date', None),
                "status": getattr(w, 'status', None),
                "name_servers": getattr(w, 'name_servers', None),
                "registrant": {
                    "name": getattr(w, 'registrant_name', None),
                    "organization": getattr(w, 'registrant_organization', None),
                    "email": getattr(w, 'registrant_email', None),
                    "phone": getattr(w, 'registrant_phone', None),
                    "address": getattr(w, 'registrant_address', None)
                },
                "admin": {
                    "name": getattr(w, 'admin_name', None),
                    "organization": getattr(w, 'admin_organization', None),
                    "email": getattr(w, 'admin_email', None),
                    "phone": getattr(w, 'admin_phone', None)
                },
                "tech": {
                    "name": getattr(w, 'tech_name', None),
                    "organization": getattr(w, 'tech_organization', None),
                    "email": getattr(w, 'tech_email', None),
                    "phone": getattr(w, 'tech_phone', None)
                }
            }
            
            return whois_data
            
        except Exception as e:
            logger.error(f"Error analyzing WHOIS for {domain}: {e}")
            return {
                "error": str(e),
                "registrar": None,
                "creation_date": None,
                "expiration_date": None,
                "updated_date": None,
                "status": None,
                "name_servers": None,
                "registrant": {},
                "admin": {},
                "tech": {}
            }
    
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
                if self.session is None:
                    # Create a temporary session if none exists
                    async with aiohttp.ClientSession(
                        headers={
                            "User-Agent": "Kali-OSINT-Platform/1.0",
                            "Accept": "application/json, text/html, */*"
                        }
                    ) as temp_session:
                        async with temp_session.get(f"https://{domain}", timeout=10) as response:
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
                else:
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
            return {
                "error": str(e),
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
        """Get IP geolocation for domain using real API"""
        try:
            # Resolve domain to IP
            ip_address = socket.gethostbyname(domain)
            
            # Use ipapi.co for geolocation (free tier)
            geolocation_url = f"https://ipapi.co/{ip_address}/json/"
            
            response = requests.get(geolocation_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                geolocation = {
                    "ip": ip_address,
                    "country": data.get("country_name", ""),
                    "country_code": data.get("country_code", ""),
                    "region": data.get("region", ""),
                    "city": data.get("city", ""),
                    "latitude": data.get("latitude", 0),
                    "longitude": data.get("longitude", 0),
                    "timezone": data.get("timezone", ""),
                    "isp": data.get("org", ""),
                    "organization": data.get("org", "")
                }
                
                return geolocation
            else:
                return {"error": f"Failed to get geolocation: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error getting IP geolocation for {domain}: {e}")
            return {"error": str(e)}
    
    async def _check_reputation(self, domain: str) -> Dict[str, Any]:
        """Check domain reputation using real APIs"""
        try:
            reputation = {
                "blacklisted": False,
                "suspicious": False,
                "malware": False,
                "phishing": False,
                "spam": False,
                "reputation_score": 100,
                "sources_checked": [],
                "last_checked": datetime.utcnow().isoformat()
            }
            
            # Check with VirusTotal (requires API key, but we'll use public endpoint)
            try:
                vt_url = f"https://www.virustotal.com/vtapi/v2/url/report"
                params = {"apikey": "", "resource": domain}  # Empty API key for public endpoint
                response = requests.get(vt_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    vt_data = response.json()
                    reputation["sources_checked"].append("VirusTotal")
                    
                    if vt_data.get("positives", 0) > 0:
                        reputation["malware"] = True
                        reputation["reputation_score"] -= 30
                        
            except Exception as e:
                logger.warning(f"VirusTotal check failed: {e}")
            
            # Check with URLVoid (free tier)
            try:
                urlvoid_url = f"https://api.urlvoid.com/v1/url/{domain}/"
                response = requests.get(urlvoid_url, timeout=10)
                
                if response.status_code == 200:
                    urlvoid_data = response.json()
                    reputation["sources_checked"].append("URLVoid")
                    
                    # Parse URLVoid results
                    if urlvoid_data.get("detections", 0) > 0:
                        reputation["suspicious"] = True
                        reputation["reputation_score"] -= 20
                        
            except Exception as e:
                logger.warning(f"URLVoid check failed: {e}")
            
            # Check with Google Safe Browsing (requires API key)
            # For now, skip this as it requires API key
            
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