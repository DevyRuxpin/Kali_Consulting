"""
Threat analyzer service for OSINT investigations
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import re

from app.core.config import settings
from app.models.schemas import ThreatAssessment, ThreatLevel

logger = logging.getLogger(__name__)

class ThreatAnalyzer:
    """Threat analysis service for OSINT investigations"""
    
    def __init__(self):
        self.threat_patterns = {
            "extremist_keywords": [
                "nazi", "white supremacy", "hate speech", "terrorism",
                "extremist", "radical", "hate group", "supremacist"
            ],
            "suspicious_patterns": [
                r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # IP addresses
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Emails
                r"\b\d{3}-\d{3}-\d{4}\b",  # Phone numbers
            ]
        }
        
    async def analyze_threat(self, target: str, analysis_type: str = "comprehensive") -> ThreatAssessment:
        """Analyze threat level for a target"""
        try:
            threat_score = 0.0
            indicators: List[str] = []
            risk_factors: List[str] = []
            recommendations: List[str] = []
            
            # Basic threat analysis
            if analysis_type in ["comprehensive", "basic"]:
                basic_analysis = await self._basic_threat_analysis(target)
                threat_score += basic_analysis["score"]
                indicators.extend(basic_analysis["indicators"])
                risk_factors.extend(basic_analysis["risk_factors"])
            
            # Advanced threat analysis
            if analysis_type in ["comprehensive", "deep"]:
                advanced_analysis = await self._advanced_threat_analysis(target)
                threat_score += advanced_analysis["score"]
                indicators.extend(advanced_analysis["indicators"])
                risk_factors.extend(advanced_analysis["risk_factors"])
            
            # Determine threat level
            if threat_score >= 0.8:
                threat_level = ThreatLevel.CRITICAL
            elif threat_score >= 0.6:
                threat_level = ThreatLevel.HIGH
            elif threat_score >= 0.4:
                threat_level = ThreatLevel.MEDIUM
            else:
                threat_level = ThreatLevel.LOW
            
            # Generate recommendations
            recommendations = self._generate_recommendations(threat_level, indicators)
            
            return ThreatAssessment(
                target=target,
                threat_level=threat_level,
                threat_score=min(threat_score, 1.0),
                indicators=indicators,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.8 if analysis_type == "comprehensive" else 0.6
            )
            
        except Exception as e:
            logger.error(f"Error analyzing threat for {target}: {e}")
            return ThreatAssessment(
                target=target,
                threat_level=ThreatLevel.LOW,
                threat_score=0.0,
                indicators=[],
                risk_factors=[],
                recommendations=[],
                confidence=0.0
            )
    
    async def _basic_threat_analysis(self, target: str) -> Dict[str, Any]:
        """Perform basic threat analysis"""
        score = 0.0
        indicators: List[str] = []
        risk_factors: List[str] = []
        
        # Check for extremist keywords
        target_lower = target.lower()
        for keyword in self.threat_patterns["extremist_keywords"]:
            if keyword in target_lower:
                score += 0.3
                indicators.append(f"Extremist keyword detected: {keyword}")
                risk_factors.append("Potential extremist content")
        
        # Check for suspicious patterns
        for pattern in self.threat_patterns["suspicious_patterns"]:
            matches = re.findall(pattern, target)
            if matches:
                score += 0.1
                indicators.append(f"Suspicious pattern detected: {pattern}")
                risk_factors.append("Suspicious data patterns")
        
        return {
            "score": score,
            "indicators": indicators,
            "risk_factors": risk_factors
        }
    
    async def _advanced_threat_analysis(self, target: str) -> Dict[str, Any]:
        """Perform advanced threat analysis"""
        score = 0.0
        indicators: List[str] = []
        risk_factors: List[str] = []
        
        # This would include more sophisticated analysis
        # such as network analysis, temporal patterns, etc.
        
        return {
            "score": score,
            "indicators": indicators,
            "risk_factors": risk_factors
        }
    
    def _generate_recommendations(self, threat_level: ThreatLevel, indicators: List[str]) -> List[str]:
        """Generate security recommendations based on threat level"""
        recommendations: List[str] = []
        
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.extend([
                "Immediate investigation required",
                "Contact law enforcement if necessary",
                "Implement enhanced monitoring",
                "Review security protocols"
            ])
        elif threat_level == ThreatLevel.HIGH:
            recommendations.extend([
                "Enhanced monitoring recommended",
                "Review access controls",
                "Update security policies",
                "Consider threat intelligence feeds"
            ])
        elif threat_level == ThreatLevel.MEDIUM:
            recommendations.extend([
                "Monitor for changes",
                "Review security practices",
                "Update threat models"
            ])
        else:
            recommendations.append("Continue standard monitoring")
        
        return recommendations 