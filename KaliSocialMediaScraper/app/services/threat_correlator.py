"""
Threat Correlation Service
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re
from collections import defaultdict, Counter
import statistics

from app.models.schemas import Entity, Relationship, Pattern, Anomaly, ThreatAssessment, ThreatLevel

logger = logging.getLogger(__name__)

class ThreatCorrelator:
    """Advanced threat correlation and assessment service"""
    
    def __init__(self):
        self.threat_indicators = self._load_threat_indicators()
        self.threat_patterns = self._load_threat_patterns()
        self.risk_factors = self._load_risk_factors()
        self.threat_scoring = self._load_threat_scoring()
        
    async def correlate_entity_threats(self, entities: List[Entity]) -> List[ThreatAssessment]:
        """Correlate threat indicators for entities"""
        try:
            threat_assessments = []
            
            for entity in entities:
                threat_score = await self._calculate_entity_threat_score(entity)
                threat_level = self._determine_threat_level(threat_score)
                indicators = await self._identify_entity_indicators(entity)
                
                if threat_score > 0.3:  # Only create assessment for significant threats
                    assessment = ThreatAssessment(
                        id=f"threat_entity_{entity.id}",
                        target=entity.id,
                        target_type="entity",
                        threat_level=threat_level,
                        threat_score=threat_score,
                        indicators=indicators,
                        assessment_timestamp=datetime.utcnow(),
                        metadata={
                            "entity_type": entity.type,
                            "platform": entity.platform,
                            "username": entity.username
                        }
                    )
                    threat_assessments.append(assessment)
            
            return threat_assessments
            
        except Exception as e:
            logger.error(f"Error correlating entity threats: {e}")
            return []
    
    async def correlate_relationship_threats(self, relationships: List[Relationship]) -> List[ThreatAssessment]:
        """Correlate threat indicators for relationships"""
        try:
            threat_assessments = []
            
            # Group relationships by type
            relationship_groups = defaultdict(list)
            for rel in relationships:
                relationship_groups[rel.relationship_type].append(rel)
            
            # Analyze each relationship type
            for rel_type, rels in relationship_groups.items():
                if len(rels) > 10:  # Significant relationship cluster
                    threat_score = await self._calculate_relationship_threat_score(rel_type, rels)
                    threat_level = self._determine_threat_level(threat_score)
                    indicators = await self._identify_relationship_indicators(rel_type, rels)
                    
                    if threat_score > 0.3:
                        assessment = ThreatAssessment(
                            id=f"threat_relationship_{rel_type}",
                            target=f"relationship_cluster_{rel_type}",
                            target_type="relationship_cluster",
                            threat_level=threat_level,
                            threat_score=threat_score,
                            indicators=indicators,
                            assessment_timestamp=datetime.utcnow(),
                            metadata={
                                "relationship_type": rel_type,
                                "cluster_size": len(rels),
                                "platforms": list(set([rel.platform for rel in rels]))
                            }
                        )
                        threat_assessments.append(assessment)
            
            return threat_assessments
            
        except Exception as e:
            logger.error(f"Error correlating relationship threats: {e}")
            return []
    
    async def correlate_pattern_threats(self, patterns: List[Pattern]) -> List[ThreatAssessment]:
        """Correlate threat indicators for patterns"""
        try:
            threat_assessments = []
            
            # Group patterns by type
            pattern_groups = defaultdict(list)
            for pattern in patterns:
                pattern_groups[pattern.pattern_type].append(pattern)
            
            # Analyze each pattern type
            for pattern_type, pattern_list in pattern_groups.items():
                threat_score = await self._calculate_pattern_threat_score(pattern_type, pattern_list)
                threat_level = self._determine_threat_level(threat_score)
                indicators = await self._identify_pattern_indicators(pattern_type, pattern_list)
                
                if threat_score > 0.3:
                    assessment = ThreatAssessment(
                        id=f"threat_pattern_{pattern_type}",
                        target=f"pattern_cluster_{pattern_type}",
                        target_type="pattern_cluster",
                        threat_level=threat_level,
                        threat_score=threat_score,
                        indicators=indicators,
                        assessment_timestamp=datetime.utcnow(),
                        metadata={
                            "pattern_type": pattern_type,
                            "pattern_count": len(pattern_list),
                            "average_confidence": statistics.mean([p.confidence for p in pattern_list])
                        }
                    )
                    threat_assessments.append(assessment)
            
            return threat_assessments
            
        except Exception as e:
            logger.error(f"Error correlating pattern threats: {e}")
            return []
    
    async def correlate_anomaly_threats(self, anomalies: List[Anomaly]) -> List[ThreatAssessment]:
        """Correlate threat indicators for anomalies"""
        try:
            threat_assessments = []
            
            # Group anomalies by type
            anomaly_groups = defaultdict(list)
            for anomaly in anomalies:
                anomaly_groups[anomaly.anomaly_type].append(anomaly)
            
            # Analyze each anomaly type
            for anomaly_type, anomaly_list in anomaly_groups.items():
                threat_score = await self._calculate_anomaly_threat_score(anomaly_type, anomaly_list)
                threat_level = self._determine_threat_level(threat_score)
                indicators = await self._identify_anomaly_indicators(anomaly_type, anomaly_list)
                
                if threat_score > 0.3:
                    assessment = ThreatAssessment(
                        id=f"threat_anomaly_{anomaly_type}",
                        target=f"anomaly_cluster_{anomaly_type}",
                        target_type="anomaly_cluster",
                        threat_level=threat_level,
                        threat_score=threat_score,
                        indicators=indicators,
                        assessment_timestamp=datetime.utcnow(),
                        metadata={
                            "anomaly_type": anomaly_type,
                            "anomaly_count": len(anomaly_list),
                            "average_severity": statistics.mean([self._severity_to_score(a.severity) for a in anomaly_list])
                        }
                    )
                    threat_assessments.append(assessment)
            
            return threat_assessments
            
        except Exception as e:
            logger.error(f"Error correlating anomaly threats: {e}")
            return []
    
    async def _calculate_entity_threat_score(self, entity: Entity) -> float:
        """Calculate threat score for an entity"""
        try:
            threat_score = 0.0
            
            # Account age factors
            if entity.created_at:
                days_old = (datetime.utcnow() - entity.created_at).days
                if days_old < 30:
                    threat_score += 0.2  # Recently created account
                if days_old < 7:
                    threat_score += 0.3  # Very recently created
            
            # Follower ratio factors
            followers_count = entity.followers_count or 0
            following_count = entity.following_count or 0
            
            if followers_count > 0 and following_count > 0:
                ratio = followers_count / following_count
                if ratio > 100:
                    threat_score += 0.4  # Suspicious follower ratio
                elif ratio > 50:
                    threat_score += 0.2  # Moderately suspicious ratio
            
            # Bot-like behavior
            if followers_count > 5000 and following_count > 4000:
                threat_score += 0.3  # Bot-like following behavior
            
            # Cross-platform presence
            if hasattr(entity, 'metadata') and entity.metadata:
                all_platforms = entity.metadata.get('all_platforms', [])
                if len(all_platforms) > 5:
                    threat_score += 0.2  # Many platforms
                if len(all_platforms) > 10:
                    threat_score += 0.3  # Very many platforms
            
            # Content-based threats
            if hasattr(entity, 'bio') and entity.bio:
                bio_lower = entity.bio.lower()
                for threat_type, keywords in self.threat_indicators.items():
                    for keyword in keywords:
                        if keyword in bio_lower:
                            threat_score += 0.2
                            break
            
            # Growth rate factors
            if entity.created_at and followers_count > 0:
                growth_rate = followers_count / max((datetime.utcnow() - entity.created_at).days, 1)
                if growth_rate > 100:
                    threat_score += 0.4  # Suspicious growth rate
                elif growth_rate > 50:
                    threat_score += 0.2  # Moderately suspicious growth
            
            return min(threat_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating entity threat score: {e}")
            return 0.0
    
    async def _calculate_relationship_threat_score(self, rel_type: str, relationships: List[Relationship]) -> float:
        """Calculate threat score for relationships"""
        try:
            threat_score = 0.0
            
            # Relationship type factors
            if rel_type == "mentions":
                # Analyze mention patterns
                mention_counts = Counter([rel.source_id for rel in relationships])
                if len(mention_counts) > 0:
                    avg_mentions = statistics.mean(mention_counts.values())
                    if avg_mentions > 10:
                        threat_score += 0.3  # Excessive mentioning
                    elif avg_mentions > 5:
                        threat_score += 0.2  # High mentioning
            
            elif rel_type == "same_user":
                # Cross-platform same user relationships
                if len(relationships) > 5:
                    threat_score += 0.3  # Many cross-platform accounts
                elif len(relationships) > 2:
                    threat_score += 0.2  # Multiple cross-platform accounts
            
            elif rel_type == "authored":
                # Analyze posting patterns
                if len(relationships) > 100:
                    threat_score += 0.2  # High posting volume
            
            # Platform diversity
            platforms = set([rel.platform for rel in relationships])
            if len(platforms) > 3:
                threat_score += 0.2  # Cross-platform activity
            
            # Relationship strength
            avg_strength = statistics.mean([rel.strength for rel in relationships])
            if avg_strength > 0.8:
                threat_score += 0.1  # Strong relationships
            
            return min(threat_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating relationship threat score: {e}")
            return 0.0
    
    async def _calculate_pattern_threat_score(self, pattern_type: str, patterns: List[Pattern]) -> float:
        """Calculate threat score for patterns"""
        try:
            threat_score = 0.0
            
            # Pattern type factors
            if pattern_type == "behavioral":
                # Behavioral patterns
                for pattern in patterns:
                    if "suspicious" in pattern.category.lower():
                        threat_score += 0.3
                    elif "bot" in pattern.category.lower():
                        threat_score += 0.4
                    elif "frequency" in pattern.category.lower():
                        threat_score += 0.2
            
            elif pattern_type == "network":
                # Network patterns
                for pattern in patterns:
                    if "cluster" in pattern.category.lower():
                        threat_score += 0.2
                    elif "influence" in pattern.category.lower():
                        threat_score += 0.3
                    elif "cross_platform" in pattern.category.lower():
                        threat_score += 0.2
            
            elif pattern_type == "temporal":
                # Temporal patterns
                for pattern in patterns:
                    if "rapid" in pattern.category.lower():
                        threat_score += 0.4
                    elif "growth" in pattern.category.lower():
                        threat_score += 0.3
                    elif "creation" in pattern.category.lower():
                        threat_score += 0.2
            
            elif pattern_type == "content":
                # Content patterns
                for pattern in patterns:
                    if "hashtag" in pattern.category.lower():
                        threat_score += 0.1
                    elif "mention" in pattern.category.lower():
                        threat_score += 0.2
                    elif "url" in pattern.category.lower():
                        threat_score += 0.3
            
            # Pattern confidence
            avg_confidence = statistics.mean([p.confidence for p in patterns])
            threat_score += avg_confidence * 0.2
            
            # Pattern severity
            high_severity_count = sum(1 for p in patterns if p.severity == "high")
            if high_severity_count > 0:
                threat_score += min(high_severity_count * 0.2, 0.4)
            
            return min(threat_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating pattern threat score: {e}")
            return 0.0
    
    async def _calculate_anomaly_threat_score(self, anomaly_type: str, anomalies: List[Anomaly]) -> float:
        """Calculate threat score for anomalies"""
        try:
            threat_score = 0.0
            
            # Anomaly type factors
            if anomaly_type == "behavioral":
                # Behavioral anomalies
                for anomaly in anomalies:
                    if "suspicious" in anomaly.category.lower():
                        threat_score += 0.4
                    elif "bot" in anomaly.category.lower():
                        threat_score += 0.5
                    elif "ratio" in anomaly.category.lower():
                        threat_score += 0.3
                    elif "frequency" in anomaly.category.lower():
                        threat_score += 0.2
            
            elif anomaly_type == "network":
                # Network anomalies
                for anomaly in anomalies:
                    if "centrality" in anomaly.category.lower():
                        threat_score += 0.3
                    elif "cluster" in anomaly.category.lower():
                        threat_score += 0.2
                    elif "communication" in anomaly.category.lower():
                        threat_score += 0.2
            
            elif anomaly_type == "temporal":
                # Temporal anomalies
                for anomaly in anomalies:
                    if "rapid" in anomaly.category.lower():
                        threat_score += 0.5
                    elif "growth" in anomaly.category.lower():
                        threat_score += 0.4
                    elif "creation" in anomaly.category.lower():
                        threat_score += 0.3
                    elif "seasonal" in anomaly.category.lower():
                        threat_score += 0.1
            
            elif anomaly_type == "content":
                # Content anomalies
                for anomaly in anomalies:
                    if "url" in anomaly.category.lower():
                        threat_score += 0.3
                    elif "mention" in anomaly.category.lower():
                        threat_score += 0.2
                    elif "hashtag" in anomaly.category.lower():
                        threat_score += 0.1
                    elif "sentiment" in anomaly.category.lower():
                        threat_score += 0.2
            
            # Anomaly severity
            high_severity_count = sum(1 for a in anomalies if a.severity == "high")
            medium_severity_count = sum(1 for a in anomalies if a.severity == "medium")
            
            if high_severity_count > 0:
                threat_score += min(high_severity_count * 0.3, 0.6)
            if medium_severity_count > 0:
                threat_score += min(medium_severity_count * 0.2, 0.4)
            
            # Anomaly confidence
            avg_confidence = statistics.mean([a.confidence for a in anomalies])
            threat_score += avg_confidence * 0.2
            
            return min(threat_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating anomaly threat score: {e}")
            return 0.0
    
    async def _identify_entity_indicators(self, entity: Entity) -> List[str]:
        """Identify threat indicators for an entity"""
        try:
            indicators = []
            
            # Account age indicators
            if entity.created_at:
                days_old = (datetime.utcnow() - entity.created_at).days
                if days_old < 30:
                    indicators.append("Recently created account")
                if days_old < 7:
                    indicators.append("Very recently created account")
            
            # Follower ratio indicators
            followers_count = entity.followers_count or 0
            following_count = entity.following_count or 0
            
            if followers_count > 0 and following_count > 0:
                ratio = followers_count / following_count
                if ratio > 100:
                    indicators.append("Suspicious follower ratio")
                elif ratio > 50:
                    indicators.append("Moderately suspicious follower ratio")
            
            # Bot-like behavior indicators
            if followers_count > 5000 and following_count > 4000:
                indicators.append("Bot-like following behavior")
            
            # Cross-platform indicators
            if hasattr(entity, 'metadata') and entity.metadata:
                all_platforms = entity.metadata.get('all_platforms', [])
                if len(all_platforms) > 10:
                    indicators.append("Presence on many platforms")
                elif len(all_platforms) > 5:
                    indicators.append("Cross-platform presence")
            
            # Content-based indicators
            if hasattr(entity, 'bio') and entity.bio:
                bio_lower = entity.bio.lower()
                for threat_type, keywords in self.threat_indicators.items():
                    for keyword in keywords:
                        if keyword in bio_lower:
                            indicators.append(f"Contains {threat_type} keywords")
                            break
            
            # Growth rate indicators
            if entity.created_at and followers_count > 0:
                growth_rate = followers_count / max((datetime.utcnow() - entity.created_at).days, 1)
                if growth_rate > 100:
                    indicators.append("Suspicious growth rate")
                elif growth_rate > 50:
                    indicators.append("Moderately suspicious growth rate")
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error identifying entity indicators: {e}")
            return ["Unable to analyze entity indicators"]
    
    async def _identify_relationship_indicators(self, rel_type: str, relationships: List[Relationship]) -> List[str]:
        """Identify threat indicators for relationships"""
        try:
            indicators = []
            
            if rel_type == "mentions":
                mention_counts = Counter([rel.source_id for rel in relationships])
                if len(mention_counts) > 0:
                    avg_mentions = statistics.mean(mention_counts.values())
                    if avg_mentions > 10:
                        indicators.append("Excessive mentioning behavior")
                    elif avg_mentions > 5:
                        indicators.append("High mentioning frequency")
            
            elif rel_type == "same_user":
                if len(relationships) > 5:
                    indicators.append("Multiple cross-platform accounts")
                elif len(relationships) > 2:
                    indicators.append("Cross-platform account presence")
            
            elif rel_type == "authored":
                if len(relationships) > 100:
                    indicators.append("High posting volume")
            
            # Platform diversity
            platforms = set([rel.platform for rel in relationships])
            if len(platforms) > 3:
                indicators.append("Cross-platform activity")
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error identifying relationship indicators: {e}")
            return ["Unable to analyze relationship indicators"]
    
    async def _identify_pattern_indicators(self, pattern_type: str, patterns: List[Pattern]) -> List[str]:
        """Identify threat indicators for patterns"""
        try:
            indicators = []
            
            if pattern_type == "behavioral":
                for pattern in patterns:
                    if "suspicious" in pattern.category.lower():
                        indicators.append("Suspicious behavioral patterns")
                    elif "bot" in pattern.category.lower():
                        indicators.append("Bot-like behavior patterns")
                    elif "frequency" in pattern.category.lower():
                        indicators.append("Unusual activity frequency")
            
            elif pattern_type == "network":
                for pattern in patterns:
                    if "cluster" in pattern.category.lower():
                        indicators.append("Network clustering patterns")
                    elif "influence" in pattern.category.lower():
                        indicators.append("High network influence")
                    elif "cross_platform" in pattern.category.lower():
                        indicators.append("Cross-platform network activity")
            
            elif pattern_type == "temporal":
                for pattern in patterns:
                    if "rapid" in pattern.category.lower():
                        indicators.append("Rapid activity patterns")
                    elif "growth" in pattern.category.lower():
                        indicators.append("Unusual growth patterns")
                    elif "creation" in pattern.category.lower():
                        indicators.append("Account creation patterns")
            
            elif pattern_type == "content":
                for pattern in patterns:
                    if "hashtag" in pattern.category.lower():
                        indicators.append("Unusual hashtag usage")
                    elif "mention" in pattern.category.lower():
                        indicators.append("Unusual mention patterns")
                    elif "url" in pattern.category.lower():
                        indicators.append("Suspicious URL patterns")
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error identifying pattern indicators: {e}")
            return ["Unable to analyze pattern indicators"]
    
    async def _identify_anomaly_indicators(self, anomaly_type: str, anomalies: List[Anomaly]) -> List[str]:
        """Identify threat indicators for anomalies"""
        try:
            indicators = []
            
            if anomaly_type == "behavioral":
                for anomaly in anomalies:
                    if "suspicious" in anomaly.category.lower():
                        indicators.append("Suspicious behavioral anomalies")
                    elif "bot" in anomaly.category.lower():
                        indicators.append("Bot-like behavior anomalies")
                    elif "ratio" in anomaly.category.lower():
                        indicators.append("Suspicious ratio anomalies")
                    elif "frequency" in anomaly.category.lower():
                        indicators.append("Unusual frequency anomalies")
            
            elif anomaly_type == "network":
                for anomaly in anomalies:
                    if "centrality" in anomaly.category.lower():
                        indicators.append("Network centrality anomalies")
                    elif "cluster" in anomaly.category.lower():
                        indicators.append("Network clustering anomalies")
                    elif "communication" in anomaly.category.lower():
                        indicators.append("Communication pattern anomalies")
            
            elif anomaly_type == "temporal":
                for anomaly in anomalies:
                    if "rapid" in anomaly.category.lower():
                        indicators.append("Rapid activity anomalies")
                    elif "growth" in anomaly.category.lower():
                        indicators.append("Growth rate anomalies")
                    elif "creation" in anomaly.category.lower():
                        indicators.append("Creation timing anomalies")
                    elif "seasonal" in anomaly.category.lower():
                        indicators.append("Seasonal pattern anomalies")
            
            elif anomaly_type == "content":
                for anomaly in anomalies:
                    if "url" in anomaly.category.lower():
                        indicators.append("URL pattern anomalies")
                    elif "mention" in anomaly.category.lower():
                        indicators.append("Mention pattern anomalies")
                    elif "hashtag" in anomaly.category.lower():
                        indicators.append("Hashtag usage anomalies")
                    elif "sentiment" in anomaly.category.lower():
                        indicators.append("Sentiment pattern anomalies")
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error identifying anomaly indicators: {e}")
            return ["Unable to analyze anomaly indicators"]
    
    def _determine_threat_level(self, threat_score: float) -> ThreatLevel:
        """Determine threat level based on score"""
        try:
            if threat_score >= 0.8:
                return ThreatLevel.HIGH
            elif threat_score >= 0.5:
                return ThreatLevel.MEDIUM
            elif threat_score >= 0.3:
                return ThreatLevel.LOW
            else:
                return ThreatLevel.NONE
                
        except Exception as e:
            logger.error(f"Error determining threat level: {e}")
            return ThreatLevel.NONE
    
    def _severity_to_score(self, severity: str) -> float:
        """Convert severity string to numeric score"""
        try:
            severity_map = {
                "high": 0.8,
                "medium": 0.5,
                "low": 0.2
            }
            return severity_map.get(severity.lower(), 0.0)
            
        except Exception as e:
            logger.error(f"Error converting severity to score: {e}")
            return 0.0
    
    def _load_threat_indicators(self) -> Dict[str, List[str]]:
        """Load threat indicator keywords"""
        return {
            "malware": ["malware", "virus", "trojan", "backdoor", "exploit", "keylogger", "ransomware"],
            "phishing": ["phishing", "scam", "fake", "spoof", "credential", "password", "login"],
            "hacking": ["hack", "crack", "bypass", "inject", "overflow", "ddos", "exploit"],
            "extremism": ["hate", "violence", "terror", "extremist", "radical", "jihad", "nazi"],
            "fraud": ["fraud", "scam", "fake", "counterfeit", "illegal", "money", "bitcoin"],
            "spam": ["spam", "bot", "automated", "bulk", "mass", "advertisement"],
            "cybercrime": ["cyber", "crime", "illegal", "hack", "steal", "breach"],
            "disinformation": ["fake", "news", "disinformation", "propaganda", "conspiracy"]
        }
    
    def _load_threat_patterns(self) -> Dict[str, Any]:
        """Load threat pattern definitions"""
        return {
            "bot_behavior": {
                "indicators": ["high_following", "low_engagement", "rapid_posting"],
                "weight": 0.8
            },
            "suspicious_growth": {
                "indicators": ["rapid_follower_growth", "recent_creation"],
                "weight": 0.7
            },
            "cross_platform": {
                "indicators": ["multiple_platforms", "same_username"],
                "weight": 0.6
            },
            "content_threats": {
                "indicators": ["malicious_urls", "threat_keywords"],
                "weight": 0.5
            }
        }
    
    def _load_risk_factors(self) -> Dict[str, float]:
        """Load risk factor weights"""
        return {
            "account_age": 0.3,
            "follower_ratio": 0.4,
            "growth_rate": 0.5,
            "cross_platform": 0.3,
            "content_analysis": 0.4,
            "behavioral_patterns": 0.6,
            "network_analysis": 0.5,
            "temporal_patterns": 0.4
        }
    
    def _load_threat_scoring(self) -> Dict[str, Any]:
        """Load threat scoring configuration"""
        return {
            "thresholds": {
                "high": 0.8,
                "medium": 0.5,
                "low": 0.3
            },
            "weights": {
                "entity": 0.4,
                "relationship": 0.3,
                "pattern": 0.2,
                "anomaly": 0.1
            },
            "multipliers": {
                "recent_creation": 1.5,
                "suspicious_ratio": 2.0,
                "bot_behavior": 1.8,
                "cross_platform": 1.3
            }
        } 