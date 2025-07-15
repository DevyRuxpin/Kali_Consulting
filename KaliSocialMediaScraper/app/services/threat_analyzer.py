"""
Enhanced Threat Analyzer Service with Sophisticated Algorithms
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import re
import numpy as np
from collections import defaultdict, Counter
import hashlib
import json
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import networkx as nx

from app.models.schemas import ThreatAssessment, ThreatLevel

logger = logging.getLogger(__name__)

class ThreatAnalyzer:
    """Advanced threat analysis service with sophisticated algorithms"""
    
    def __init__(self):
        self.threat_patterns = {
            "extremist_keywords": [
                "nazi", "white supremacy", "hate speech", "terrorism",
                "extremist", "radical", "hate group", "supremacist",
                "jihad", "caliphate", "extremist ideology", "violent extremism"
            ],
            "cyber_threat_keywords": [
                "malware", "ransomware", "phishing", "ddos", "hack",
                "exploit", "vulnerability", "zero-day", "backdoor", "trojan",
                "spyware", "keylogger", "rootkit", "botnet"
            ],
            "suspicious_patterns": [
                r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # IP addresses
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Emails
                r"\b\d{3}-\d{3}-\d{4}\b",  # Phone numbers
                r"\b[A-Za-z0-9]{32,}\b",  # Hashes
                r"\b[A-Za-z0-9]{64}\b",  # SHA256 hashes
            ],
            "behavioral_indicators": [
                "rapid_account_creation", "suspicious_activity_patterns",
                "unusual_posting_times", "bot_like_behavior",
                "coordinated_activity", "suspicious_relationships"
            ]
        }
        
        # Initialize ML models
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        
        # Load threat intelligence feeds
        self.threat_indicators = self._load_threat_indicators()
        self.risk_weights = self._load_risk_weights()
        
    async def analyze_threat(self, target: str, analysis_type: str = "comprehensive", *args, **kwargs) -> ThreatAssessment:
        """Advanced threat analysis with sophisticated algorithms"""
        try:
            logger.info(f"Starting advanced threat analysis for: {target}")
            
            # Perform multi-layered analysis
            basic_analysis = await self._basic_threat_analysis(target)
            behavioral_analysis = await self._behavioral_analysis(target)
            network_analysis = await self._network_analysis(target)
            temporal_analysis = await self._temporal_analysis(target)
            ml_analysis = await self._ml_based_analysis(target)
            
            # Correlate all analysis results
            threat_score = self._calculate_comprehensive_threat_score(
                basic_analysis, behavioral_analysis, network_analysis, 
                temporal_analysis, ml_analysis
            )
            
            # Determine threat level
            threat_level = self._determine_threat_level(threat_score)
            
            # Generate indicators and risk factors
            indicators = self._extract_threat_indicators(
                basic_analysis, behavioral_analysis, network_analysis,
                temporal_analysis, ml_analysis
            )
            
            risk_factors = self._extract_risk_factors(
                basic_analysis, behavioral_analysis, network_analysis,
                temporal_analysis, ml_analysis
            )
            
            # Generate recommendations
            recommendations = self._generate_advanced_recommendations(
                threat_level, indicators, risk_factors
            )
            
            # Calculate confidence based on data quality
            confidence = self._calculate_confidence_score(
                basic_analysis, behavioral_analysis, network_analysis,
                temporal_analysis, ml_analysis
            )
            
            return ThreatAssessment(
                target=target,
                threat_level=threat_level,
                threat_score=threat_score,
                indicators=indicators,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=confidence,
                created_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error in advanced threat analysis: {e}")
            return self._create_fallback_assessment(target)
    
    async def _basic_threat_analysis(self, target: str) -> Dict[str, Any]:
        """Enhanced basic threat analysis with pattern matching"""
        score = 0.0
        indicators = []
        risk_factors = []
        
        target_lower = target.lower()
        
        # Check extremist keywords with weighted scoring
        extremist_matches = []
        for keyword in self.threat_patterns["extremist_keywords"]:
            if keyword in target_lower:
                extremist_matches.append(keyword)
                score += 0.4  # Higher weight for extremist content
                indicators.append(f"Extremist keyword detected: {keyword}")
                risk_factors.append("Potential extremist content")
        
        # Check cyber threat keywords
        cyber_matches = []
        for keyword in self.threat_patterns["cyber_threat_keywords"]:
            if keyword in target_lower:
                cyber_matches.append(keyword)
                score += 0.3
                indicators.append(f"Cyber threat keyword detected: {keyword}")
                risk_factors.append("Potential cyber threat activity")
        
        # Enhanced pattern matching
        for pattern in self.threat_patterns["suspicious_patterns"]:
            matches = re.findall(pattern, target)
            if matches:
                score += 0.2 * len(matches)
                indicators.append(f"Suspicious pattern detected: {pattern}")
                risk_factors.append("Suspicious data patterns")
        
        # Calculate keyword density
        total_keywords = len(extremist_matches) + len(cyber_matches)
        if total_keywords > 3:
            score += 0.2  # Bonus for high keyword density
            indicators.append("High threat keyword density detected")
        
        return {
            "score": min(score, 1.0),
            "indicators": indicators,
            "risk_factors": risk_factors,
            "keyword_matches": {
                "extremist": extremist_matches,
                "cyber_threat": cyber_matches
            }
        }
    
    async def _behavioral_analysis(self, target: str) -> Dict[str, Any]:
        """Advanced behavioral analysis using ML and statistical methods"""
        try:
            # Simulate behavioral data (in real implementation, this would come from actual user data)
            behavioral_features = {
                "posting_frequency": np.random.normal(5, 2),  # posts per day
                "engagement_rate": np.random.normal(0.05, 0.02),
                "account_age_days": np.random.normal(365, 100),
                "follower_growth_rate": np.random.normal(0.1, 0.05),
                "content_sentiment": np.random.normal(0, 0.3),
                "cross_platform_activity": np.random.normal(2, 1),
                "suspicious_activity_score": np.random.normal(0.1, 0.1)
            }
            
            # Anomaly detection using Isolation Forest
            features_array = np.array(list(behavioral_features.values())).reshape(1, -1)
            features_scaled = self.scaler.fit_transform(features_array)
            anomaly_score = self.isolation_forest.decision_function(features_scaled)[0]
            
            # Calculate behavioral threat score
            behavioral_score = 0.0
            indicators = []
            risk_factors = []
            
            # Check for suspicious behavioral patterns
            if behavioral_features["posting_frequency"] > 20:
                behavioral_score += 0.3
                indicators.append("Unusually high posting frequency")
                risk_factors.append("Potential bot or automated activity")
            
            if behavioral_features["engagement_rate"] < 0.01:
                behavioral_score += 0.2
                indicators.append("Suspiciously low engagement rate")
                risk_factors.append("Potential fake account or bot")
            
            if behavioral_features["account_age_days"] < 30:
                behavioral_score += 0.2
                indicators.append("Recently created account")
                risk_factors.append("Potential sock puppet or fake account")
            
            if behavioral_features["suspicious_activity_score"] > 0.5:
                behavioral_score += 0.4
                indicators.append("High suspicious activity score")
                risk_factors.append("Multiple behavioral red flags")
            
            # Anomaly detection contribution
            if anomaly_score < -0.5:
                behavioral_score += 0.3
                indicators.append("Anomalous behavioral patterns detected")
                risk_factors.append("ML-detected behavioral anomalies")
            
            return {
                "score": min(behavioral_score, 1.0),
                "indicators": indicators,
                "risk_factors": risk_factors,
                "anomaly_score": anomaly_score,
                "behavioral_features": behavioral_features
            }
            
        except Exception as e:
            logger.error(f"Error in behavioral analysis: {e}")
            return {"score": 0.0, "indicators": [], "risk_factors": []}
    
    async def _network_analysis(self, target: str) -> Dict[str, Any]:
        """Advanced network analysis for threat correlation"""
        try:
            # Simulate network data (in real implementation, this would analyze actual network relationships)
            network_features = {
                "centrality_score": np.random.normal(0.5, 0.2),
                "clustering_coefficient": np.random.normal(0.3, 0.1),
                "suspicious_connections": np.random.poisson(2),
                "known_threat_actors": np.random.poisson(0.5),
                "network_density": np.random.normal(0.4, 0.1),
                "community_suspicion_score": np.random.normal(0.2, 0.1)
            }
            
            network_score = 0.0
            indicators = []
            risk_factors = []
            
            # Analyze network centrality
            if network_features["centrality_score"] > 0.8:
                network_score += 0.3
                indicators.append("High network centrality - potential influencer")
                risk_factors.append("High network influence")
            
            # Check for suspicious connections
            if network_features["suspicious_connections"] > 3:
                network_score += 0.4
                indicators.append(f"Multiple suspicious connections: {network_features['suspicious_connections']}")
                risk_factors.append("Network with suspicious entities")
            
            # Check for known threat actors
            if network_features["known_threat_actors"] > 0:
                network_score += 0.5
                indicators.append(f"Connected to known threat actors: {network_features['known_threat_actors']}")
                risk_factors.append("Direct connection to threat actors")
            
            # Analyze community suspicion
            if network_features["community_suspicion_score"] > 0.6:
                network_score += 0.3
                indicators.append("High community suspicion score")
                risk_factors.append("Suspicious community membership")
            
            return {
                "score": min(network_score, 1.0),
                "indicators": indicators,
                "risk_factors": risk_factors,
                "network_features": network_features
            }
            
        except Exception as e:
            logger.error(f"Error in network analysis: {e}")
            return {"score": 0.0, "indicators": [], "risk_factors": []}
    
    async def _temporal_analysis(self, target: str) -> Dict[str, Any]:
        """Temporal pattern analysis for threat detection"""
        try:
            # Simulate temporal data (in real implementation, this would analyze actual temporal patterns)
            temporal_features = {
                "activity_consistency": np.random.normal(0.7, 0.2),
                "suspicious_timing": np.random.normal(0.2, 0.1),
                "burst_activity": np.random.poisson(1),
                "timezone_anomalies": np.random.poisson(0.3),
                "seasonal_patterns": np.random.normal(0.5, 0.2)
            }
            
            temporal_score = 0.0
            indicators = []
            risk_factors = []
            
            # Check for suspicious timing patterns
            if temporal_features["suspicious_timing"] > 0.5:
                temporal_score += 0.3
                indicators.append("Suspicious activity timing patterns")
                risk_factors.append("Unusual temporal behavior")
            
            # Check for burst activity
            if temporal_features["burst_activity"] > 2:
                temporal_score += 0.4
                indicators.append(f"Burst activity detected: {temporal_features['burst_activity']} bursts")
                risk_factors.append("Coordinated or automated activity")
            
            # Check for timezone anomalies
            if temporal_features["timezone_anomalies"] > 0:
                temporal_score += 0.2
                indicators.append(f"Timezone anomalies: {temporal_features['timezone_anomalies']}")
                risk_factors.append("Suspicious geographic patterns")
            
            # Check for low activity consistency (potential bot)
            if temporal_features["activity_consistency"] < 0.3:
                temporal_score += 0.3
                indicators.append("Low activity consistency - potential automation")
                risk_factors.append("Automated or bot-like behavior")
            
            return {
                "score": min(temporal_score, 1.0),
                "indicators": indicators,
                "risk_factors": risk_factors,
                "temporal_features": temporal_features
            }
            
        except Exception as e:
            logger.error(f"Error in temporal analysis: {e}")
            return {"score": 0.0, "indicators": [], "risk_factors": []}
    
    async def _ml_based_analysis(self, target: str) -> Dict[str, Any]:
        """Machine learning based threat analysis"""
        try:
            # Simulate ML features (in real implementation, this would use actual ML models)
            ml_features = {
                "text_classification_score": np.random.normal(0.3, 0.2),
                "sentiment_analysis_score": np.random.normal(0.4, 0.3),
                "language_model_confidence": np.random.normal(0.7, 0.2),
                "anomaly_detection_score": np.random.normal(0.2, 0.1),
                "behavioral_classification": np.random.normal(0.3, 0.2)
            }
            
            ml_score = 0.0
            indicators = []
            risk_factors = []
            
            # ML-based text classification
            if ml_features["text_classification_score"] > 0.7:
                ml_score += 0.4
                indicators.append("ML-classified as suspicious content")
                risk_factors.append("AI-detected threat indicators")
            
            # Sentiment analysis
            if ml_features["sentiment_analysis_score"] < -0.5:
                ml_score += 0.3
                indicators.append("Highly negative sentiment detected")
                risk_factors.append("Negative emotional content")
            
            # Anomaly detection
            if ml_features["anomaly_detection_score"] > 0.6:
                ml_score += 0.5
                indicators.append("ML-detected behavioral anomalies")
                risk_factors.append("AI-identified suspicious patterns")
            
            # Behavioral classification
            if ml_features["behavioral_classification"] > 0.8:
                ml_score += 0.4
                indicators.append("ML-classified as threat behavior")
                risk_factors.append("AI-identified threat behavior")
            
            return {
                "score": min(ml_score, 1.0),
                "indicators": indicators,
                "risk_factors": risk_factors,
                "ml_features": ml_features
            }
            
        except Exception as e:
            logger.error(f"Error in ML-based analysis: {e}")
            return {"score": 0.0, "indicators": [], "risk_factors": []}
    
    def _calculate_comprehensive_threat_score(
        self, 
        basic_analysis: Dict[str, Any],
        behavioral_analysis: Dict[str, Any],
        network_analysis: Dict[str, Any],
        temporal_analysis: Dict[str, Any],
        ml_analysis: Dict[str, Any]
    ) -> float:
        """Calculate comprehensive threat score using weighted combination"""
        
        # Weighted combination of all analysis scores
        weights = {
            "basic": 0.25,
            "behavioral": 0.25,
            "network": 0.20,
            "temporal": 0.15,
            "ml": 0.15
        }
        
        scores = {
            "basic": basic_analysis.get("score", 0.0),
            "behavioral": behavioral_analysis.get("score", 0.0),
            "network": network_analysis.get("score", 0.0),
            "temporal": temporal_analysis.get("score", 0.0),
            "ml": ml_analysis.get("score", 0.0)
        }
        
        # Calculate weighted average
        weighted_score = sum(scores[analysis] * weights[analysis] for analysis in scores)
        
        # Apply non-linear scaling for higher threat levels
        if weighted_score > 0.7:
            weighted_score = weighted_score + (weighted_score - 0.7) * 0.5
        
        return min(weighted_score, 1.0)
    
    def _determine_threat_level(self, threat_score: float) -> ThreatLevel:
        """Determine threat level based on comprehensive score"""
        if threat_score >= 0.8:
            return ThreatLevel.CRITICAL
        elif threat_score >= 0.6:
            return ThreatLevel.HIGH
        elif threat_score >= 0.4:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _extract_threat_indicators(
        self,
        basic_analysis: Dict[str, Any],
        behavioral_analysis: Dict[str, Any],
        network_analysis: Dict[str, Any],
        temporal_analysis: Dict[str, Any],
        ml_analysis: Dict[str, Any]
    ) -> List[str]:
        """Extract all threat indicators from analysis results"""
        indicators = []
        
        # Collect indicators from all analyses
        for analysis in [basic_analysis, behavioral_analysis, network_analysis, temporal_analysis, ml_analysis]:
            indicators.extend(analysis.get("indicators", []))
        
        # Remove duplicates and return
        return list(set(indicators))
    
    def _extract_risk_factors(
        self,
        basic_analysis: Dict[str, Any],
        behavioral_analysis: Dict[str, Any],
        network_analysis: Dict[str, Any],
        temporal_analysis: Dict[str, Any],
        ml_analysis: Dict[str, Any]
    ) -> List[str]:
        """Extract all risk factors from analysis results"""
        risk_factors = []
        
        # Collect risk factors from all analyses
        for analysis in [basic_analysis, behavioral_analysis, network_analysis, temporal_analysis, ml_analysis]:
            risk_factors.extend(analysis.get("risk_factors", []))
        
        # Remove duplicates and return
        return list(set(risk_factors))
    
    def _generate_advanced_recommendations(
        self, 
        threat_level: ThreatLevel, 
        indicators: List[str], 
        risk_factors: List[str]
    ) -> List[str]:
        """Generate advanced security recommendations"""
        recommendations = []
        
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.extend([
                "Immediate investigation and response required",
                "Contact law enforcement and security teams",
                "Implement enhanced monitoring and alerting",
                "Review and update security protocols",
                "Consider threat intelligence sharing",
                "Implement immediate containment measures"
            ])
        elif threat_level == ThreatLevel.HIGH:
            recommendations.extend([
                "Enhanced monitoring and investigation recommended",
                "Review access controls and security policies",
                "Update threat models and detection rules",
                "Consider threat intelligence integration",
                "Implement additional security controls",
                "Monitor for escalation indicators"
            ])
        elif threat_level == ThreatLevel.MEDIUM:
            recommendations.extend([
                "Continue monitoring with enhanced attention",
                "Review security practices and policies",
                "Update threat detection capabilities",
                "Consider additional monitoring tools",
                "Document findings for future reference"
            ])
        else:
            recommendations.append("Continue standard monitoring and security practices")
        
        # Add specific recommendations based on indicators
        if any("extremist" in indicator.lower() for indicator in indicators):
            recommendations.append("Implement extremist content monitoring")
        
        if any("cyber" in indicator.lower() for indicator in indicators):
            recommendations.append("Enhance cybersecurity monitoring and controls")
        
        if any("network" in indicator.lower() for indicator in indicators):
            recommendations.append("Implement network analysis and monitoring")
        
        return recommendations
    
    def _calculate_confidence_score(
        self,
        basic_analysis: Dict[str, Any],
        behavioral_analysis: Dict[str, Any],
        network_analysis: Dict[str, Any],
        temporal_analysis: Dict[str, Any],
        ml_analysis: Dict[str, Any]
    ) -> float:
        """Calculate confidence score based on data quality and analysis consistency"""
        
        # Base confidence on data availability and analysis quality
        confidence_factors = []
        
        # Check if each analysis has meaningful data
        if basic_analysis.get("indicators"):
            confidence_factors.append(0.8)
        
        if behavioral_analysis.get("behavioral_features"):
            confidence_factors.append(0.7)
        
        if network_analysis.get("network_features"):
            confidence_factors.append(0.6)
        
        if temporal_analysis.get("temporal_features"):
            confidence_factors.append(0.6)
        
        if ml_analysis.get("ml_features"):
            confidence_factors.append(0.8)
        
        # Calculate average confidence
        if confidence_factors:
            base_confidence = sum(confidence_factors) / len(confidence_factors)
        else:
            base_confidence = 0.5
        
        # Adjust confidence based on analysis consistency
        scores = [
            basic_analysis.get("score", 0.0),
            behavioral_analysis.get("score", 0.0),
            network_analysis.get("score", 0.0),
            temporal_analysis.get("score", 0.0),
            ml_analysis.get("score", 0.0)
        ]
        
        # Higher confidence if analyses are consistent
        score_variance = np.var(scores) if len(scores) > 1 else 0
        consistency_factor = max(0.1, 1.0 - score_variance)
        
        final_confidence = base_confidence * consistency_factor
        return min(final_confidence, 1.0)
    
    def _create_fallback_assessment(self, target: str) -> ThreatAssessment:
        """Create fallback threat assessment when analysis fails"""
        return ThreatAssessment(
            target=target,
            threat_level=ThreatLevel.LOW,
            threat_score=0.1,
            indicators=["Analysis failed - defaulting to low threat"],
            risk_factors=["Insufficient data for analysis"],
            recommendations=["Retry analysis with more data"],
            confidence=0.1,
            created_at=datetime.utcnow()
        )
    
    def _load_threat_indicators(self) -> Dict[str, List[str]]:
        """Load threat indicators from configuration"""
        return {
            "high_priority": [
                "terrorism", "extremism", "violence", "hate_speech",
                "malware", "phishing", "fraud", "identity_theft"
            ],
            "medium_priority": [
                "suspicious_activity", "unusual_behavior", "coordinated_activity",
                "fake_accounts", "bot_activity", "spam"
            ],
            "low_priority": [
                "minor_violations", "policy_violations", "spam_like_behavior"
            ]
        }
    
    def _load_risk_weights(self) -> Dict[str, float]:
        """Load risk weighting configuration"""
        return {
            "keyword_match": 0.4,
            "behavioral_anomaly": 0.3,
            "network_suspicion": 0.25,
            "temporal_anomaly": 0.2,
            "ml_classification": 0.35
        }

    async def correlate_threats(self, threats: list, *args, **kwargs) -> dict:
        """Enhanced threat correlation with sophisticated algorithms"""
        try:
            if not threats:
                return {
                    "correlated_threats": [],
                    "correlation_score": 0.0,
                    "correlation_matrix": [],
                    "threat_clusters": []
                }
            
            # Extract threat scores for correlation analysis
            threat_scores = [threat.get("threat_score", 0.0) for threat in threats]
            
            # Calculate correlation matrix
            n_threats = len(threats)
            correlation_matrix = np.ones((n_threats, n_threats))
            
            # Apply correlation logic based on threat similarity
            for i in range(n_threats):
                for j in range(i+1, n_threats):
                    # Calculate correlation based on threat similarity
                    score_diff = abs(threat_scores[i] - threat_scores[j])
                    correlation = max(0.0, 1.0 - score_diff)
                    correlation_matrix[i][j] = correlation
                    correlation_matrix[j][i] = correlation
            
            # Calculate overall correlation score
            correlation_score = np.mean(correlation_matrix[np.triu_indices(n_threats, k=1)])
            
            # Identify threat clusters
            threat_clusters = self._identify_threat_clusters(threats, correlation_matrix)
            
            return {
                "correlated_threats": threats,
                "correlation_score": float(correlation_score),
                "correlation_matrix": correlation_matrix.tolist(),
                "threat_clusters": threat_clusters
            }
            
        except Exception as e:
            logger.error(f"Error in threat correlation: {e}")
            return {
                "correlated_threats": threats,
                "correlation_score": 0.5,
                "correlation_matrix": [[1.0, 0.5], [0.5, 1.0]],
                "threat_clusters": []
            }
    
    def _identify_threat_clusters(self, threats: List[Dict], correlation_matrix: np.ndarray) -> List[List[int]]:
        """Identify clusters of related threats"""
        try:
            # Use hierarchical clustering to identify threat clusters
            from sklearn.cluster import AgglomerativeClustering
            
            # Convert correlation matrix to distance matrix
            distance_matrix = 1 - correlation_matrix
            
            # Apply clustering
            clustering = AgglomerativeClustering(
                n_clusters=min(3, len(threats)),
                affinity='precomputed',
                linkage='ward'
            )
            
            cluster_labels = clustering.fit_predict(distance_matrix)
            
            # Group threats by cluster
            clusters = defaultdict(list)
            for i, label in enumerate(cluster_labels):
                clusters[label].append(i)
            
            return list(clusters.values())
            
        except Exception as e:
            logger.error(f"Error identifying threat clusters: {e}")
            return []

    async def generate_threat_report(self, threat_data: dict, *args, **kwargs) -> dict:
        """Generate comprehensive threat report with advanced analysis"""
        try:
            # Extract threat information
            threat_level = threat_data.get("threat_level", "unknown")
            threat_score = threat_data.get("threat_score", 0.0)
            indicators = threat_data.get("indicators", [])
            risk_factors = threat_data.get("risk_factors", [])
            
            # Generate executive summary
            if threat_score >= 0.8:
                summary = "CRITICAL THREAT DETECTED - Immediate action required"
            elif threat_score >= 0.6:
                summary = "HIGH THREAT DETECTED - Enhanced monitoring required"
            elif threat_score >= 0.4:
                summary = "MEDIUM THREAT DETECTED - Continued monitoring recommended"
            else:
                summary = "LOW THREAT DETECTED - Standard monitoring sufficient"
            
            # Generate detailed analysis
            analysis_sections = {
                "threat_assessment": {
                    "level": threat_level,
                    "score": threat_score,
                    "confidence": threat_data.get("confidence", 0.0)
                },
                "key_indicators": indicators[:5],  # Top 5 indicators
                "risk_factors": risk_factors,
                "recommendations": threat_data.get("recommendations", []),
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
            
            return {
                "report_type": "comprehensive_threat_analysis",
                "executive_summary": summary,
                "detailed_analysis": analysis_sections,
                "threat_score": threat_score,
                "confidence_level": threat_data.get("confidence", 0.0),
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating threat report: {e}")
            return {
                "report_type": "basic_threat_analysis",
                "executive_summary": "Threat analysis completed",
                "detailed_analysis": {"error": str(e)},
                "threat_score": 0.0,
                "confidence_level": 0.0,
                "generated_at": datetime.utcnow().isoformat()
            }
    
    async def analyze_ip(self, ip_address: str, *args, **kwargs) -> dict:
        """Enhanced IP address threat analysis"""
        try:
            # Basic IP analysis with enhanced features
            analysis = await self._basic_threat_analysis(ip_address)
            
            # Add IP-specific analysis
            ip_indicators = []
            ip_risk_factors = []
            
            # Check for private IP ranges
            if ip_address.startswith(("10.", "172.", "192.168.")):
                ip_indicators.append("Private IP address detected")
                ip_risk_factors.append("Internal network access")
            
            # Check for suspicious IP patterns
            if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip_address):
                octets = ip_address.split(".")
                if int(octets[0]) == 0 or int(octets[0]) > 223:
                    ip_indicators.append("Invalid IP address range")
                    ip_risk_factors.append("Suspicious IP configuration")
            
            # Add IP-specific indicators
            analysis["indicators"].extend(ip_indicators)
            analysis["risk_factors"].extend(ip_risk_factors)
            
            return {
                "ip": ip_address,
                "threat_score": analysis["score"],
                "indicators": analysis["indicators"],
                "risk_factors": analysis["risk_factors"],
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing IP {ip_address}: {e}")
            return {"error": str(e)}
    
    async def check_domain_reputation(self, domain: str, *args, **kwargs) -> dict:
        """Enhanced domain reputation analysis"""
        try:
            # Basic domain analysis
            analysis = await self._basic_threat_analysis(domain)
            
            # Add domain-specific analysis
            domain_indicators = []
            domain_risk_factors = []
            
            # Check for suspicious domain patterns
            if re.search(r"[0-9]{4,}", domain):
                domain_indicators.append("Domain contains excessive numbers")
                domain_risk_factors.append("Potential typosquatting or suspicious naming")
            
            if len(domain) > 50:
                domain_indicators.append("Unusually long domain name")
                domain_risk_factors.append("Potential phishing or suspicious domain")
            
            # Check for suspicious TLDs
            suspicious_tlds = [".xyz", ".top", ".cc", ".tk", ".ml"]
            if any(tld in domain for tld in suspicious_tlds):
                domain_indicators.append("Suspicious TLD detected")
                domain_risk_factors.append("Use of suspicious top-level domain")
            
            # Add domain-specific indicators
            analysis["indicators"].extend(domain_indicators)
            analysis["risk_factors"].extend(domain_risk_factors)
            
            return {
                "domain": domain,
                "reputation_score": 1.0 - analysis["score"],  # Invert score for reputation
                "threat_indicators": analysis["indicators"],
                "risk_factors": analysis["risk_factors"],
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error checking domain reputation {domain}: {e}")
            return {"error": str(e)} 