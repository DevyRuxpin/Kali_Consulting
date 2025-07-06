"""
Dark Web Intelligence Service
Advanced dark web monitoring and intelligence gathering
"""

import asyncio
import logging
import aiohttp
import hashlib
import json
import re
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
import base64
import hmac
import time

from app.models.schemas import (
    ThreatAssessment,
    ThreatLevel,
    Entity,
    Relationship,
    Pattern,
    Anomaly
)

logger = logging.getLogger(__name__)

@dataclass
class DarkWebEntity:
    """Dark web entity information"""
    id: str
    entity_type: str  # marketplace, vendor, listing, forum, user
    platform: str  # tor, i2p, zeronet, etc.
    url: str
    title: str
    description: Optional[str]
    created_at: datetime
    last_seen: datetime
    threat_score: float
    metadata: Dict[str, Any]

@dataclass
class DarkWebIntelligence:
    """Dark web intelligence data"""
    investigation_id: str
    entities: List[DarkWebEntity]
    relationships: List[Relationship]
    threats: List[ThreatAssessment]
    patterns: List[Pattern]
    anomalies: List[Anomaly]
    collected_at: datetime
    metadata: Dict[str, Any]

class DarkWebIntelligenceService:
    """Advanced dark web intelligence gathering and analysis"""
    
    def __init__(self):
        self.tor_proxies = []
        self.i2p_proxies = []
        self.known_marketplaces = self._load_known_marketplaces()
        self.threat_indicators = self._load_threat_indicators()
        self.session = None
        self.rate_limits = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(ssl=False)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def scan_dark_web_entities(
        self, 
        target: str,
        platforms: List[str] = None,
        depth: str = "comprehensive"
    ) -> DarkWebIntelligence:
        """Scan dark web for target-related entities"""
        try:
            logger.info(f"Starting dark web scan for target: {target}")
            
            if platforms is None:
                platforms = ["tor", "i2p", "zeronet"]
            
            entities = []
            relationships = []
            threats = []
            patterns = []
            anomalies = []
            
            # Scan different dark web platforms
            for platform in platforms:
                platform_entities = await self._scan_platform(
                    target, platform, depth
                )
                entities.extend(platform_entities)
                
                # Analyze platform-specific relationships
                platform_relationships = await self._analyze_platform_relationships(
                    platform_entities, platform
                )
                relationships.extend(platform_relationships)
            
            # Cross-platform analysis
            cross_platform_relationships = await self._analyze_cross_platform_relationships(
                entities
            )
            relationships.extend(cross_platform_relationships)
            
            # Threat assessment
            threats = await self._assess_dark_web_threats(entities, relationships)
            
            # Pattern detection
            patterns = await self._detect_dark_web_patterns(entities, relationships)
            
            # Anomaly detection
            anomalies = await self._detect_dark_web_anomalies(entities, relationships)
            
            # Create intelligence result
            intelligence = DarkWebIntelligence(
                investigation_id=f"dark_web_{target}_{int(time.time())}",
                entities=entities,
                relationships=relationships,
                threats=threats,
                patterns=patterns,
                anomalies=anomalies,
                collected_at=datetime.utcnow(),
                metadata={
                    "target": target,
                    "platforms_scanned": platforms,
                    "scan_depth": depth,
                    "total_entities": len(entities),
                    "total_relationships": len(relationships),
                    "total_threats": len(threats),
                    "total_patterns": len(patterns),
                    "total_anomalies": len(anomalies)
                }
            )
            
            logger.info(f"Dark web scan completed for target: {target}")
            return intelligence
            
        except Exception as e:
            logger.error(f"Error scanning dark web for target {target}: {e}")
            raise
    
    async def monitor_dark_web_marketplaces(
        self,
        keywords: List[str] = None,
        categories: List[str] = None
    ) -> List[DarkWebEntity]:
        """Monitor dark web marketplaces for specific items"""
        try:
            logger.info("Starting dark web marketplace monitoring")
            
            if keywords is None:
                keywords = ["weapons", "drugs", "hacking", "malware", "credentials"]
            
            if categories is None:
                categories = ["weapons", "drugs", "digital_goods", "services"]
            
            marketplace_entities = []
            
            # Monitor known marketplaces
            for marketplace in self.known_marketplaces:
                if marketplace.get("active", True):
                    entities = await self._monitor_marketplace(
                        marketplace, keywords, categories
                    )
                    marketplace_entities.extend(entities)
            
            logger.info(f"Marketplace monitoring completed: {len(marketplace_entities)} entities found")
            return marketplace_entities
            
        except Exception as e:
            logger.error(f"Error monitoring dark web marketplaces: {e}")
            return []
    
    async def analyze_cryptocurrency_transactions(
        self,
        addresses: List[str],
        blockchain: str = "bitcoin"
    ) -> Dict[str, Any]:
        """Analyze cryptocurrency transactions for dark web activity"""
        try:
            logger.info(f"Analyzing cryptocurrency transactions for {len(addresses)} addresses")
            
            transaction_data = {}
            
            for address in addresses:
                # Get transaction history
                transactions = await self._get_transaction_history(address, blockchain)
                
                # Analyze transaction patterns
                patterns = await self._analyze_transaction_patterns(transactions)
                
                # Detect suspicious activity
                suspicious_activity = await self._detect_suspicious_transactions(transactions)
                
                # Calculate risk score
                risk_score = await self._calculate_crypto_risk_score(
                    transactions, patterns, suspicious_activity
                )
                
                transaction_data[address] = {
                    "transactions": transactions,
                    "patterns": patterns,
                    "suspicious_activity": suspicious_activity,
                    "risk_score": risk_score,
                    "blockchain": blockchain
                }
            
            logger.info("Cryptocurrency transaction analysis completed")
            return transaction_data
            
        except Exception as e:
            logger.error(f"Error analyzing cryptocurrency transactions: {e}")
            return {}
    
    async def track_dark_web_forums(
        self,
        keywords: List[str],
        platforms: List[str] = None
    ) -> List[DarkWebEntity]:
        """Track dark web forums for specific discussions"""
        try:
            logger.info(f"Tracking dark web forums for keywords: {keywords}")
            
            if platforms is None:
                platforms = ["tor", "i2p"]
            
            forum_entities = []
            
            for platform in platforms:
                platform_entities = await self._track_platform_forums(
                    keywords, platform
                )
                forum_entities.extend(platform_entities)
            
            logger.info(f"Forum tracking completed: {len(forum_entities)} entities found")
            return forum_entities
            
        except Exception as e:
            logger.error(f"Error tracking dark web forums: {e}")
            return []
    
    async def _scan_platform(
        self, 
        target: str, 
        platform: str, 
        depth: str
    ) -> List[DarkWebEntity]:
        """Scan specific dark web platform"""
        try:
            entities = []
            
            if platform == "tor":
                entities = await self._scan_tor_network(target, depth)
            elif platform == "i2p":
                entities = await self._scan_i2p_network(target, depth)
            elif platform == "zeronet":
                entities = await self._scan_zeronet_network(target, depth)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error scanning platform {platform}: {e}")
            return []
    
    async def _scan_tor_network(self, target: str, depth: str) -> List[DarkWebEntity]:
        """Scan Tor network for target-related entities"""
        try:
            entities = []
            
            # Search known Tor directories
            directories = [
                "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion",
                "http://ahmiafiqnpuboyls22wj36577c4qfnbb7dxmoxkmowy4kjlyx3l6ptlad.onion"
            ]
            
            for directory in directories:
                try:
                    # Search for target in directory
                    search_results = await self._search_tor_directory(
                        directory, target
                    )
                    
                    for result in search_results:
                        entity = DarkWebEntity(
                            id=f"tor_{hashlib.md5(result['url'].encode()).hexdigest()}",
                            entity_type="service",
                            platform="tor",
                            url=result["url"],
                            title=result.get("title", "Unknown"),
                            description=result.get("description"),
                            created_at=datetime.utcnow(),
                            last_seen=datetime.utcnow(),
                            threat_score=await self._calculate_tor_threat_score(result),
                            metadata={
                                "directory": directory,
                                "search_term": target,
                                "response_time": result.get("response_time"),
                                "ssl_cert": result.get("ssl_cert")
                            }
                        )
                        entities.append(entity)
                        
                except Exception as e:
                    logger.warning(f"Error scanning Tor directory {directory}: {e}")
                    continue
            
            return entities
            
        except Exception as e:
            logger.error(f"Error scanning Tor network: {e}")
            return []
    
    async def _search_tor_directory(self, directory: str, target: str) -> List[Dict[str, Any]]:
        """Search Tor directory for target"""
        try:
            # This would implement actual Tor directory searching
            # For now, return mock data
            return [
                {
                    "url": f"http://{target}.onion",
                    "title": f"Service related to {target}",
                    "description": f"Dark web service related to {target}",
                    "response_time": 2.5,
                    "ssl_cert": "valid"
                }
            ]
        except Exception as e:
            logger.error(f"Error searching Tor directory: {e}")
            return []
    
    async def _calculate_tor_threat_score(self, result: Dict[str, Any]) -> float:
        """Calculate threat score for Tor entity"""
        try:
            score = 0.0
        
            # SSL certificate validity
            if result.get("ssl_cert") == "valid":
                score += 0.2
            else:
                score += 0.8
            
            # Response time (faster = more suspicious)
            response_time = result.get("response_time", 5.0)
            if response_time < 1.0:
                score += 0.3
            elif response_time < 3.0:
                score += 0.1
            
            # Content analysis (would implement actual content analysis)
            if "suspicious" in result.get("title", "").lower():
                score += 0.4
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating Tor threat score: {e}")
            return 0.5
    
    async def _monitor_marketplace(
        self, 
        marketplace: Dict[str, Any], 
        keywords: List[str], 
        categories: List[str]
    ) -> List[DarkWebEntity]:
        """Monitor specific dark web marketplace"""
        try:
            entities = []
            
            # This would implement actual marketplace monitoring
            # For now, return mock data based on keywords
            for keyword in keywords:
                entity = DarkWebEntity(
                    id=f"marketplace_{marketplace['name']}_{hashlib.md5(keyword.encode()).hexdigest()}",
                    entity_type="listing",
                    platform=marketplace.get("platform", "tor"),
                    url=marketplace.get("url", ""),
                    title=f"Listing related to {keyword}",
                    description=f"Dark web listing for {keyword} on {marketplace['name']}",
                    created_at=datetime.utcnow(),
                    last_seen=datetime.utcnow(),
                    threat_score=0.8 if keyword in ["weapons", "drugs", "malware"] else 0.4,
                    metadata={
                        "marketplace": marketplace["name"],
                        "keyword": keyword,
                        "category": "suspicious" if keyword in ["weapons", "drugs", "malware"] else "monitoring"
                    }
                )
                entities.append(entity)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error monitoring marketplace {marketplace.get('name', 'unknown')}: {e}")
            return []
    
    async def _get_transaction_history(self, address: str, blockchain: str) -> List[Dict[str, Any]]:
        """Get cryptocurrency transaction history"""
        try:
            # This would implement actual blockchain API calls
            # For now, return mock data
            return [
                {
                    "txid": f"tx_{hashlib.md5(address.encode()).hexdigest()}",
                    "amount": 0.001,
                    "timestamp": datetime.utcnow().isoformat(),
                    "from_address": address,
                    "to_address": "suspicious_address_123",
                    "block_height": 123456,
                    "confirmations": 6
                }
            ]
        except Exception as e:
            logger.error(f"Error getting transaction history: {e}")
            return []
    
    async def _analyze_transaction_patterns(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cryptocurrency transaction patterns"""
        try:
            patterns = {
                "total_transactions": len(transactions),
                "total_volume": sum(tx.get("amount", 0) for tx in transactions),
                "average_amount": sum(tx.get("amount", 0) for tx in transactions) / len(transactions) if transactions else 0,
                "suspicious_patterns": []
            }
            
            # Detect suspicious patterns
            if len(transactions) > 100:
                patterns["suspicious_patterns"].append("high_transaction_frequency")
            
            if patterns["total_volume"] > 1.0:
                patterns["suspicious_patterns"].append("high_volume")
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing transaction patterns: {e}")
            return {}
    
    async def _detect_suspicious_transactions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect suspicious cryptocurrency transactions"""
        try:
            suspicious = []
            
            for tx in transactions:
                # Check for known suspicious addresses
                if "suspicious" in tx.get("to_address", ""):
                    suspicious.append({
                        "txid": tx.get("txid"),
                        "reason": "suspicious_destination",
                        "risk_score": 0.8
                    })
                
                # Check for unusual amounts
                if tx.get("amount", 0) > 0.1:
                    suspicious.append({
                        "txid": tx.get("txid"),
                        "reason": "high_amount",
                        "risk_score": 0.6
                    })
            
            return suspicious
            
        except Exception as e:
            logger.error(f"Error detecting suspicious transactions: {e}")
            return []
    
    async def _calculate_crypto_risk_score(
        self, 
        transactions: List[Dict[str, Any]], 
        patterns: Dict[str, Any], 
        suspicious: List[Dict[str, Any]]
    ) -> float:
        """Calculate cryptocurrency risk score"""
        try:
            score = 0.0
            
            # Base score from suspicious transactions
            score += len(suspicious) * 0.2
            
            # Pattern-based scoring
            if "high_transaction_frequency" in patterns.get("suspicious_patterns", []):
                score += 0.3
            
            if "high_volume" in patterns.get("suspicious_patterns", []):
                score += 0.4
            
            # Transaction volume scoring
            total_volume = patterns.get("total_volume", 0)
            if total_volume > 1.0:
                score += 0.2
            elif total_volume > 0.1:
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating crypto risk score: {e}")
            return 0.5
    
    async def _assess_dark_web_threats(
        self, 
        entities: List[DarkWebEntity], 
        relationships: List[Relationship]
    ) -> List[ThreatAssessment]:
        """Assess threats from dark web entities"""
        try:
            threats = []
            
            for entity in entities:
                if entity.threat_score > 0.7:
                    threat = ThreatAssessment(
                        id=f"dark_web_threat_{entity.id}",
                        target=entity.title,
                        threat_level=ThreatLevel.HIGH if entity.threat_score > 0.8 else ThreatLevel.MEDIUM,
                        confidence=entity.threat_score,
                        indicators=[
                            f"Dark web entity: {entity.title}",
                            f"Platform: {entity.platform}",
                            f"URL: {entity.url}",
                            f"Threat score: {entity.threat_score}"
                        ],
                        description=f"High-threat dark web entity detected: {entity.title}",
                        recommendations=[
                            "Monitor entity activity",
                            "Investigate entity connections",
                            "Assess potential impact",
                            "Consider law enforcement notification"
                        ],
                        metadata={
                            "entity_id": entity.id,
                            "platform": entity.platform,
                            "entity_type": entity.entity_type,
                            "threat_score": entity.threat_score
                        }
                    )
                    threats.append(threat)
            
            return threats
            
        except Exception as e:
            logger.error(f"Error assessing dark web threats: {e}")
            return []
    
    async def _detect_dark_web_patterns(
        self, 
        entities: List[DarkWebEntity], 
        relationships: List[Relationship]
    ) -> List[Pattern]:
        """Detect patterns in dark web activity"""
        try:
            patterns = []
            
            # Platform distribution pattern
            platform_counts = {}
            for entity in entities:
                platform_counts[entity.platform] = platform_counts.get(entity.platform, 0) + 1
            
            if len(platform_counts) > 1:
                pattern = Pattern(
                    id="dark_web_cross_platform",
                    pattern_type="cross_platform_activity",
                    title="Cross-Platform Dark Web Activity",
                    description=f"Target appears on {len(platform_counts)} different dark web platforms",
                    confidence=0.8,
                    entities_involved=[e.id for e in entities],
                    metadata={
                        "platforms": list(platform_counts.keys()),
                        "platform_counts": platform_counts
                    }
                )
                patterns.append(pattern)
            
            # High-threat concentration pattern
            high_threat_entities = [e for e in entities if e.threat_score > 0.8]
            if len(high_threat_entities) > 2:
                pattern = Pattern(
                    id="dark_web_high_threat_concentration",
                    pattern_type="threat_concentration",
                    title="High-Threat Entity Concentration",
                    description=f"Multiple high-threat entities detected ({len(high_threat_entities)})",
                    confidence=0.9,
                    entities_involved=[e.id for e in high_threat_entities],
                    metadata={
                        "high_threat_count": len(high_threat_entities),
                        "average_threat_score": sum(e.threat_score for e in high_threat_entities) / len(high_threat_entities)
                    }
                )
                patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting dark web patterns: {e}")
            return []
    
    async def _detect_dark_web_anomalies(
        self, 
        entities: List[DarkWebEntity], 
        relationships: List[Relationship]
    ) -> List[Anomaly]:
        """Detect anomalies in dark web activity"""
        try:
            anomalies = []
            
            # Unusual platform combination
            platforms = set(e.platform for e in entities)
            if len(platforms) > 2:
                anomaly = Anomaly(
                    id="dark_web_unusual_platform_combination",
                    anomaly_type="platform",
                    category="unusual_combination",
                    title="Unusual Platform Combination",
                    description=f"Target appears on {len(platforms)} different dark web platforms simultaneously",
                    severity="high",
                    confidence=0.8,
                    entities_involved=[e.id for e in entities],
                    metadata={
                        "platforms": list(platforms),
                        "platform_count": len(platforms)
                    }
                )
                anomalies.append(anomaly)
            
            # Rapid appearance across platforms
            creation_times = [e.created_at for e in entities]
            if len(creation_times) > 1:
                time_span = max(creation_times) - min(creation_times)
                if time_span.total_seconds() < 3600:  # Less than 1 hour
                    anomaly = Anomaly(
                        id="dark_web_rapid_appearance",
                        anomaly_type="temporal",
                        category="rapid_appearance",
                        title="Rapid Cross-Platform Appearance",
                        description="Target appeared on multiple dark web platforms within a short time period",
                        severity="medium",
                        confidence=0.7,
                        entities_involved=[e.id for e in entities],
                        metadata={
                            "time_span_seconds": time_span.total_seconds(),
                            "platform_count": len(entities)
                        }
                    )
                    anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting dark web anomalies: {e}")
            return []
    
    async def _analyze_platform_relationships(
        self, 
        entities: List[DarkWebEntity], 
        platform: str
    ) -> List[Relationship]:
        """Analyze relationships between entities on the same platform"""
        try:
            relationships = []
            
            # Create relationships between entities on the same platform
            for i, entity1 in enumerate(entities):
                for entity2 in entities[i+1:]:
                    if entity1.platform == entity2.platform:
                        relationship = Relationship(
                            id=f"dark_web_platform_{entity1.id}_{entity2.id}",
                            source_entity_id=entity1.id,
                            target_entity_id=entity2.id,
                            relationship_type="same_platform",
                            confidence=0.9,
                            metadata={
                                "platform": platform,
                                "source_type": entity1.entity_type,
                                "target_type": entity2.entity_type
                            }
                        )
                        relationships.append(relationship)
            
            return relationships
            
        except Exception as e:
            logger.error(f"Error analyzing platform relationships: {e}")
            return []
    
    async def _analyze_cross_platform_relationships(
        self, 
        entities: List[DarkWebEntity]
    ) -> List[Relationship]:
        """Analyze relationships between entities across different platforms"""
        try:
            relationships = []
            
            # Group entities by target similarity
            target_groups = {}
            for entity in entities:
                # Simple grouping by title similarity (would implement more sophisticated matching)
                key = entity.title.lower().split()[0] if entity.title else "unknown"
                if key not in target_groups:
                    target_groups[key] = []
                target_groups[key].append(entity)
            
            # Create cross-platform relationships
            for key, group in target_groups.items():
                if len(group) > 1:
                    for i, entity1 in enumerate(group):
                        for entity2 in group[i+1:]:
                            if entity1.platform != entity2.platform:
                                relationship = Relationship(
                                    id=f"dark_web_cross_platform_{entity1.id}_{entity2.id}",
                                    source_entity_id=entity1.id,
                                    target_entity_id=entity2.id,
                                    relationship_type="cross_platform",
                                    confidence=0.7,
                                    metadata={
                                        "source_platform": entity1.platform,
                                        "target_platform": entity2.platform,
                                        "group_key": key
                                    }
                                )
                                relationships.append(relationship)
            
            return relationships
            
        except Exception as e:
            logger.error(f"Error analyzing cross-platform relationships: {e}")
            return []
    
    def _load_known_marketplaces(self) -> List[Dict[str, Any]]:
        """Load known dark web marketplaces"""
        return [
            {
                "name": "Silk Road",
                "url": "http://silkroad.onion",
                "platform": "tor",
                "active": False,
                "categories": ["drugs", "digital_goods"]
            },
            {
                "name": "AlphaBay",
                "url": "http://alphabay.onion",
                "platform": "tor",
                "active": False,
                "categories": ["drugs", "weapons", "digital_goods"]
            },
            {
                "name": "Dream Market",
                "url": "http://dreammarket.onion",
                "platform": "tor",
                "active": False,
                "categories": ["drugs", "digital_goods"]
            }
        ]
    
    def _load_threat_indicators(self) -> Dict[str, List[str]]:
        """Load threat indicators for dark web analysis"""
        return {
            "weapons": ["gun", "weapon", "ammo", "explosive", "knife"],
            "drugs": ["drug", "cocaine", "heroin", "marijuana", "pills"],
            "malware": ["malware", "virus", "trojan", "ransomware", "spyware"],
            "credentials": ["password", "login", "credential", "account", "hack"],
            "services": ["hacking", "ddos", "phishing", "fraud", "scam"]
        } 